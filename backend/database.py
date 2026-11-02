import sqlite3
import os
import sys
from typing import List, Optional, Tuple

if __package__ is None or __package__ == "":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from backend.models import Question, Answer
else:
    from .models import Question, Answer

class GameDatabase:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.db_dir = os.path.join(project_root, "db")
        self.face_off_db_path = os.path.join(self.db_dir, "Face-Off Questions.db")
        self.fast_money_db_path = os.path.join(self.db_dir, "Fast-Money Questions.db")
        self._ensure_tables()

    def _ensure_tables(self):
        """Ensures that SQLite databases and schemas exist."""
        os.makedirs(self.db_dir, exist_ok=True)
        
        # Face-Off DB
        with sqlite3.connect(self.face_off_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS face_off_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS face_off_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER NOT NULL,
                    answer TEXT NOT NULL,
                    points INTEGER NOT NULL,
                    FOREIGN KEY (question_id) REFERENCES face_off_questions (id) ON DELETE CASCADE
                )
            ''')
            conn.commit()

        # Fast-Money DB
        with sqlite3.connect(self.fast_money_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fast_money_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fast_money_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER NOT NULL,
                    answer TEXT NOT NULL,
                    points INTEGER NOT NULL,
                    FOREIGN KEY (question_id) REFERENCES fast_money_questions (id) ON DELETE CASCADE
                )
            ''')
            conn.commit()

    # --- Face-Off Queries ---

    def get_all_face_off_questions(self, custom_path: Optional[str] = None) -> List[Tuple[int, str]]:
        db_path = custom_path or self.face_off_db_path
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, question FROM face_off_questions ORDER BY id ASC")
            return cursor.fetchall()

    def get_face_off_question_by_id(self, question_id: int, custom_path: Optional[str] = None) -> Optional[Question]:
        db_path = custom_path or self.face_off_db_path
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, question FROM face_off_questions WHERE id = ?", (question_id,))
            q_row = cursor.fetchone()
            if not q_row:
                return None
            
            cursor.execute(
                "SELECT id, answer, points FROM face_off_answers WHERE question_id = ? ORDER BY points DESC, id ASC",
                (question_id,)
            )
            ans_rows = cursor.fetchall()
            answers = [
                Answer(id=row[0], index=idx + 1, text=row[1], points=row[2], is_revealed=False)
                for idx, row in enumerate(ans_rows)
            ]
            return Question(id=q_row[0], text=q_row[1], answers=answers)

    def save_face_off_question(self, question_text: str, answers: List[Tuple[str, int]], question_id: Optional[int] = None) -> int:
        with sqlite3.connect(self.face_off_db_path) as conn:
            cursor = conn.cursor()
            if question_id:
                cursor.execute("UPDATE face_off_questions SET question = ? WHERE id = ?", (question_text, question_id))
                cursor.execute("DELETE FROM face_off_answers WHERE question_id = ?", (question_id,))
                q_id = question_id
            else:
                cursor.execute("INSERT INTO face_off_questions (question) VALUES (?)", (question_text,))
                q_id = cursor.lastrowid

            for ans_text, points in answers:
                if ans_text.strip():
                    cursor.execute(
                        "INSERT INTO face_off_answers (question_id, answer, points) VALUES (?, ?, ?)",
                        (q_id, ans_text.strip(), points)
                    )
            conn.commit()
            return q_id

    def delete_face_off_question(self, question_id: int) -> bool:
        with sqlite3.connect(self.face_off_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM face_off_answers WHERE question_id = ?", (question_id,))
            cursor.execute("DELETE FROM face_off_questions WHERE id = ?", (question_id,))
            conn.commit()
            return cursor.rowcount > 0

    # --- Fast-Money Queries ---

    def get_all_fast_money_questions(self, custom_path: Optional[str] = None) -> List[Tuple[int, str]]:
        db_path = custom_path or self.fast_money_db_path
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, question FROM fast_money_questions ORDER BY id ASC")
            return cursor.fetchall()

    def get_fast_money_question_by_id(self, question_id: int, custom_path: Optional[str] = None) -> Optional[Question]:
        db_path = custom_path or self.fast_money_db_path
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, question FROM fast_money_questions WHERE id = ?", (question_id,))
            q_row = cursor.fetchone()
            if not q_row:
                return None
            
            cursor.execute(
                "SELECT id, answer, points FROM fast_money_answers WHERE question_id = ? ORDER BY points DESC, id ASC",
                (question_id,)
            )
            ans_rows = cursor.fetchall()
            answers = [
                Answer(id=row[0], index=idx + 1, text=row[1], points=row[2], is_revealed=False)
                for idx, row in enumerate(ans_rows)
            ]
            return Question(id=q_row[0], text=q_row[1], answers=answers)
