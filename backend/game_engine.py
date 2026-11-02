import logging
from typing import Optional, Dict, Any, List, Tuple
import os
import sys

if __package__ is None or __package__ == "":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from backend.models import GameState, RoundLog, TeamState, Question, Answer, FastMoneyEntry
    from backend.database import GameDatabase
    from backend.audio_service import AudioService
else:
    from .models import GameState, RoundLog, TeamState, Question, Answer, FastMoneyEntry
    from .database import GameDatabase
    from .audio_service import AudioService

class GameEngine:
    def __init__(self, project_root: str):
        self.state = GameState()
        self.db = GameDatabase(project_root)
        self.audio = AudioService(project_root)
        
        # Load first face-off question by default if available
        self.load_first_available_question()

    def load_first_available_question(self):
        questions = self.db.get_all_face_off_questions()
        if questions:
            self.load_question(questions[0][0])

    def load_question(self, question_id: int):
        q = self.db.get_face_off_question_by_id(question_id)
        if q:
            self.state.active_question = q
            self.state.bank_points = 0
            self.state.answers_count_visible = False
            self.state.current_strike_display = 0

    def reveal_answer(self, answer_index: int) -> bool:
        if not self.state.active_question:
            return False
        
        for ans in self.state.active_question.answers:
            if ans.index == answer_index and not ans.is_revealed:
                ans.is_revealed = True
                points_to_add = ans.points * self.state.multiplier
                self.state.bank_points += points_to_add
                self.audio.play("good_answer")
                return True
        return False

    def add_strike(self, team: str) -> int:
        """Adds a strike to team ('A' or 'B'), plays sound, and returns new strike count."""
        team_state = self.state.team_a if team.upper() == "A" else self.state.team_b
        if team_state.strikes < 3:
            team_state.strikes += 1
        
        self.state.current_strike_display = team_state.strikes
        self.audio.play("strike")
        return team_state.strikes

    def clear_strike_display(self):
        self.state.current_strike_display = 0

    def reward_team(self, team: str):
        """Awards banked points to designated team and resets bank."""
        points = self.state.bank_points
        if team.upper() == "A":
            self.state.team_a.total_points += points
        else:
            self.state.team_b.total_points += points
        
        self.state.bank_points = 0

    def set_multiplier(self, multiplier: int):
        if multiplier in [1, 2, 3]:
            self.state.multiplier = multiplier

    def log_and_next_round(self) -> Optional[int]:
        """Archives current round score/strikes into match log and resets board for next round."""
        if len(self.state.match_log) >= 4:
            logging.warning("All 4 rounds already logged.")
            return None

        round_num = len(self.state.match_log) + 1
        log_entry = RoundLog(
            round_num=round_num,
            team_a_points=self.state.team_a.total_points,
            team_b_points=self.state.team_b.total_points,
            team_a_strikes=self.state.team_a.strikes,
            team_b_strikes=self.state.team_b.strikes
        )
        self.state.match_log.append(log_entry)

        # Reset for next round
        self.state.round = min(4, round_num + 1)
        self.state.bank_points = 0
        self.state.team_a.strikes = 0
        self.state.team_b.strikes = 0
        self.state.current_strike_display = 0
        self.state.multiplier = 1
        self.state.answers_count_visible = False

        if self.state.active_question:
            for ans in self.state.active_question.answers:
                ans.is_revealed = False

        return round_num

    def set_team_names(self, team_a_name: str, team_b_name: str):
        if team_a_name.strip():
            self.state.team_a.name = team_a_name.strip()
        if team_b_name.strip():
            self.state.team_b.name = team_b_name.strip()

    # --- Fast Money Methods ---

    def set_fast_money_entry(self, player_num: int, index: int, answer: str, points: int):
        entries = self.state.fast_money.p1_entries if player_num == 1 else self.state.fast_money.p2_entries
        if 0 <= index < len(entries):
            entries[index].answer = answer
            entries[index].points = points
            self._recalculate_fast_money_total()

    def reveal_fast_money_answer(self, player_num: int, index: int):
        entries = self.state.fast_money.p1_entries if player_num == 1 else self.state.fast_money.p2_entries
        if 0 <= index < len(entries):
            entries[index].is_revealed = True
            self.audio.play("fm_count")

    def reveal_fast_money_points(self, player_num: int, index: int):
        entries = self.state.fast_money.p1_entries if player_num == 1 else self.state.fast_money.p2_entries
        if 0 <= index < len(entries):
            entries[index].is_points_revealed = True
            if entries[index].points > 0:
                self.audio.play("fm_correct")
            else:
                self.audio.play("fm_no_points")
            self._recalculate_fast_money_total()

    def _recalculate_fast_money_total(self):
        total = 0
        for entry in self.state.fast_money.p1_entries:
            if entry.is_points_revealed:
                total += entry.points
        for entry in self.state.fast_money.p2_entries:
            if entry.is_points_revealed:
                total += entry.points
        
        self.state.fast_money.total_points = total
        
        # Check winning threshold
        if total >= 200 and not self.state.fast_money.winning_sound_active:
            self.state.fast_money.winning_sound_active = True
            self.audio.play("win")

    def reset_fast_money(self):
        self.state.fast_money = FastMoneyState()

    def reset_match(self):
        """Resets the entire match state back to fresh round 1."""
        team_a_name = self.state.team_a.name
        team_b_name = self.state.team_b.name
        self.state = GameState()
        self.state.team_a.name = team_a_name
        self.state.team_b.name = team_b_name
        self.load_first_available_question()

    def set_answers_count_visible(self, visible: bool):
        self.state.answers_count_visible = visible

