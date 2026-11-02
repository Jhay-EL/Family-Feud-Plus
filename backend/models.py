from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

@dataclass
class Answer:
    id: int
    index: int
    text: str
    points: int
    is_revealed: bool = False

@dataclass
class Question:
    id: int
    text: str
    answers: List[Answer] = field(default_factory=list)

@dataclass
class TeamState:
    name: str = "Team A"
    total_points: int = 0
    strikes: int = 0

@dataclass
class RoundLog:
    round_num: int
    team_a_points: int = 0
    team_b_points: int = 0
    team_a_strikes: int = 0
    team_b_strikes: int = 0

@dataclass
class FastMoneyEntry:
    answer: str = ""
    points: int = 0
    is_revealed: bool = False
    is_points_revealed: bool = False

@dataclass
class FastMoneyState:
    team_name: str = "Team A"
    timer: int = 0
    is_timer_running: bool = False
    p1_entries: List[FastMoneyEntry] = field(default_factory=lambda: [FastMoneyEntry() for _ in range(5)])
    p2_entries: List[FastMoneyEntry] = field(default_factory=lambda: [FastMoneyEntry() for _ in range(5)])
    total_points: int = 0
    winning_sound_active: bool = False

@dataclass
class GameState:
    # Match Navigation & Meta
    round: int = 1
    multiplier: int = 1
    bank_points: int = 0
    active_screen: str = "welcome"  # welcome, face_off, fast_money, about
    
    # Teams
    team_a: TeamState = field(default_factory=lambda: TeamState(name="Team A"))
    team_b: TeamState = field(default_factory=lambda: TeamState(name="Team B"))
    
    # Active Face-off Question
    active_question: Optional[Question] = None
    answers_count_visible: bool = False
    
    # Strikes & Animation Trigger
    current_strike_display: int = 0  # 0, 1, 2, 3 (triggers visual overlay)
    
    # Match History Log (R1-R4)
    match_log: List[RoundLog] = field(default_factory=list)
    
    # Fast Money State
    fast_money: FastMoneyState = field(default_factory=FastMoneyState)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
