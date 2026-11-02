import unittest
import os
import shutil
import tempfile
from backend.models import GameState
from backend.database import GameDatabase
from backend.game_engine import GameEngine

class TestGameEngine(unittest.TestCase):
    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.engine = GameEngine(self.project_root)

    def test_initial_state(self):
        self.assertIsNotNone(self.engine.state)
        self.assertEqual(self.engine.state.round, 1)
        self.assertEqual(self.engine.state.multiplier, 1)
        self.assertEqual(self.engine.state.bank_points, 0)
        self.assertEqual(self.engine.state.team_a.total_points, 0)
        self.assertEqual(self.engine.state.team_b.total_points, 0)

    def test_database_loads_questions(self):
        questions = self.engine.db.get_all_face_off_questions()
        self.assertGreaterEqual(len(questions), 1)
        q1 = self.engine.db.get_face_off_question_by_id(questions[0][0])
        self.assertIsNotNone(q1)
        self.assertGreaterEqual(len(q1.answers), 1)

    def test_reveal_answer_and_multipliers(self):
        # Load question 1
        self.engine.load_first_available_question()
        q = self.engine.state.active_question
        self.assertIsNotNone(q)
        ans1 = q.answers[0]
        pts = ans1.points
        
        # Reveal answer 1 with 1x multiplier
        self.engine.reveal_answer(ans1.index)
        self.assertEqual(self.engine.state.bank_points, pts)

        # Set 2x multiplier and reveal answer 2 if exists
        if len(q.answers) > 1:
            ans2 = q.answers[1]
            self.engine.set_multiplier(2)
            self.engine.reveal_answer(ans2.index)
            self.assertEqual(self.engine.state.bank_points, pts + (ans2.points * 2))

    def test_strikes_and_caps(self):
        self.assertEqual(self.engine.state.team_a.strikes, 0)
        s1 = self.engine.add_strike("A")
        self.assertEqual(s1, 1)
        s2 = self.engine.add_strike("A")
        self.assertEqual(s2, 2)
        s3 = self.engine.add_strike("A")
        self.assertEqual(s3, 3)
        # Cannot exceed 3
        s4 = self.engine.add_strike("A")
        self.assertEqual(s4, 3)

    def test_reward_team_points(self):
        self.engine.state.bank_points = 80
        self.engine.reward_team("A")
        self.assertEqual(self.engine.state.team_a.total_points, 80)
        self.assertEqual(self.engine.state.bank_points, 0)

    def test_log_round_and_reset(self):
        self.engine.state.team_a.total_points = 50
        self.engine.state.team_b.total_points = 30
        self.engine.state.team_a.strikes = 2
        self.engine.state.team_b.strikes = 1

        r_logged = self.engine.log_and_next_round()
        self.assertEqual(r_logged, 1)
        self.assertEqual(len(self.engine.state.match_log), 1)
        self.assertEqual(self.engine.state.match_log[0].team_a_points, 50)
        self.assertEqual(self.engine.state.round, 2)
        self.assertEqual(self.engine.state.team_a.strikes, 0)
        self.assertEqual(self.engine.state.team_b.strikes, 0)

    def test_fast_money_scoring(self):
        self.engine.set_fast_money_entry(player_num=1, index=0, answer="Tenga", points=32)
        self.engine.reveal_fast_money_points(player_num=1, index=0)
        self.assertEqual(self.engine.state.fast_money.total_points, 32)

    def test_reset_match_and_answers_count(self):
        self.engine.set_answers_count_visible(True)
        self.assertTrue(self.engine.state.answers_count_visible)
        self.engine.set_answers_count_visible(False)
        self.assertFalse(self.engine.state.answers_count_visible)

        self.engine.state.team_a.total_points = 150
        self.engine.state.team_b.total_points = 120
        self.engine.reset_match()
        self.assertEqual(self.engine.state.team_a.total_points, 0)
        self.assertEqual(self.engine.state.team_b.total_points, 0)
        self.assertEqual(self.engine.state.round, 1)

if __name__ == "__main__":
    unittest.main()
