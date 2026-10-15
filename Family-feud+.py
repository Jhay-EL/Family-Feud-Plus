import sqlite3
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QTabWidget,
    QMainWindow,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QTextEdit,
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QFont, QGuiApplication, QIcon, QIntValidator
from PyQt5.QtCore import Qt, QSize, QTimer, QUrl
import sys
from ui_adjustments import adjust_ui_elements 
import psutil
import shutil
import os
import json
from gui_setup import setup_gui  
from Face_off_window import FaceOff_Window  
import logging

class FamilyFeud_ControlPanel(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.edit_mode = False
        
        self.setWindowTitle("Family Feud+")
        self.setWindowIcon(QIcon("res/mipmap/icon.png"))
        self.setStyleSheet("QMainWindow { background-color: #ffffff; }")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.family_feud_game_tab = QTabWidget(self.central_widget)
        
        self.title_screen_window = None
        self.face_off_window = None
        self.fast_money_window = None

        self.manual_add_style = """
            background-color: #efefef;
            color: #000000;
            border: 1px solid #c8c8c8;
            border-radius: 5px;
            padding: 5px;
            font-family: Arial;
            font-size: 12px;
        """
        
        self.modify_style = """
            background-color: #efefef;
            color: #000000;
            border: 1px solid #ea7620;
            border-radius: 5px;
            padding: 5px;
            font-family: Arial;
            font-size: 12px;
        """

        setup_gui(self, parent)

        self.auto_load_database()
        self.auto_load_fm_database()

        self.deploy.titleScreen.btn.clicked.connect(self.open_title_screen)
        self.deploy.faceOff.btn.clicked.connect(self.open_face_off_window)
        self.deploy.fastMoney.btn.clicked.connect(self.open_fast_money_window)
        self.game.mechanics.btn.clicked.connect(lambda: self.family.feud.game.tab.setCurrentIndex(3))

        self.resize(1280, 720)
        self.setMinimumSize(QSize(1280, 720))
        
        self.statusBar().showMessage("Ready")

        self.save_btn.setEnabled(False)
        
        self.setup_timer()
        self.answer_sound_player = QMediaPlayer()

#        self.cpu_timer = QTimer(self)
#        self.cpu_timer.timeout.connect(self.update_cpu_usage)
#        self.cpu_timer.start(1000)

        self.show_answers_count_btn.clicked.connect(self.show_answers_count)
        self.clear_answers_count_btn.clicked.connect(self.clear_answers_count)

        self.setup_answer_buttons()
        self.setup_reward_buttons()
        self.setup_strike_buttons()

        self.setup_points_mirroring()
 
        self.setup_round_logging()

        self.clear_log_btn.clicked.connect(self.clear_log)

        self.game_questions_input.textChanged.connect(self.update_modify_button_state)
        
        self.modify_btn.setEnabled(False)

        self.winning_sound_active = False
        self.winning_sound_btn.setEnabled(False)

        self.last_selected_fm_item = None
        self.is_fm_displayed = False

        self.setup_fm_timer()

        for i in range(1, 6):
            # Round 1 buttons
            getattr(self, f'fm_R1Ans{i}_btn').clicked.connect(
                lambda checked, r=1, n=i: self.display_fm_answer(r, n)
            )
            getattr(self, f'fm_R1Point{i}_btn').clicked.connect(
                lambda checked, r=1, n=i: self.display_fm_point(r, n)
            )
            
            # Round 2 buttons
            getattr(self, f'fm_R2Ans{i}_btn').clicked.connect(
                lambda checked, r=2, n=i: self.display_fm_answer(r, n)
            )
            getattr(self, f'fm_R2Point{i}_btn').clicked.connect(
                lambda checked, r=2, n=i: self.display_fm_point(r, n)
            )

        for i in range(1, 6):
            # Round 1 point inputs
            r1_point_input = getattr(self, f'fm_R1Point{i}_input')
            r1_point_input.setValidator(QIntValidator(1, 100, self))  # Accept 1-100
            r1_point_input.setFont(QFont("Arial", 11))
            
            # Round 2 point inputs
            r2_point_input = getattr(self, f'fm_R2Point{i}_input')
            r2_point_input.setValidator(QIntValidator(1, 100, self))  # Accept 1-100
            r2_point_input.setFont(QFont("Arial", 11))

        self.initialize_fm_buttons_state()

        for i in range(1, 6):
            # Round 1 connections
            getattr(self, f'fm_R1Ans{i}_input').textChanged.connect(self.update_fm_answer_buttons_state)
            getattr(self, f'fm_R1Point{i}_input').textChanged.connect(self.update_fm_answer_buttons_state)
            
            # Round 2 connections
            getattr(self, f'fm_R2Ans{i}_input').textChanged.connect(self.update_fm_answer_buttons_state)
            getattr(self, f'fm_R2Point{i}_input').textChanged.connect(self.update_fm_answer_buttons_state)

#__________________< Face Off Screen - Logic________________________

        self.last_selected_item = None
        self.is_displayed = False

        self.edit_mode = False  
        self.current_question = ""  
        self.current_answers = []  
        self.current_points = []  

        self.manual_add_btn.clicked.connect(self.toggle_manual_add_btn)
        self.save_btn.clicked.connect(self.save_question_to_database)
        self.load_file_btn.clicked.connect(self.load_database_file)
        self.delete_btn.clicked.connect(self.delete_selected_question)
        self.queued_questions_listbox.itemClicked.connect(self.display_selected_question)
        self.modify_btn.clicked.connect(self.toggle_edit_mode)

        for i in range(1, 9):
            point_input = getattr(self, f'point{i}_input')
            point_input.textChanged.connect(self.update_total_points)

        self.setup_fm_winning_sound_button()

#__________________Face Off Screen - Logic >________________________

    def resizeEvent(self, event):
        adjust_ui_elements(self)
        super().resizeEvent(event)

#__________________< Welcome Screen________________________

    def open_title_screen(self):
        """Opens the TitleScreen window when the button is clicked"""
        from TitleScreen_window import TitleScreen
        
        # Close other windows
        if self.face_off_window and self.face_off_window.isVisible():
            self.face_off_window.close()
        if self.fast_money_window and self.fast_money_window.isVisible():
            self.fast_money_window.close()
        
        if self.title_screen_window and self.title_screen_window.isVisible():
            self.title_screen_window.close()
        else:
            self.title_screen_window = TitleScreen()
            selected_index = self.display.selection.comboBox.currentIndex() - 1
            if selected_index >= 0:
                screen = QGuiApplication.screens()[selected_index]
                self.title_screen_window.setGeometry(screen.geometry())
            self.title_screen_window.showFullScreen()
    
    def open_face_off_window(self):
        """Opens the FaceOff window when the button is clicked"""
        # Close other windows
        if self.title_screen_window and self.title_screen_window.isVisible():
            self.title_screen_window.close()
        if self.fast_money_window and self.fast_money_window.isVisible():
            self.fast_money_window.close()
        
        if self.face_off_window and self.face_off_window.isVisible():
            self.face_off_window.close()
        else:
            self.face_off_window = FaceOff_Window()
            # Set initial team names
            self.face_off_window.gw_TeamAName.setText(self.team_A_name_input.text())
            self.face_off_window.gw_TeamBName.setText(self.team_B_name_input.text())
            # Connect text changes to update labels
            self.team_A_name_input.textChanged.connect(self.face_off_window.gw_TeamAName.setText)
            self.team_B_name_input.textChanged.connect(self.face_off_window.gw_TeamBName.setText)
            
            selected_index = self.display.selection.comboBox.currentIndex() - 1
            if selected_index >= 0:
                screen = QGuiApplication.screens()[selected_index]
                self.face_off_window.setGeometry(screen.geometry())
            self.face_off_window.showFullScreen()

    def open_fast_money_window(self):
        """Opens the Fast Money window when the button is clicked"""
        from Fast_Money_window import FastMoneyWindow
        
        # Close other windows
        if self.title_screen_window and self.title_screen_window.isVisible():
            self.title_screen_window.close()
        if self.face_off_window and self.face_off_window.isVisible():
            self.face_off_window.close()
        
        if self.fast_money_window and self.fast_money_window.isVisible():
            self.fast_money_window.close()
        else:
            self.fast_money_window = FastMoneyWindow()
            selected_index = self.display.selection.comboBox.currentIndex() - 1
            if selected_index >= 0:
                screen = QGuiApplication.screens()[selected_index]
                self.fast_money_window.setGeometry(screen.geometry())
            self.fast_money_window.showFullScreen()

    def populate_display_comboBox(self):
        """
        Detects all connected monitors and populates the ComboBox with their names.
        """
        # Get the list of connected screens
        screens = QGuiApplication.screens()
        
        # Check if there are multiple screens
        if len(screens) > 1:
            for index, screen in enumerate(screens, start=1):
                screen_name = screen.name()
                self.display.selection.comboBox.addItem(f"Monitor {index}: {screen_name}")
        elif len(screens) == 1:
            screen_name = screens[0].name()
            self.display.selection.comboBox.addItem(f"Monitor 1: {screen_name}")
        else:
            self.display.selection.comboBox.addItem("No monitors detected")

    def force_quit(self):
        QApplication.quit()

#    def update_cpu_usage(self):
#       cpu_usage = psutil.cpu_percent(interval=0)
#       self.statusBar().showMessage(f"CPU Usage: {cpu_usage}%")

#__________________Face Off Questions - Logic________________________

    def toggle_manual_add_btn(self):
        self.edit_mode = not self.edit_mode  # Toggle edit mode
        
        if self.edit_mode:
            # Enable save button when entering manual add mode
            self.save_btn.setEnabled(True)
            # Disable the listbox to make it read-only
            self.queued_questions_listbox.setEnabled(False)
            
            # Enable editing mode
            edit_style = """
                background-color: #efefef;
                color: #000000;
                border: 1px solid #c8c8c8;
                border-radius: 5px;
                padding: 5px;
                font-family: Arial;
                font-size: 12px;
            """
            
            # Convert game_questions_input to QLineEdit
            self.game_questions_input.setStyleSheet(edit_style)
            self.game_questions_input.setText("")
            self.game_questions_input.setReadOnly(False)
            
            # Convert point inputs
            for i in range(1, 9):
                point_input = getattr(self, f'point{i}_input')
                point_input.setStyleSheet(edit_style)
                point_input.setText("")
                point_input.setReadOnly(False)
                point_input.setValidator(QIntValidator(1, 100, self))  # Accept only numbers greater than 0
                point_input.setFont(QFont("Arial", 11))
            # Convert answer buttons to QLineEdit
            for i in range(1, 9):
                old_btn = getattr(self, f'ans{i}_btn')
                # Create new QLineEdit
                ans_input = QLineEdit(self)
                ans_input.setStyleSheet(edit_style)
                ans_input.setText("")
                ans_input.setAlignment(Qt.AlignCenter)  # Set text alignment to center
                ans_input.setFont(QFont("Arial", 11))
                
                # Copy exact geometry and parent
                ans_input.setParent(old_btn.parent())
                ans_input.setGeometry(old_btn.geometry())
                ans_input.setFixedSize(old_btn.size())  # Maintain exact size
                
                # Hide old button
                old_btn.hide()
                # Store reference to both widgets
                setattr(self, f'ans{i}_btn_original', old_btn)
                setattr(self, f'ans{i}_btn', ans_input)
                ans_input.show()
                
        else:
            # Disable save button when exiting manual add mode
            self.save_btn.setEnabled(False)
            # Re-enable the listbox
            self.queued_questions_listbox.setEnabled(True)

            # Update the last selected item to the current one
            current_item = self.queued_questions_listbox.currentItem()
            if current_item:
                self.last_selected_item = current_item  # Update last selected item
                self.display_selected_question(current_item)  # Display the selected question
            
            # Restore default mode
            # Reset game_questions_input
            self.game_questions_input.setStyleSheet("""
                background-color: #c8c8c8;
                color: #000000;
                border: 1px solid #c8c8c8;
                border-radius: 5px;
            """)
            self.game_questions_input.setReadOnly(True)
            
            # Reset point inputs
            point_style = """
                background-color: #c8c8c8;
                color: #000000;
                border: 1px solid #c8c8c8;
                border-radius: 5px;
            """
            for i in range(1, 9):
                point_input = getattr(self, f'point{i}_input')
                point_input.setStyleSheet(point_style)
                point_input.setReadOnly(True)
            
            # Restore original answer buttons
            ans_btn_style = """
                QPushButton {
                    background-color: #008f4a;
                    color: #ffffff;
                    border: none;
                    border-radius: 0px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #00a65a;
                }
                QPushButton:pressed {
                    background-color: #006f3a;
                }
            """
            for i in range(1, 9):
                # Get references to both widgets
                line_edit = getattr(self, f'ans{i}_btn')
                original_btn = getattr(self, f'ans{i}_btn_original')
                
                # Hide line edit
                line_edit.hide()
                # Show original button
                original_btn.show()
                original_btn.setStyleSheet(ans_btn_style)
                # Set button text to "Answer i"
                original_btn.setText(f"Answer {i}")
                # Restore original button reference
                setattr(self, f'ans{i}_btn', original_btn)

    def update_total_points(self):
        """
        Calculate and update the total points from all point inputs.
        Updates automatically when any point input changes.
        Shows empty string if total is 0.
        """
        try:
            total = 0
            for i in range(1, 9):
                point_input = getattr(self, f'point{i}_input')
                value = point_input.text().strip()
                if value:  # Only add if there's a value
                    try:
                        total += int(value)
                    except ValueError:
                        # Skip invalid number inputs
                        continue
            
            # Update the total points input - show empty string if total is 0
            self.total_points_input.setText("" if total == 0 else str(total))
        except Exception as e:
            self.statusBar().showMessage(f"Error calculating total: {str(e)}", 3000)

    def reset_inputs(self):
        # Reset game_questions_input
        self.game_questions_input.setText("")
        self.game_questions_input.setStyleSheet("""
            background-color: #c8c8c8;
            color: #000000;
            border: 1px solid #c8c8c8;
            border-radius: 5px;
        """)
        self.game_questions_input.setReadOnly(True)
    
        # Reset point inputs
        point_style = """
            background-color: #c8c8c8;
            color: #000000;
            border: 1px solid #c8c8c8;
            border-radius: 5px;
        """
        for i in range(1, 9):
            point_input = getattr(self, f'point{i}_input')
            point_input.setText("")
            point_input.setStyleSheet(point_style)
            point_input.setReadOnly(True)
    
        # Reset answer buttons
        ans_btn_style = """
            QPushButton {
                background-color: #008f4a;
                color: #ffffff;
                border: none;
                border-radius: 0px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #00a65a;
            }
            QPushButton:pressed {
                background-color: #006f3a;
            }
        """
        for i in range(1, 9):
            current_widget = getattr(self, f'ans{i}_btn')
            
            # Check if we're in edit mode with QLineEdit widgets
            if hasattr(self, f'ans{i}_btn_original'):
                original_btn = getattr(self, f'ans{i}_btn_original')
                
                # If current widget is QLineEdit, hide it
                if isinstance(current_widget, QLineEdit):
                    current_widget.hide()
                
                # Show and reset original button
                original_btn.show()
                original_btn.setText(f"Answer {i}")
                original_btn.setStyleSheet(ans_btn_style)
                original_btn.setEnabled(False)  # Disable by default
                # Restore original button reference
                setattr(self, f'ans{i}_btn', original_btn)
            else:
                # If not in edit mode, just reset the button
                current_widget.setText(f"Answer {i}")
                current_widget.setStyleSheet("""
                    QPushButton {
                        background-color: #c8c8c8;
                        color: #ffffff;
                        border: none;
                        border-radius: 0px;
                        padding: 5px;
                    }
                """)
                current_widget.setEnabled(False)
    
        # Reset edit mode
        self.edit_mode = False

    def save_question_to_database(self):
        # Get the current border color from game_questions_input stylesheet
        current_style = self.game_questions_input.styleSheet()
        is_edit_mode = "#ea7620" in current_style  # Check if orange border is present
        
        if not is_edit_mode:
            # Normal mode - proceed with saving new question
            # Get values from inputs
            question = self.game_questions_input.toPlainText()
            answers = []
            points = []
            
            # Collect answers and points
            for i in range(1, 9):
                answer_widget = getattr(self, f'ans{i}_btn')
                point_widget = getattr(self, f'point{i}_input')
                
                answer = answer_widget.text() if hasattr(answer_widget, 'text') else answer_widget.toPlainText()
                point = point_widget.text()
                
                if answer and point and answer != f"Answer {i}":  # Only add if both answer and point have values
                    answers.append(answer)
                    points.append(point)
        
            # Validate inputs
            if not question or not answers or not points:
                self.statusBar().showMessage("Please fill in at least one answer and point", 3000)
                return
            
            # Get the current directory and construct the database path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_dir = os.path.join(current_dir, "db")
            db_path = os.path.join(db_dir, "Face-Off Questions.db")
            
            try:
                # Create db directory if it doesn't exist
                if not os.path.exists(db_dir):
                    os.makedirs(db_dir)
                    self.statusBar().showMessage("Created database directory...", 2000)
                
                # Check if database file exists
                db_exists = os.path.exists(db_path)
                
                # Connect to database (this will create the file if it doesn't exist)
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
        
                # If database is new, show status message
                if not db_exists:
                    self.statusBar().showMessage("Creating new database file...", 2000)
        
                # Create tables if they don't exist
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS face_off_questions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        question TEXT NOT NULL
                    )
                ''')
        
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS face_off_answers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        question_id INTEGER,
                        answer TEXT NOT NULL,
                        points INTEGER NOT NULL,
                        FOREIGN KEY (question_id) REFERENCES face_off_questions (id)
                    )
                ''')
        
                # Insert question
                cursor.execute('INSERT INTO face_off_questions (question) VALUES (?)', (question,))
                question_id = cursor.lastrowid  # Get the last inserted ID
        
                # Insert answers and points
                for answer, point in zip(answers, points):
                    cursor.execute('''
                        INSERT INTO face_off_answers (question_id, answer, points)
                        VALUES (?, ?, ?)
                    ''', (question_id, answer, point))
        
                # Commit changes
                conn.commit()
        
                # Reset all inputs to default state
                self.reset_inputs()
        
                self.statusBar().showMessage("Question saved successfully!", 3000)
        
                # After successful save, disable the save button
                self.save_btn.setEnabled(False)

                # After successful save, reload and reorder questions
                try:
                    # Get all questions ordered by ID
                    cursor.execute('SELECT id FROM face_off_questions ORDER BY id')
                    questions = cursor.fetchall()
                    
                    # Clear and repopulate the listbox
                    self.queued_questions_listbox.clear()
                    
                    # Add questions with sequential numbers
                    for index, (question_id,) in enumerate(questions, 1):
                        self.queued_questions_listbox.addItem(f"Question {index}")
                        
                    # Update the database to reflect the new ordering
                    for index, (old_id,) in enumerate(questions, 1):
                        if old_id != index:
                            # Update the question ID
                            cursor.execute('UPDATE face_off_questions SET id = ? WHERE id = ?', (index, old_id))
                            # Update related answers
                            cursor.execute('UPDATE face_off_answers SET question_id = ? WHERE question_id = ?', (index, old_id))
                    
                    conn.commit()
                    
                    # Re-enable the listbox
                    self.queued_questions_listbox.setEnabled(True)

                    # Select the newly added question (last item in the list)
                    last_item = self.queued_questions_listbox.item(self.queued_questions_listbox.count() - 1)
                    if last_item:
                        self.queued_questions_listbox.setCurrentItem(last_item)
                        self.last_selected_item = last_item
                        self.is_displayed = False  # Reset display flag
                        self.display_selected_question(last_item)  # Display the newly added question
                    
                    # Reset inputs and disable save button
                    self.reset_inputs()
                    self.save_btn.setEnabled(False)
                    
                except sqlite3.Error as e:
                    self.statusBar().showMessage(f"Database error: {str(e)}", 3000)
        
            except sqlite3.Error as e:
                self.statusBar().showMessage(f"Database error: {str(e)}", 3000)
            finally:
                conn.close()
        else:
            # Re-enable necessary buttons
            self.manual_add_btn.setEnabled(True)
            self.load_file_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
            self.x2_round_btn.setEnabled(True)
            self.x3_round_btn.setEnabled(True)
            self.start_timer_btn.setEnabled(True)
            self.show_answers_count_btn.setEnabled(True)
            self.clear_answers_count_btn.setEnabled(True)

            # Edit mode - update existing question
            current_item = self.queued_questions_listbox.currentItem()
            if not current_item:
                self.statusBar().showMessage("No question selected to update", 3000)
                return
                
            # Extract question ID from list item text
            question_id = int(current_item.text().split()[1])
            
            # Get updated values
            question = self.game_questions_input.toPlainText()
            answers = []
            points = []
            
            for i in range(1, 9):
                answer_widget = getattr(self, f'ans{i}_btn')
                point_widget = getattr(self, f'point{i}_input')
                
                answer = answer_widget.text() if hasattr(answer_widget, 'text') else answer_widget.toPlainText()
                point = point_widget.text()
                
                if answer and point:
                    answers.append(answer)
                    points.append(point)
            
            try:
                # Get the current directory and construct the database path
                current_dir = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.join(current_dir, "db", "Face-Off Questions.db")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Update question
                cursor.execute('''
                    UPDATE face_off_questions 
                    SET question = ? 
                    WHERE id = ?
                ''', (question, question_id))
                
                # Delete old answers
                cursor.execute('DELETE FROM face_off_answers WHERE question_id = ?', (question_id,))
                        
                # Insert updated answers
                for answer, point in zip(answers, points):
                    cursor.execute('''
                        INSERT INTO face_off_answers (question_id, answer, points)
                        VALUES (?, ?, ?)
                    ''', (question_id, answer, point))
                
                conn.commit()
                self.statusBar().showMessage("Question updated successfully!", 3000)

                # Re-enable the listbox
                self.queued_questions_listbox.setEnabled(True)

                # Update the last selected item to the current one
                current_item = self.queued_questions_listbox.currentItem()
                if current_item:
                    self.last_selected_item = current_item  # Update last selected item

                # Optionally, you can call display_selected_question to refresh the display
                self.display_selected_question(current_item)
                
                # Reset inputs and exit edit mode
                self.reset_inputs()
                self.edit_mode = False
                
                # After successful save, disable the save button
                self.save_btn.setEnabled(False)

                # After successful update, reload and reorder questions
                try:
                    # Get all questions ordered by ID
                    cursor.execute('SELECT id FROM face_off_questions ORDER BY id')
                    questions = cursor.fetchall()
                    
                    # Clear and repopulate the listbox
                    self.queued_questions_listbox.clear()
                    
                    # Add questions with sequential numbers
                    for index, (question_id,) in enumerate(questions, 1):
                        self.queued_questions_listbox.addItem(f"Question {index}")
                        
                    # Update the database to reflect the new ordering
                    for index, (old_id,) in enumerate(questions, 1):
                        if old_id != index:
                            # Update the question ID
                            cursor.execute('UPDATE face_off_questions SET id = ? WHERE id = ?', (index, old_id))
                            # Update related answers
                            cursor.execute('UPDATE face_off_answers SET question_id = ? WHERE question_id = ?', (index, old_id))
                    
                    conn.commit()
                    
                except sqlite3.Error as e:
                    self.statusBar().showMessage(f"Database error: {str(e)}", 3000)               
            finally:
                conn.close()

    def auto_load_database(self):
        """Automatically load the default Face-Off Questions database on startup"""
        try:
            # Get the current directory and construct the database path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            default_db_path = os.path.join(current_dir, "db", "Face-Off Questions.db")
            
            # Check if database exists at default location
            if not os.path.exists(default_db_path):
                self.statusBar().showMessage("Default database not found at: db/Face-Off Questions.db", 3000)
                return
            
            # Connect to the database
            conn = sqlite3.connect(default_db_path)
            cursor = conn.cursor()
            
            # Get all questions
            cursor.execute('''
                SELECT id, question 
                FROM face_off_questions 
                ORDER BY id
            ''')
            questions = cursor.fetchall()
            
            # Clear existing items in listbox
            self.queued_questions_listbox.clear()
            
            # Add questions to the listbox
            for question_id, question in questions:
                self.queued_questions_listbox.addItem(f"Question {question_id}")
            
            self.statusBar().showMessage(f"Loaded {len(questions)} questions from default database", 3000)
            
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Database error: {str(e)}", 3000)
            logging.error(f"Database error in auto_load_database: {str(e)}")
        except Exception as e:
            self.statusBar().showMessage(f"Error loading default database: {str(e)}", 3000)
            logging.error(f"Error in auto_load_database: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def load_database_file(self):
        """Load database file from user selection"""
        try:
            # Get the current directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            default_db_dir = os.path.join(current_dir, "db")
            
            # Open file dialog starting in the default database directory
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Load Face-Off Round questions",
                default_db_dir,  # Set default directory
                "Database Files (*.db);;All Files (*)"
            )
            
            if file_path:
                # Verify if it's the correct database file
                if os.path.basename(file_path) != "Face-Off Questions.db":
                    self.statusBar().showMessage("Please select 'Face-Off Questions.db' file", 3000)
                    return
                    
                # Connect to the selected database
                conn = sqlite3.connect(file_path)
                cursor = conn.cursor()
                
                # Get all questions
                cursor.execute('''
                    SELECT id, question 
                    FROM face_off_questions 
                    ORDER BY id
                ''')
                questions = cursor.fetchall()
                
                # Clear existing items in listbox
                self.queued_questions_listbox.clear()
                
                # Add questions to the listbox
                for question_id, question in questions:
                    self.queued_questions_listbox.addItem(f"Question {question_id}")
                
                self.statusBar().showMessage(f"Loaded {len(questions)} questions successfully!", 3000)
                
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Database error: {str(e)}", 3000)
            logging.error(f"Database error in load_database_file: {str(e)}")
        except Exception as e:
            self.statusBar().showMessage(f"Error loading file: {str(e)}", 3000)
            logging.error(f"Error in load_database_file: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def delete_selected_question(self):
        current_item = self.queued_questions_listbox.currentItem()
        if not current_item:
            self.statusBar().showMessage("Please select a question to delete", 3000)
            return

        # Confirmation dialog
        reply = self.show_message_box(
            'Confirm Deletion',
            "Are you sure you want to delete this question?",
            QMessageBox.Question,
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return

        try:
            # Extract question ID from the item text
            question_id = int(current_item.text().split()[1])

            # Get the current directory and construct the database path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, "db", "Face-Off Questions.db")

            # Connect to database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Delete answers first
            cursor.execute('DELETE FROM face_off_answers WHERE question_id = ?', (question_id,))

            # Delete the question
            cursor.execute('DELETE FROM face_off_questions WHERE id = ?', (question_id,))

            # Get all remaining questions ordered by ID
            cursor.execute('SELECT id FROM face_off_questions ORDER BY id')
            questions = cursor.fetchall()
            
            # Clear and repopulate the listbox
            self.queued_questions_listbox.clear()
            
            # Add questions with sequential numbers
            for index, (old_id,) in enumerate(questions, 1):
                self.queued_questions_listbox.addItem(f"Question {index}")
                
                # Update the database to reflect the new ordering
                if old_id != index:
                    # Update the question ID
                    cursor.execute('UPDATE face_off_questions SET id = ? WHERE id = ?', (index, old_id))
                    # Update related answers
                    cursor.execute('UPDATE face_off_answers SET question_id = ? WHERE question_id = ?', (index, old_id))

            # Commit the changes
            conn.commit()

            # Clear displayed values
            self.clear_displayed_values()

            # Provide feedback
            self.statusBar().showMessage("Question deleted successfully!", 3000)

        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Database error: {str(e)}", 3000)
            print(f"Database error in delete_selected_question: {str(e)}")
        except Exception as e:
            self.statusBar().showMessage(f"Error deleting question: {str(e)}", 3000)
            print(f"Error in delete_selected_question: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()
        
    def display_selected_question(self, item):
        question_id = int(item.text().split()[1])  # Extract question ID from the item text

        if self.last_selected_item == item and self.is_displayed:
            self.clear_displayed_values()  # Clear displayed values if the same question is clicked again
            self.is_displayed = False  # Update the flag to indicate values are cleared
        else:
            # Fetch the question and answers from the database
            try:
                # Get the current directory and construct the database path
                current_dir = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.join(current_dir, "db", "Face-Off Questions.db")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Get the question
                cursor.execute('SELECT question FROM face_off_questions WHERE id = ?', (question_id,))
                question = cursor.fetchone()

                # Get the answers and points
                cursor.execute('SELECT answer, points FROM face_off_answers WHERE question_id = ?', (question_id,))
                answers = cursor.fetchall()

                # Display the question
                if question:
                    self.game_questions_input.setPlainText(question[0])  # Set the question text

                # Clear previous answers and points
                for i in range(1, 9):
                    ans_btn = getattr(self, f'ans{i}_btn')
                    point_input = getattr(self, f'point{i}_input')
                    ans_btn.setText("")  # Clear answer button text
                    point_input.setText("")  # Clear point input text
                    
                    # Set empty buttons to gray and disabled
                    ans_btn.setEnabled(False)
                    ans_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #c8c8c8;
                            color: #ffffff;
                            border: none;
                            border-radius: 0px;
                            padding: 5px;
                        }
                    """)

                # Display the answers and points
                for i, (answer, point) in enumerate(answers, start=1):
                    if i <= 8:  # Ensure we don't exceed the number of answer fields
                        ans_btn = getattr(self, f'ans{i}_btn')
                        point_input = getattr(self, f'point{i}_input')
                        ans_btn.setText(answer)  # Set answer text
                        point_input.setText(str(point))  # Set point text
                        
                        # If answer has a value, set normal button style and enable
                        if answer.strip():
                            ans_btn.setEnabled(True)
                            ans_btn.setStyleSheet("""
                                QPushButton {
                                    background-color: #008f4a;
                                    color: #ffffff;
                                    border: none;
                                    border-radius: 0px;
                                    padding: 5px;
                                }
                                QPushButton:hover {
                                    background-color: #00a65a;
                                }
                                QPushButton:pressed {
                                    background-color: #006f3a;
                                }
                            """)

                self.is_displayed = True  # Update the flag to indicate values are displayed

            except sqlite3.Error as e:
                self.statusBar().showMessage(f"Database error: {str(e)}", 5000)
            finally:
                if 'conn' in locals():
                    conn.close()

        # Update the last selected item
        self.last_selected_item = item
 
    def clear_displayed_values(self):
        """Clear all displayed values in the input fields."""
        self.game_questions_input.setPlainText("")  # Clear question input
        
        ans_btn_style = """
            QPushButton {
                background-color: #008f4a;
                color: #ffffff;
                border: none;
                border-radius: 0px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #00a65a;
            }
            QPushButton:pressed {
                background-color: #006f3a;
            }
        """
        
        for i in range(1, 9):
            ans_btn = getattr(self, f'ans{i}_btn')
            point_input = getattr(self, f'point{i}_input')
            ans_btn.setText(f"Answer {i}")
            ans_btn.setEnabled(True)  # Enable the button instead of setReadOnly
            ans_btn.setStyleSheet(ans_btn_style)  # Restore original style
            point_input.setText("")  # Clear point input text
    
    def toggle_edit_mode(self):
        # Check if a question is selected
        current_item = self.queued_questions_listbox.currentItem()
        if not current_item:
            self.statusBar().showMessage("Error, Select a question to modify", 3000)
            return

        # Check if game_questions_input is empty
        if not self.game_questions_input.toPlainText().strip():
            self.modify_btn.setEnabled(False)
            self.statusBar().showMessage("Cannot modify: No question selected", 3000)
            return
        else:
            self.modify_btn.setEnabled(True)

        self.edit_mode = not self.edit_mode  # Toggle edit mode

        if self.edit_mode:
            try:
                # Get the current directory and construct the database path
                current_dir = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.join(current_dir, "db", "Face-Off Questions.db")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Enable save button when entering edit mode
                self.save_btn.setEnabled(True)
                # Disable the listbox and other buttons
                self.queued_questions_listbox.setEnabled(False)
                self.manual_add_btn.setEnabled(False)
                self.load_file_btn.setEnabled(False)
                self.delete_btn.setEnabled(False)
                self.x2_round_btn.setEnabled(False)
                self.x3_round_btn.setEnabled(False)
                self.start_timer_btn.setEnabled(False)
                self.show_answers_count_btn.setEnabled(False)
                self.clear_answers_count_btn.setEnabled(False)
                self.clear_log_btn.setEnabled(False)
                self.log_next_round.setEnabled(False)

                # Store current values before entering edit mode
                self.current_question = self.game_questions_input.toPlainText()
                self.current_answers = [getattr(self, f'ans{i}_btn').text() for i in range(1, 9)]
                self.current_points = [getattr(self, f'point{i}_input').text() for i in range(1, 9)]

                # Enable editing mode
                edit_style = """
                    background-color: #efefef;
                    color: #000000;
                    border: 1px solid #ea7620;
                    border-radius: 5px;
                    padding: 5px;
                    font-family: Arial;
                    font-size: 12px;
                """
                
                # Convert game_questions_input to QLineEdit
                self.game_questions_input.setStyleSheet(edit_style)
                self.game_questions_input.setText(self.current_question)  # Keep the current question
                self.game_questions_input.setReadOnly(False)
                
                # Convert point inputs
                for i in range(1, 9):
                    point_input = getattr(self, f'point{i}_input')
                    point_input.setStyleSheet(edit_style)
                    point_input.setText(self.current_points[i-1])  # Keep the current point
                    point_input.setReadOnly(False)
                    point_input.setValidator(QIntValidator(1, 100, self))  # Accept only numbers greater than 0

                # Convert answer buttons to QLineEdit
                for i in range(1, 9):
                    old_btn = getattr(self, f'ans{i}_btn')
                    # Create new QLineEdit
                    ans_input = QLineEdit(self)
                    ans_input.setStyleSheet(edit_style)
                    ans_input.setText(self.current_answers[i-1])  # Keep the current answer
                    ans_input.setAlignment(Qt.AlignCenter)  # Set text alignment to center
                    
                    # Copy exact geometry and parent
                    ans_input.setParent(old_btn.parent())
                    ans_input.setGeometry(old_btn.geometry())
                    ans_input.setFixedSize(old_btn.size())  # Maintain exact size
                    
                    # Hide old button
                    old_btn.hide()
                    # Store reference to both widgets
                    setattr(self, f'ans{i}_btn_original', old_btn)
                    setattr(self, f'ans{i}_btn', ans_input)
                    ans_input.show()

            except sqlite3.Error as e:
                self.statusBar().showMessage(f"Database error: {str(e)}", 5000)
            finally:
                if 'conn' in locals():
                    conn.close()

        else:  # When exiting edit mode
            # Disable save button when exiting edit mode
            self.save_btn.setEnabled(False)
            # Re-enable the listbox and other buttons
            self.queued_questions_listbox.setEnabled(True)
            self.manual_add_btn.setEnabled(True)
            self.load_file_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
            self.x2_round_btn.setEnabled(True)
            self.x3_round_btn.setEnabled(True)
            self.start_timer_btn.setEnabled(True)
            self.show_answers_count_btn.setEnabled(True)
            self.clear_answers_count_btn.setEnabled(True)
            self.clear_log_btn.setEnabled(True)
            self.log_next_round.setEnabled(True)
            
            # Reset game_questions_input
            self.game_questions_input.setStyleSheet("""
                background-color: #c8c8c8;
                color: #000000;
                border: 1px solid #c8c8c8;
                border-radius: 5px;
                font-family: Arial;
                font-size: 12px;
            """)
            self.game_questions_input.setReadOnly(True)

            # Reset point inputs
            point_style = """
                background-color: #c8c8c8;
                color: #000000;
                border: 1px solid #c8c8c8;
                border-radius: 5px;
                font-family: Arial;
                font-size: 12px;
            """
            for i in range(1, 9):
                point_input = getattr(self, f'point{i}_input')
                point_input.setStyleSheet(point_style)
                point_input.setReadOnly(True)
            
            # Restore original answer buttons with appropriate styling
            for i in range(1, 9):
                # Get references to both widgets
                line_edit = getattr(self, f'ans{i}_btn')
                original_btn = getattr(self, f'ans{i}_btn_original')
                
                # Hide line edit
                line_edit.hide()
                # Show original button
                original_btn.show()
                
                # Set button text to the current answer
                original_btn.setText(self.current_answers[i-1])
                
                # Check if button has a value and apply appropriate style
                if not original_btn.text().strip() or original_btn.text() == f"Answer {i}":
                    # Gray style for empty buttons
                    original_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #c8c8c8;
                            color: #ffffff;
                            border: none;
                            border-radius: 0px;
                            padding: 5px;
                            font-family: Arial;
                            font-size: 12px;
                        }
                    """)
                    original_btn.setEnabled(False)
                else:
                    # Green style for buttons with values
                    original_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #008f4a;
                            color: #ffffff;
                            border: none;
                            border-radius: 0px;
                            padding: 5px;
                            font-family: Arial;
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background-color: #00a65a;
                        }
                        QPushButton:pressed {
                            background-color: #006f3a;
                        }
                    """)
                    original_btn.setEnabled(True)
                
                # Restore original button reference
                setattr(self, f'ans{i}_btn', original_btn)

    def update_modify_button_state(self):
        """Update modify button state based on game_questions_input content"""
        has_content = bool(self.game_questions_input.toPlainText().strip())
        self.modify_btn.setEnabled(has_content)

#__________________Face Off Questions Display - Logic________________________

    def show_answers_count(self):
        # Check if Face-off window exists and is visible
        if not self.face_off_window or not self.face_off_window.isVisible():
            self.show_message_box(
                "Error",
                "Please open Face-off window first",
                QMessageBox.Warning,
                QMessageBox.Ok
            )
            return

        # Check if total_points_input is empty
        if not self.total_points_input.text().strip():
            self.show_message_box(
                "Error",
                "Select a Question first",
                QMessageBox.Warning,
                QMessageBox.Ok
            )
            return

        # Count answers that have values
        answer_count = 0
        for i in range(1, 9):
            ans_btn = getattr(self, f'ans{i}_btn')
            if ans_btn.text().strip() and ans_btn.text() != f"Answer {i}":
                answer_count += 1
                # Enable all answer buttons that have values
                ans_btn.setEnabled(True)

        # Update Face-off window preview answers
        # Hide all preview answers first
        for i in range(8):
            rect = getattr(self.face_off_window, f'gw_AnsDisplay{i+1}')
            label = getattr(self.face_off_window, f'gw_AnsLabel{i+1}')
            rect.hide()
            label.hide()

        # Show only the number of answers that have values
        for i in range(answer_count):
            rect = getattr(self.face_off_window, f'gw_AnsDisplay{i+1}')
            label = getattr(self.face_off_window, f'gw_AnsLabel{i+1}')
            rect.show()
            label.show()

        # Change button style to indicate active state
        self.show_answers_count_btn.setStyleSheet("""
            QPushButton {
                background-color: #006f3a;
                color: #ffffff;
                border: 3px solid #e97523;
                border-radius: 0px;
                padding: 3px;
            }
        """)
        self.show_answers_count_btn.setText("Answers Active..")
        self.show_answers_count_btn.setEnabled(False)
        
        # Enable winning sound button when answers are shown
        self.winning_sound_btn.setEnabled(True)
        
        # Disable buttons while answers are active
        self.load_file_btn.setEnabled(False)
        self.manual_add_btn.setEnabled(False)
        self.modify_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        
        # Enable clear answers count button
        self.clear_answers_count_btn.setEnabled(True)

        self.statusBar().showMessage(f"Showing {answer_count} answer{'s' if answer_count != 1 else ''}", 3000)

    def clear_answers_count(self):
        """Clear all displayed answers and reset buttons to their default state"""
        # Hide all preview answers
        for i in range(1, 9):
            if hasattr(self.face_off_window, f'gw_AnsDisplay{i}'):
                rect = getattr(self.face_off_window, f'gw_AnsDisplay{i}')
                label = getattr(self.face_off_window, f'gw_AnsLabel{i}')
                rect.hide()
                label.hide()

        # Reset show answers count button
        self.show_answers_count_btn.setStyleSheet("""
            QPushButton {
                background-color: #008f4a;
                color: #ffffff;
                border: none;
                border-radius: 0px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #00a65a;
            }
            QPushButton:pressed {
                background-color: #006f3a;
            }
        """)
        self.show_answers_count_btn.setText("Show Answers Count")
        self.show_answers_count_btn.setEnabled(True)
        
        # Disable winning sound button when answers are cleared
        self.winning_sound_btn.setEnabled(False)
        if self.winning_sound_active:
            self.winning_sound_active = False
            self.winning_sound_btn.setStyleSheet("""
                QPushButton {
                    background-color: #008f4a;
                    color: #ffffff;
                    border: none;
                    border-radius: 0px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #00a65a;
                }
                QPushButton:pressed {
                    background-color: #006f3a;
                }
            """)
            self.winning_sound_btn.setText("Winning Sound")
        
        # Reset answer buttons to default state
        for i in range(1, 9):
            ans_btn = getattr(self, f'ans{i}_btn')
            if ans_btn.text().strip() and ans_btn.text() != f"Answer {i}":
                ans_btn.setEnabled(True)
                ans_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #008f4a;
                        color: #ffffff;
                        border: none;
                        border-radius: 0px;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #00a65a;
                    }
                    QPushButton:pressed {
                        background-color: #006f3a;
                    }
                """)
        
        # Re-enable buttons with appropriate states
        self.load_file_btn.setEnabled(True)
        self.manual_add_btn.setEnabled(True)
        
        # Only enable modify button if there's a question selected
        has_question = bool(self.game_questions_input.toPlainText().strip())
        self.modify_btn.setEnabled(has_question)
        
        # Save button should only be enabled in edit mode
        self.save_btn.setEnabled(self.edit_mode)
        
        # Delete button should only be enabled if there's a question selected
        self.delete_btn.setEnabled(has_question)
        
        # Disable clear answers count button
        self.clear_answers_count_btn.setEnabled(False)

        # Clear Face-off window elements if it exists and is visible
        if self.face_off_window and self.face_off_window.isVisible():
            try:
                # Clear points
                self.face_off_window.gw_Points.setText("")
                
                # Clear answers and points in face-off window
                for i in range(1, 9):
                    ans_label = getattr(self.face_off_window, f'gw_Ans{i}')
                    points_label = getattr(self.face_off_window, f'gw_Points{i}')
                    ans_label.setText("")
                    points_label.setText("")
                    
            except AttributeError as e:
                self.statusBar().showMessage(f"Error clearing Face-off window: {str(e)}", 3000)

        self.statusBar().showMessage("Cleared answer display", 3000)

    def setup_answer_buttons(self):
        # Connect each answer button to its reveal function
        for i in range(1, 9):
            btn = getattr(self, f'ans{i}_btn')
            btn.clicked.connect(lambda checked, num=i: self.reveal_answer(num))
    
    def reveal_answer(self, answer_num):
        # Check if total_points_input has value and Face-off window exists
        if not self.total_points_input.text().strip():
            self.show_message_box(
                "Error",
                "Select a Question first",
                QMessageBox.Warning,
                QMessageBox.Ok
            )
            return
            
        if not self.face_off_window or not self.face_off_window.isVisible():
            return

        # Check if the corresponding preview answer is visible
        gw_display = getattr(self.face_off_window, f'gw_AnsDisplay{answer_num}')
        if not gw_display.isVisible():
            self.show_message_box(
                "Error",
                "Please click 'Show Answers Count' first",
                QMessageBox.Warning,
                QMessageBox.Ok
            )
            return

        # Get the answer button and point input
        ans_btn = getattr(self, f'ans{answer_num}_btn')
        point_input = getattr(self, f'point{answer_num}_input')
        
        # Get the corresponding Face-off window elements
        gw_ans = getattr(self.face_off_window, f'gw_Ans{answer_num}')
        gw_points = getattr(self.face_off_window, f'gw_Points{answer_num}')
        gw_label = getattr(self.face_off_window, f'gw_AnsLabel{answer_num}')
        
        # Only proceed if the button has a real answer (not the default "Answer X" text)
        if ans_btn.text().strip() and ans_btn.text() != f"Answer {answer_num}":
            # Hide the preview answer (both rectangle and number)
            gw_display.hide()
            gw_label.hide()
            
            # Show the answer and points with "| " prefix for display
            gw_ans.setText(ans_btn.text())
            points_value = point_input.text()
            gw_points.setText(f"| {points_value}")
            
            # Store the original points value as a property for calculations
            setattr(gw_points, 'original_value', points_value)
            
            # Disable the button and change its color after revealing the answer
            ans_btn.setEnabled(False)
            ans_btn.setStyleSheet("""
                QPushButton {
                    background-color: #990000;
                    color: #ffffff;
                    border: none;
                    border-radius: 0px;
                    padding: 5px;
                }
            """)
            
            # Update the total points display
            self.update_total_displayed_points()
            
            # Play sound based on winning_sound_active state
            self.play_answer_sound()
            
            # Reset winning sound button if it was active
            if self.winning_sound_active:
                self.winning_sound_active = False
                self.winning_sound_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #008f4a;
                        color: #ffffff;
                        border: none;
                        border-radius: 0px;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #00a65a;
                    }
                    QPushButton:pressed {
                        background-color: #006f3a;
                    }
                """)
                self.winning_sound_btn.setText("Winning Sound")
                self.winning_sound_btn.setEnabled(True)
            
            # Update status bar
            self.statusBar().showMessage(f"Revealed answer {answer_num}", 3000)

    def update_total_displayed_points(self):
        """
        Calculate and display the sum of all revealed points in the main gw_Points label.
        """
        try:
            total_points = 0
            
            # Sum up all revealed points from gw_Points1 to gw_Points8
            for i in range(1, 9):
                points_label = getattr(self.face_off_window, f'gw_Points{i}')
                points_text = points_label.text().replace('| ', '').strip()
                
                if points_text:  # Only add if there's a value
                    try:
                        total_points += int(points_text)
                    except ValueError:
                        continue  # Skip if conversion fails
            
            # Update the main points display with only the current round's points
            self.face_off_window.gw_Points.setText(str(total_points) if total_points > 0 else "")
            
        except Exception as e:
            self.statusBar().showMessage(f"Error calculating total points: {str(e)}", 3000)
    
#__________________Face Off Points Reward - Logic________________________

    def setup_reward_buttons(self):
        """Set up reward button click handlers"""
        self.A_reward_btn.clicked.connect(self.reward_team_a)
        self.B_reward_btn.clicked.connect(self.reward_team_b)
    
    def reward_team_a(self):
        """Transfer points from gw_Points to Team A's points box with multiplier if active"""
        try:
            # Get current points from gw_Points
            current_points = self.face_off_window.gw_Points.text().strip()
            if not current_points:
                self.show_message_box(
                    "Error", 
                    "No points available to reward/steal",
                    QMessageBox.Warning,
                    QMessageBox.Ok
                )
                return

            # Convert points to integer
            points = int(current_points)
            
            # Check for multipliers
            x2_active = "#e97523" in self.x2_round_btn.styleSheet()
            x3_active = "#e97523" in self.x3_round_btn.styleSheet()
            
            # Apply multiplier if active
            if x3_active:
                points *= 3
            elif x2_active:
                points *= 2
            
            # Get current points from Team A's box
            current_team_points = self.points_box_A.text().strip()
            team_points = int(current_team_points) if current_team_points else 0
            
            # Add new points to existing points
            total_points = team_points + points
            
            # Update Team A's points box (this will automatically update gw_TeamAPoints)
            self.points_box_A.setText(str(total_points))
            
            # Clear all individual answer points and the total
            for i in range(1, 9):
                points_label = getattr(self.face_off_window, f'gw_Points{i}')
                points_label.setText("")
                ans_label = getattr(self.face_off_window, f'gw_Ans{i}')
                ans_label.setText("")

            self.face_off_window.gw_Points.setText("")
            
            # Reset multiplier buttons
            self.x2_round_btn.setStyleSheet("""
                QPushButton {
                    background-color: #008f4a;
                    color: #ffffff;
                    border: none;
                    border-radius: 2px;
                    padding: 3px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background-color: #00a65a;
                }
                QPushButton:pressed {
                    background-color: #006f3a;
                }
            """)
            self.x3_round_btn.setStyleSheet("""
                QPushButton {
                    background-color: #008f4a;
                    color: #ffffff;
                    border: none;
                    border-radius: 0px;
                    padding: 3px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background-color: #00a65a;
                }
                QPushButton:pressed {
                    background-color: #006f3a;
                }
            """)
            
            # Update status bar with multiplier info
            multiplier_text = " (x3)" if x3_active else " (x2)" if x2_active else ""
            self.statusBar().showMessage(f"Awarded {points}{multiplier_text} points to Team A", 3000)
            
        except ValueError as e:
            self.show_message_box(
                "Error",
                "Invalid point value",
                QMessageBox.Warning,
                QMessageBox.Ok
            )
        except Exception as e:
            self.statusBar().showMessage(f"Error rewarding points: {str(e)}", 3000)

    def reward_team_b(self):
        """Transfer points from gw_Points to Team B's points box with multiplier if active"""
        try:
            # Get current points from gw_Points
            current_points = self.face_off_window.gw_Points.text().strip()
            if not current_points:
                self.show_message_box(
                    "Error",
                    "No points available to reward/steal",
                    QMessageBox.Warning,
                    QMessageBox.Ok
                )
                return

            # Convert points to integer
            points = int(current_points)
            
            # Check for multipliers
            x2_active = "#e97523" in self.x2_round_btn.styleSheet()
            x3_active = "#e97523" in self.x3_round_btn.styleSheet()
            
            # Apply multiplier if active
            if x3_active:
                points *= 3
            elif x2_active:
                points *= 2
            
            # Get current points from Team B's box
            current_team_points = self.points_box_B.text().strip()
            team_points = int(current_team_points) if current_team_points else 0
            
            # Add new points to existing points
            total_points = team_points + points
            
            # Update Team B's points box (this will automatically update gw_TeamBPoints)
            self.points_box_B.setText(str(total_points))
            
            # Clear all individual answer points and the total
            for i in range(1, 9):
                points_label = getattr(self.face_off_window, f'gw_Points{i}')
                points_label.setText("")
                ans_label = getattr(self.face_off_window, f'gw_Ans{i}')
                ans_label.setText("")
                
            self.face_off_window.gw_Points.setText("")
            
            # Reset multiplier buttons
            self.x2_round_btn.setStyleSheet("""
                QPushButton {
                    background-color: #008f4a;
                    color: #ffffff;
                    border: none;
                    border-radius: 2px;
                    padding: 3px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background-color: #00a65a;
                }
                QPushButton:pressed {
                    background-color: #006f3a;
                }
            """)
            self.x3_round_btn.setStyleSheet("""
                QPushButton {
                    background-color: #008f4a;
                    color: #ffffff;
                    border: none;
                    border-radius: 0px;
                    padding: 3px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background-color: #00a65a;
                }
                QPushButton:pressed {
                    background-color: #006f3a;
                }
            """)
            
            # Update status bar with multiplier info
            multiplier_text = " (x3)" if x3_active else " (x2)" if x2_active else ""
            self.statusBar().showMessage(f"Awarded {points}{multiplier_text} points to Team B", 3000)
            
        except ValueError as e:
            self.show_message_box(
                "Error",
                "Invalid point value",
                QMessageBox.Warning,
                QMessageBox.Ok
            )
        except Exception as e:
            self.statusBar().showMessage(f"Error rewarding points: {str(e)}", 3000)

    def setup_points_mirroring(self):
        """Set up the mirroring of points between control panel and game window"""
        # Connect the points boxes to update the game window labels
        self.points_box_A.textChanged.connect(self.update_team_a_points_display)
        self.points_box_B.textChanged.connect(self.update_team_b_points_display)
    
    def update_team_a_points_display(self, value):
        """Update Team A's points display in the game window"""
        if self.face_off_window and self.face_off_window.isVisible():
            self.face_off_window.gw_TeamAPoints.setText(value)
    
    def update_team_b_points_display(self, value):
        """Update Team B's points display in the game window"""
        if self.face_off_window and self.face_off_window.isVisible():
            self.face_off_window.gw_TeamBPoints.setText(value)

#__________________Strike Logic________________________

    def setup_strike_buttons(self):
        """Set up strike button click handlers"""
        self.A_strike_btn.clicked.connect(self.add_strike_team_a)
        self.B_strike_btn.clicked.connect(self.add_strike_team_b)
        
        # Add QTimer for X image display
        self.x_timer = QTimer(self)
        self.x_timer.timeout.connect(self.hide_x_images)
        self.x_timer.setSingleShot(True)

    def hide_x_images(self):
        """Hide all X images"""
        if self.face_off_window and self.face_off_window.isVisible():
            self.face_off_window.gw_XImage.hide()
            self.face_off_window.gw_XXImage.hide()
            self.face_off_window.gw_XXXImage.hide()

    def show_strike_image(self, strikes):
        """Show appropriate X image based on number of strikes"""
        if not self.face_off_window or not self.face_off_window.isVisible():
            return
        
        # First hide all X images
        self.hide_x_images()
        
        # Show appropriate X image based on strikes and raise it to the top
        if strikes == 1:
            self.face_off_window.gw_XImage.show()
            self.face_off_window.gw_XImage.raise_()  # Bring to front
        elif strikes == 2:
            self.face_off_window.gw_XXImage.show()
            self.face_off_window.gw_XXImage.raise_()  # Bring to front
        elif strikes >= 3:
            self.face_off_window.gw_XXXImage.show()
            self.face_off_window.gw_XXXImage.raise_()  # Bring to front
        
        # Start timer to hide the image after 3 seconds
        self.x_timer.start(3000)

    def add_strike_team_a(self):
        """Add strike for Team A up to a maximum of 3"""
        try:
            # Get current strikes
            current_strikes = self.strike_box_A.text().strip()
            strikes = int(current_strikes) if current_strikes else 0
            
            # Only increment if less than 3
            if strikes < 3:
                strikes += 1
                self.strike_box_A.setText(str(strikes))
                
                # Show appropriate X image
                self.show_strike_image(strikes)
                
                # Update status bar with appropriate message
                if strikes == 3:
                    self.statusBar().showMessage("Team A: Maximum strikes reached!", 3000)
                else:
                    self.statusBar().showMessage(f"Team A: Strike {strikes} added", 3000)
            else:
                # Show XXX image even when at maximum strikes
                self.show_strike_image(strikes)
                
                self.show_message_box(
                    "Maximum Strikes",
                    "Team A already has 3 strikes",
                    QMessageBox.Warning,
                    QMessageBox.Ok
                )
                
        except Exception as e:
            self.statusBar().showMessage(f"Error adding strike: {str(e)}", 3000)
    
    def add_strike_team_b(self):
        """Add strike for Team B up to a maximum of 3"""
        try:
            # Get current strikes
            current_strikes = self.strike_box_B.text().strip()
            strikes = int(current_strikes) if current_strikes else 0
            
            # Only increment if less than 3
            if strikes < 3:
                strikes += 1
                self.strike_box_B.setText(str(strikes))
                
                # Show appropriate X image
                self.show_strike_image(strikes)
                
                # Update status bar with appropriate message
                if strikes == 3:
                    self.statusBar().showMessage("Team B: Maximum strikes reached!", 3000)
                else:
                    self.statusBar().showMessage(f"Team B: Strike {strikes} added", 3000)
            else:
                # Show XXX image even when at maximum strikes
                self.show_strike_image(strikes)
                
                self.show_message_box(
                    "Maximum Strikes",
                    "Team B already has 3 strikes",
                    QMessageBox.Warning,
                    QMessageBox.Ok
                )
                
        except Exception as e:
            self.statusBar().showMessage(f"Error adding strike: {str(e)}", 3000)

#__________________Log game points and strikes Logic________________________

    def setup_round_logging(self):
        """Set up round logging button handler"""
        self.log_next_round.clicked.connect(self.log_round_points_and_strikes)
    
    def log_round_points_and_strikes(self):
        """Log the current round points and strikes to the next available round boxes"""
        try:
            # Find the next empty round
            for round_num in range(1, 5):
                # Check if the current round boxes are empty
                a_points_box = getattr(self, f'A_round{round_num}_points_box')
                b_points_box = getattr(self, f'B_round{round_num}_points_box')
                a_strike_box = getattr(self, f'A_round{round_num}_strike_box')
                b_strike_box = getattr(self, f'B_round{round_num}_strike_box')
                
                if not a_points_box.text() and not b_points_box.text():
                    # Calculate points gained in this round
                    prev_round = round_num - 1
                    prev_a_total = 0
                    prev_b_total = 0
                    
                    # Get total points from previous round
                    if prev_round > 0:
                        prev_a_box = getattr(self, f'A_round{prev_round}_points_box')
                        prev_b_box = getattr(self, f'B_round{prev_round}_points_box')
                        prev_a_total = int(prev_a_box.text()) if prev_a_box.text() else 0
                        prev_b_total = int(prev_b_box.text()) if prev_b_box.text() else 0
                    
                    # Calculate points gained this round
                    current_a_total = int(self.points_box_A.text()) if self.points_box_A.text() else 0
                    current_b_total = int(self.points_box_B.text()) if self.points_box_B.text() else 0
                    
                    points_gained_a = current_a_total - prev_a_total
                    points_gained_b = current_b_total - prev_b_total
                    
                    # Log only the points gained this round
                    a_points_box.setText(str(points_gained_a) if points_gained_a > 0 else "")
                    b_points_box.setText(str(points_gained_b) if points_gained_b > 0 else "")
                    a_strike_box.setText(self.strike_box_A.text())
                    b_strike_box.setText(self.strike_box_B.text())
                    
                    # Reset strike boxes
                    self.strike_box_A.setText("")
                    self.strike_box_B.setText("")
                    
                    # Reset show_answers_count_btn to default state
                    self.show_answers_count_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #008f4a;
                            color: #ffffff;
                            border: none;
                            border-radius: 0px;
                            padding: 3px;
                        }
                        QPushButton:hover {
                            background-color: #00a65a;
                        }
                        QPushButton:pressed {
                            background-color: #006f3a;
                        }
                    """)
                    self.show_answers_count_btn.setText("Show Answers Count")
                    self.show_answers_count_btn.setEnabled(True)

                    # Reset winning sound button
                    self.winning_sound_btn.setEnabled(False)
                    if self.winning_sound_active:
                        self.winning_sound_active = False
                        self.winning_sound_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #008f4a;
                                color: #ffffff;
                                border: none;
                                border-radius: 0px;
                                padding: 5px;
                            }
                            QPushButton:hover {
                                background-color: #00a65a;
                            }
                            QPushButton:pressed {
                                background-color: #006f3a;
                            }
                        """)
                        self.winning_sound_btn.setText("Winning Sound")
                    
                    # Reset multiplier buttons
                    self.x2_round_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #008f4a;
                            color: #ffffff;
                            border: none;
                            border-radius: 2px;
                            padding: 3px;
                            font-weight: normal;
                        }
                        QPushButton:hover {
                            background-color: #00a65a;
                        }
                        QPushButton:pressed {
                            background-color: #006f3a;
                        }
                    """)
                    self.x3_round_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #008f4a;
                            color: #ffffff;
                            border: none;
                            border-radius: 0px;
                            padding: 3px;
                            font-weight: normal;
                        }
                        QPushButton:hover {
                            background-color: #00a65a;
                        }
                        QPushButton:pressed {
                            background-color: #006f3a;
                        }
                    """)
                    
                    # Hide X images if they're showing
                    if self.face_off_window and self.face_off_window.isVisible():
                        self.hide_x_images()
                        
                        # Clear game window answers and points
                        for i in range(1, 9):
                            ans_label = getattr(self.face_off_window, f'gw_Ans{i}')
                            points_label = getattr(self.face_off_window, f'gw_Points{i}')
                            ans_label.setText("")
                            points_label.setText("")
                        
                            # Hide all preview answers and labels
                            rect = getattr(self.face_off_window, f'gw_AnsDisplay{i}')
                            label = getattr(self.face_off_window, f'gw_AnsLabel{i}')
                            rect.hide()
                            label.hide()
                        
                        # Clear the total points display
                        self.face_off_window.gw_Points.setText("")
                    
                    # Reset all inputs
                    self.reset_inputs()
                    
                    # Re-enable all answer buttons and restore original style
                    for i in range(1, 9):
                        ans_btn = getattr(self, f'ans{i}_btn')
                        ans_btn.setEnabled(True)
                        ans_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #008f4a;
                                color: #ffffff;
                                border: none;
                                border-radius: 0px;
                                padding: 5px;
                            }
                            QPushButton:hover {
                                background-color: #00a65a;
                            }
                            QPushButton:pressed {
                                background-color: #006f3a;
                            }
                        """)
                    
                    # Clear and reset all inputs
                    self.game_questions_input.setPlainText("")
                    for i in range(1, 9):
                        ans_btn = getattr(self, f'ans{i}_btn')
                        point_input = getattr(self, f'point{i}_input')
                        ans_btn.setText(f"Answer {i}")
                        ans_btn.setEnabled(True)
                        point_input.setText("")
                    
                    # Reset total points display
                    self.total_points_input.setText("")
                    
                    self.statusBar().showMessage(f"Round {round_num} logged successfully and inputs reset", 3000)
                    return
                
            # If we get here, all rounds are filled
            self.show_message_box(
                "Maximum Rounds Reached",
                "All 4 rounds have been logged. Clear rounds to log new ones.",
                QMessageBox.Warning,
                QMessageBox.Ok
            )
                
        except Exception as e:
            self.statusBar().showMessage(f"Error logging round: {str(e)}", 3000)
            logging.error(f"Error in log_round_points_and_strikes: {e}")

#__________________Sound________________________

    def play_strike_sound(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(current_dir, "res", "sound", "strike.mp3")
            self.answer_sound_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(sound_path))
            )
            self.answer_sound_player.play()
        except Exception as e:
            print(f"Error playing sound: {str(e)}")

    def play_CorrectAnswer_sound(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(current_dir, "res", "sound", "family-feud-good-answer.mp3")
            self.answer_sound_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(sound_path))
            )
            self.answer_sound_player.play()
        except Exception as e:
            print(f"Error playing sound: {str(e)}")

    def play_FaceOff_sound(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(current_dir, "res", "sound", "face-off.mp3")
            self.answer_sound_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(sound_path))
            )
            self.answer_sound_player.play()
        except Exception as e:
            print(f"Error playing sound: {str(e)}")

    def play_outro_sound(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(current_dir, "res", "sound", "winSound.mp3")
            self.answer_sound_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(sound_path))
            )
            self.answer_sound_player.play()
        except Exception as e:
            print(f"Error playing sound: {str(e)}")

    def play_intro_sound(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(current_dir, "res", "sound", "family-feud-returning-from-commercial.mp3")
            self.answer_sound_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(sound_path))
            )
            self.answer_sound_player.play()
        except Exception as e:
            print(f"Error playing sound: {str(e)}")

    def play_strike_sound(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(current_dir, "res", "sound", "strike.mp3")
            self.answer_sound_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(sound_path))
            )
            self.answer_sound_player.play()
        except Exception as e:
            print(f"Error playing sound: {str(e)}")

    def play_answer_sound(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(current_dir, "res", "sound", "family-feud-good-answer.mp3")
            self.answer_sound_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(sound_path))
            )
            self.answer_sound_player.play()
        except Exception as e:
            print(f"Error playing sound: {str(e)}")

    def play_ShowAnswerCount_sound(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(current_dir, "res", "sound", "FMSound1.mp3")
            self.answer_sound_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(sound_path))
            )
            self.answer_sound_player.play()
        except Exception as e:
            print(f"Error playing sound: {str(e)}")

    def setup_winning_sound_button(self):
        """Setup winning sound button and its state"""
        self.winning_sound_btn = QPushButton("Winning Sound", self)
        self.winning_sound_btn.setStyleSheet("""
            QPushButton {
                background-color: #008f4a;
                color: #ffffff;
                border: none;
                border-radius: 0px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #00a65a;
            }
            QPushButton:pressed {
                background-color: #006f3a;
            }
        """)
        self.winning_sound_btn.clicked.connect(self.activate_winning_sound)
        self.winning_sound_active = False
        self.winning_sound_btn.setEnabled(False)  # Disabled at startup
    
    def toggle_winning_sound(self):
        """Toggle winning sound state"""
        self.winning_sound_active = not self.winning_sound_active
        if self.winning_sound_active:
            # Change button style to indicate active state
            self.winning_sound_btn.setStyleSheet("""
                QPushButton {
                    background-color: #006f3a;
                    color: #ffffff;
                    border: 3px solid #e97523;
                    border-radius: 0px;
                    padding: 3px;
                }
            """)
            self.winning_sound_btn.setText("Winning Sound Active..")
            self.winning_sound_btn.setEnabled(False)
            self.statusBar().showMessage("Winning sound activated", 3000)
        else:
            # Reset button style
            self.winning_sound_btn.setStyleSheet("""
                QPushButton {
                    background-color: #008f4a;
                    color: #ffffff;
                    border: none;
                    border-radius: 0px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #00a65a;
                }
                QPushButton:pressed {
                    background-color: #006f3a;
                }
            """)
            self.winning_sound_btn.setText("Winning Sound")
            self.winning_sound_btn.setEnabled(True)
    
    def play_answer_sound(self):
        """Play appropriate sound based on winning_sound_active state"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            if self.winning_sound_active:
                sound_path = os.path.join(current_dir, "res", "sound", "win-answer.mp3")
            else:
                sound_path = os.path.join(current_dir, "res", "sound", "family-feud-good-answer.mp3")
            
            if os.path.exists(sound_path):  # Verify the file exists
                self.answer_sound_player.setMedia(
                    QMediaContent(QUrl.fromLocalFile(sound_path))
                )
                self.answer_sound_player.play()
            else:
                logging.error(f"Sound file not found: {sound_path}")
            
        except Exception as e:
            logging.error(f"Error playing sound: {str(e)}")

    def activate_winning_sound(self):
        """Activate winning sound mode"""
        self.winning_sound_active = True
        # Change button style to indicate active state (similar to show_answers_count_btn)
        self.winning_sound_btn.setStyleSheet("""
            QPushButton {
                background-color: #006f3a;
                color: #ffffff;
                border: 3px solid #e97523;
                border-radius: 0px;
                padding: 3px;
            }
        """)
        self.winning_sound_btn.setText("Winning Sound Active..")
        self.winning_sound_btn.setEnabled(False)
        self.statusBar().showMessage("Winning sound activated", 3000)
#__________________X2 and x3 Round logic________________________

    def toggle_x3_round(self):
        """Toggle X3 round button state and color with orange border when active"""
        current_style = self.x3_round_btn.styleSheet()
        
        if "#e97523" in current_style:  # Check if button is currently active/locked
            # Button is currently locked, reset to default style
            self.x3_round_btn.setStyleSheet("""
                QPushButton {
                    background-color: #008f4a;
                    color: #ffffff;
                    border: none;
                    border-radius: 0px;
                    padding: 3px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background-color: #00a65a;
                }
                QPushButton:pressed {
                    background-color: #006f3a;
                }
            """)
            self.x3_round_btn.setText("x3 Round")
            self.statusBar().showMessage("X3 Round deactivated", 3000)
        else:
            # Deactivate x2 button first
            self.x2_round_btn.setStyleSheet("""
                QPushButton {
                    background-color: #008f4a;
                    color: #ffffff;
                    border: none;
                    border-radius: 2px;
                    padding: 3px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background-color: #00a65a;
                }
                QPushButton:pressed {
                    background-color: #006f3a;
                }
            """)
            self.x2_round_btn.setText("x2 Round")
            
            # Activate x3 button
            self.x3_round_btn.setStyleSheet("""
                QPushButton {
                    background-color: #006f3a;
                    color: #ffffff;
                    border: 3px solid #e97523;
                    border-radius: 0px;
                    padding: 3px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background-color: #006f3a;
                    border: 3px solid #ea8945;
                }
            """)
            self.x3_round_btn.setText("x3 Round")
            self.statusBar().showMessage("X3 Round activated", 3000)
    
    def toggle_x2_round(self):
        """Toggle X2 round button state and color with orange border when active"""
        current_style = self.x2_round_btn.styleSheet()
        
        if "#e97523" in current_style:  # Check if button is currently active/locked
            # Button is currently locked, reset to default style
            self.x2_round_btn.setStyleSheet("""
                QPushButton {
                    background-color: #008f4a;
                    color: #ffffff;
                    border: none;
                    border-radius: 2px;
                    padding: 3px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background-color: #00a65a;
                }
                QPushButton:pressed {
                    background-color: #006f3a;
                }
            """)
            self.x2_round_btn.setText("x2 Round")
            self.statusBar().showMessage("X2 Round deactivated", 3000)
        else:
            # Deactivate x3 button first
            self.x3_round_btn.setStyleSheet("""
                QPushButton {
                    background-color: #008f4a;
                    color: #ffffff;
                    border: none;
                    border-radius: 0px;
                    padding: 3px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background-color: #00a65a;
                }
                QPushButton:pressed {
                    background-color: #006f3a;
                }
            """)
            self.x3_round_btn.setText("x3 Round")
            
            # Activate x2 button
            self.x2_round_btn.setStyleSheet("""
                QPushButton {
                    background-color: #006f3a;
                    color: #ffffff;
                    border: 3px solid #e97523;
                    border-radius: 2px;
                    padding: 3px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background-color: #006f3a;
                    border: 3px solid #ea8945;
                }
            """)
            self.x2_round_btn.setText("x2 Round")
            self.statusBar().showMessage("X2 Round activated", 3000)

#__________________Timer________________________________________

    def setup_timer(self):
        """Set up timer functionality"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = 0
        
        # Set default value to 3 seconds
        self.timer_input.setText("3")
        
        # Add validator to only accept numbers
        self.timer_input.setValidator(QIntValidator(1, 999, self))
        
        # Connect button to start_timer method
        self.start_timer_btn.clicked.connect(self.start_timer)

    def start_timer(self):
        """Start countdown timer with input value"""
        try:
            # Get time from input, default to 3 if empty
            time_str = self.timer_input.text().strip()
            if not time_str:
                time_str = "3"
                self.timer_input.setText(time_str)
            
            # Convert input to integer
            seconds = int(time_str)
            if seconds <= 0:
                seconds = 3
                self.timer_input.setText("3")
    
            # Initialize timer
            self.remaining_time = seconds
            self.timer_input.setText(str(self.remaining_time))
            
            # Change button style to indicate active timer
            self.start_timer_btn.setStyleSheet("""
                QPushButton {
                    background-color: #006f3a;
                    color: #ffffff;
                    border: 3px solid #e97523;
                    border-radius: 0px;
                    padding: 3px;
                }
            """)
            self.start_timer_btn.setText("Timer Running..")
            self.start_timer_btn.setEnabled(False)
            
            # Start timer with 1-second intervals
            self.timer.start(1000)
            
        except ValueError:
            # If any error occurs, default to 3 seconds
            self.timer_input.setText("3")
            self.remaining_time = 3
            self.timer.start(1000)

    def update_timer(self):
        """Update timer display and handle timeout"""
        self.remaining_time -= 1
        self.timer_input.setText(str(self.remaining_time))
        
        if self.remaining_time <= 0:
            # Stop timer
            self.timer.stop()
            
            # Reset timer input to 3
            self.timer_input.setText("3")
            
            # Reset button style and text
            self.start_timer_btn.setStyleSheet("""
                QPushButton {
                    background-color: #008f4a;
                    color: #ffffff;
                    border: none;
                    border-radius: 0px;
                    padding: 3px;
                }
                QPushButton:hover {
                    background-color: #00a65a;
                }
                QPushButton:pressed {
                    background-color: #006f3a;
                }
            """)
            self.start_timer_btn.setText("Start Timer")
            self.start_timer_btn.setEnabled(True)
            
            # Play timeout sound
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                sound_path = os.path.join(current_dir, "res", "sound", "FMNoPoints.mp3")
                self.answer_sound_player.setMedia(
                    QMediaContent(QUrl.fromLocalFile(sound_path))
                )
                self.answer_sound_player.play()
            except Exception as e:
                print(f"Error playing timeout sound: {str(e)}")

#__________________Reset All Button________________________________________

    def clear_log(self):
        """
        Clear all game data and reset UI elements after user confirmation.
        Includes clearing points, strikes, team names, answers, and database entries.
        """
        # Show confirmation dialog
        reply = self.show_message_box(
            "Clear Game Data",
            "This will clear all the data of the game. Do you want to continue?",
            QMessageBox.Question,
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Clear game questions input
                self.game_questions_input.setText("")
                
                # Clear points boxes
                self.points_box_A.setText("")
                self.points_box_B.setText("")
                
                # Clear strike boxes
                self.strike_box_A.setText("")
                self.strike_box_B.setText("")
                
                # Clear round points boxes for Team A
                for i in range(1, 5):
                    getattr(self, f'A_round{i}_points_box').setText("")
                    getattr(self, f'A_round{i}_strike_box').setText("")
                
                # Clear round points boxes for Team B
                for i in range(1, 5):
                    getattr(self, f'B_round{i}_points_box').setText("")
                    getattr(self, f'B_round{i}_strike_box').setText("")
                
                # Reset all answer buttons to default state
                for i in range(1, 9):
                    ans_btn = getattr(self, f'ans{i}_btn')
                    ans_btn.setText(f"Answer {i}")
                    ans_btn.setEnabled(True)
                    ans_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #008f4a;
                            color: #ffffff;
                            border: none;
                            border-radius: 0px;
                            padding: 5px;
                        }
                        QPushButton:hover {
                            background-color: #00a65a;
                        }
                        QPushButton:pressed {
                            background-color: #006f3a;
                        }
                    """)
                    
                    # Clear point inputs
                    point_input = getattr(self, f'point{i}_input')
                    point_input.setText("")
                
                # Clear Face-off window elements if it exists
                if self.face_off_window and self.face_off_window.isVisible():
                    try:
                        # Clear team names and points
                        self.face_off_window.gw_TeamAName.setText("")
                        self.face_off_window.gw_TeamBName.setText("")
                        self.face_off_window.gw_TeamAPoints.setText("")
                        self.face_off_window.gw_TeamBPoints.setText("")
                        self.face_off_window.gw_Points.setText("")
                        
                        # Clear answers and points in face-off window
                        for i in range(1, 9):
                            ans_label = getattr(self.face_off_window, f'gw_Ans{i}')
                            points_label = getattr(self.face_off_window, f'gw_Points{i}')
                            ans_label.setText("")
                            points_label.setText("")
                            
                    except AttributeError as e:
                        self.statusBar().showMessage(f"Error clearing Face-off window: {str(e)}", 3000)
                
                # Reset show answers count button if it's active
                if hasattr(self, 'show_answers_count_btn'):
                    self.show_answers_count_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #008f4a;
                            color: #ffffff;
                            border: none;
                            border-radius: 0px;
                            padding: 3px;
                        }
                        QPushButton:hover {
                            background-color: #00a65a;
                        }
                        QPushButton:pressed {
                            background-color: #006f3a;
                        }
                    """)
                    self.show_answers_count_btn.setText("Show Answers Count")
                    self.show_answers_count_btn.setEnabled(True)
                
                # Call clear_answers_count to reset the preview answers
                self.clear_answers_count()
                
                # Clear total points
                self.total_points_input.setText("")
                
                self.statusBar().showMessage("Game data cleared successfully", 3000)
                
            except Exception as e:
                self.statusBar().showMessage(f"Error clearing game data: {str(e)}", 3000)
                logging.error(f"Error in clear_log: {str(e)}")

################################### Fast Money Round #############################################

    def update_team_listBox(self):
        """Updates the team listBox when team names change"""
        current_index = self.team_listBox.currentIndex()
        self.team_listBox.clear()
        self.team_listBox.addItems(["Choose Team", self.team_A_name_input.text(), self.team_B_name_input.text()])
        self.team_listBox.setCurrentIndex(current_index)

    def toggle_fm_edit_mode(self, button_clicked):
        """Toggle edit mode for Fast Money inputs based on which button was clicked"""
        
        readonly_style = """
            background-color: #c8c8c8;
            color: #000000;
            border: 1px solid #c8c8c8;
            border-radius: 5px;
        """
        
        # Get all input fields
        input_fields = [
            self.fm_game_questions_input,
            self.fm_ans1_input, self.fm_ans2_input, self.fm_ans3_input, 
            self.fm_ans4_input, self.fm_ans5_input,
            self.fm_point1_input, self.fm_point2_input, self.fm_point3_input,
            self.fm_point4_input, self.fm_point5_input
        ]
        
        # Handle Manual Add button
        if button_clicked == self.fm_manual_add_questions_btn:
            is_readonly = not input_fields[0].isReadOnly()  # Check current state
            for field in input_fields:
                if is_readonly:  # If currently editable, make readonly
                    field.setReadOnly(True)
                    field.setStyleSheet(readonly_style)
                    field.setFont(QFont("Arial", 10))
                    field.setText("")
                else:  # If currently readonly, make editable
                    field.setReadOnly(False)
                    field.setStyleSheet(self.manual_add_style)
                    field.setText("")
        
        # Handle Modify button
        elif button_clicked == self.fm_mod_btn:
            is_readonly = not input_fields[0].isReadOnly()  # Check current state
            for field in input_fields:
                if is_readonly:  # If currently editable, make readonly
                    field.setReadOnly(True)
                    field.setStyleSheet(readonly_style)
                    field.setFont(QFont("Arial", 10))
                else:  # If currently readonly, make editable
                    field.setReadOnly(False)
                    field.setStyleSheet(self.modify_style)

    def save_fm_question_to_database(self):
        # Get the current border color from fm_game_questions_input stylesheet
        current_style = self.fm_game_questions_input.styleSheet()
        
        # Define default readonly style
        readonly_style = """
            background-color: #c8c8c8;
            color: #000000;
            border: 1px solid #c8c8c8;
            border-radius: 5px;
        """
        
        # Get values from inputs
        question = self.fm_game_questions_input.toPlainText()
        answers = []
        points = []
        
        # Collect answers and points
        for i in range(1, 6):
            answer_input = getattr(self, f'fm_ans{i}_input')
            point_input = getattr(self, f'fm_point{i}_input')
            
            answer = answer_input.text()
            point = point_input.text()
            
            if answer and point:
                answers.append(answer)
                points.append(point)

        # Validate inputs
        if not question or not answers or not points:
            self.statusBar().showMessage("Please fill in at least one answer and point", 3000)
            return
        
        # Get the current directory and construct the database path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir = os.path.join(current_dir, "db")
        db_path = os.path.join(db_dir, "Fast-Money Questions.db")
        
        try:
            # Create db directory if it doesn't exist
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
                self.statusBar().showMessage("Created database directory...", 2000)
            
            # Check if database file exists
            db_exists = os.path.exists(db_path)
            
            # Connect to database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
    
            # If database is new, show status message
            if not db_exists:
                self.statusBar().showMessage("Creating new database file...", 2000)
    
            # Create tables if they don't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fast_money_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL
                )
            ''')
    
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fast_money_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER,
                    answer TEXT NOT NULL,
                    points INTEGER NOT NULL,
                    FOREIGN KEY (question_id) REFERENCES fast_money_questions (id)
                )
            ''')
    
            # Insert question
            cursor.execute('INSERT INTO fast_money_questions (question) VALUES (?)', (question,))
            question_id = cursor.lastrowid
    
            # Insert answers and points
            for answer, point in zip(answers, points):
                cursor.execute('''
                    INSERT INTO fast_money_answers (question_id, answer, points)
                    VALUES (?, ?, ?)
                ''', (question_id, answer, point))
    
            # Commit changes
            conn.commit()
    
            # After successful save, reset all inputs to default state
            # Reset content
            self.fm_game_questions_input.clear()
            for i in range(1, 6):
                getattr(self, f'fm_ans{i}_input').clear()
                getattr(self, f'fm_point{i}_input').clear()
            
            # Reset to readonly and default style
            self.fm_game_questions_input.setReadOnly(True)
            self.fm_game_questions_input.setStyleSheet(readonly_style)
            self.fm_game_questions_input.setFont(QFont("Arial", 10))
            
            for i in range(1, 6):
                ans_input = getattr(self, f'fm_ans{i}_input')
                point_input = getattr(self, f'fm_point{i}_input')
                
                # Set readonly
                ans_input.setReadOnly(True)
                point_input.setReadOnly(True)
                
                # Reset style
                ans_input.setStyleSheet(readonly_style)
                point_input.setStyleSheet(readonly_style)
                
                # Reset font
                ans_input.setFont(QFont("Arial", 10))
                point_input.setFont(QFont("Arial", 10))
    
            self.statusBar().showMessage("Fast Money question saved successfully!", 3000)
    
            # Update listbox
            try:
                cursor.execute('SELECT id FROM fast_money_questions ORDER BY id')
                questions = cursor.fetchall()
                
                self.fm_queued_questions_listBox.clear()
                
                for index, (question_id,) in enumerate(questions, 1):
                    self.fm_queued_questions_listBox.addItem(f"Question {index}")
                    
                # Update database ordering
                for index, (old_id,) in enumerate(questions, 1):
                    if old_id != index:
                        cursor.execute('UPDATE fast_money_questions SET id = ? WHERE id = ?', (index, old_id))
                        cursor.execute('UPDATE fast_money_answers SET question_id = ? WHERE question_id = ?', (index, old_id))
                
                conn.commit()
                
                # Select the newly added question
                last_item = self.fm_queued_questions_listBox.item(self.fm_queued_questions_listBox.count() - 1)
                if last_item:
                    self.fm_queued_questions_listBox.setCurrentItem(last_item)
                
            except sqlite3.Error as e:
                self.statusBar().showMessage(f"Database error: {str(e)}", 3000)
    
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Database error: {str(e)}", 3000)
        finally:
            if 'conn' in locals():
                conn.close()

    def auto_load_fm_database(self):
        """Automatically load the Fast Money Questions database on startup"""
        try:
            # Get the current directory and construct the database path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            default_db_path = os.path.join(current_dir, "db", "Fast-Money Questions.db")
            
            # Check if database exists at default location
            if not os.path.exists(default_db_path):
                self.statusBar().showMessage("Fast Money database not found at: db/Fast-Money Questions.db", 3000)
                return
            
            # Connect to the database
            conn = sqlite3.connect(default_db_path)
            cursor = conn.cursor()
            
            # Get all questions
            cursor.execute('''
                SELECT id, question 
                FROM fast_money_questions 
                ORDER BY id
            ''')
            questions = cursor.fetchall()
            
            # Clear existing items in listbox
            self.fm_queued_questions_listBox.clear()
            
            # Add questions to the listbox
            for question_id, question in questions:
                self.fm_queued_questions_listBox.addItem(f"Question {question_id}")
            
            self.statusBar().showMessage(f"Loaded {len(questions)} Fast Money questions from database", 3000)
            
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Database error: {str(e)}", 3000)
            logging.error(f"Database error in auto_load_fm_database: {str(e)}")
        except Exception as e:
            self.statusBar().showMessage(f"Error loading Fast Money database: {str(e)}", 3000)
            logging.error(f"Error in auto_load_fm_database: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def display_selected_fm_question(self, item):
        """Display selected Fast Money question and its answers/points"""
        try:
            if not item:
                return
                
            question_id = int(item.text().split()[1])  # Extract question ID from the item text
        
            if self.last_selected_fm_item == item and self.is_fm_displayed:
                # Clear and reset to default if same question is clicked again
                self.clear_fm_displayed_values()
                self.is_fm_displayed = False
            else:
                try:
                    # Get the current directory and construct the database path
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    db_path = os.path.join(current_dir, "db", "Fast-Money Questions.db")
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
        
                    # Get the question
                    cursor.execute('SELECT question FROM fast_money_questions WHERE id = ?', (question_id,))
                    question = cursor.fetchone()
        
                    # Get the answers and points
                    cursor.execute('SELECT answer, points FROM fast_money_answers WHERE question_id = ? ORDER BY id', (question_id,))
                    answers = cursor.fetchall()
        
                    # Clear and reset all inputs first
                    readonly_style = """
                        background-color: #c8c8c8;
                        color: #000000;
                        border: 1px solid #c8c8c8;
                        border-radius: 5px;
                    """
                    # Display the question
                    if question:
                        self.fm_game_questions_input.setPlainText(question[0])
                        self.fm_game_questions_input.setStyleSheet(readonly_style)
                        self.fm_game_questions_input.setReadOnly(True)

                    # Clear previous answers and points
                    for i in range(1, 6):
                        ans_input = getattr(self, f'fm_ans{i}_input')
                        point_input = getattr(self, f'fm_point{i}_input')
                        
                        ans_input.clear()
                        point_input.clear()
                        
                        ans_input.setStyleSheet(readonly_style)
                        point_input.setStyleSheet(readonly_style)
                        
                        ans_input.setReadOnly(True)
                        point_input.setReadOnly(True)
                        
                        ans_input.setFont(QFont("Arial", 10))
                        point_input.setFont(QFont("Arial", 10))
        
                    # Display the answers and points
                    for i, (answer, point) in enumerate(answers, start=1):
                        if i <= 5:  # Fast Money has 5 answers max
                            ans_input = getattr(self, f'fm_ans{i}_input')
                            point_input = getattr(self, f'fm_point{i}_input')
                            
                            ans_input.setText(answer)
                            point_input.setText(str(point))
        
                    self.is_fm_displayed = True
        
                except sqlite3.Error as e:
                    self.statusBar().showMessage(f"Database error: {str(e)}", 5000)
                    logging.error(f"Database error in display_selected_fm_question: {str(e)}")
                finally:
                    if 'conn' in locals():
                        conn.close()
        
            # Update the last selected item
            self.last_selected_fm_item = item
            
        except Exception as e:
            logging.error(f"Error in display_selected_fm_question: {str(e)}")
            self.statusBar().showMessage(f"Error displaying question: {str(e)}", 5000)
    
    def clear_fm_displayed_values(self):
        """Clear and reset all Fast Money input fields to default state"""
        readonly_style = """
            background-color: #c8c8c8;
            color: #000000;
            border: 1px solid #c8c8c8;
            border-radius: 5px;
        """
    
        # Clear and reset question input
        self.fm_game_questions_input.clear()
        self.fm_game_questions_input.setStyleSheet(readonly_style)
        self.fm_game_questions_input.setReadOnly(True)
        self.fm_game_questions_input.setFont(QFont("Arial", 10))
    
        # Clear and reset all answer and point inputs
        for i in range(1, 6):
            ans_input = getattr(self, f'fm_ans{i}_input')
            point_input = getattr(self, f'fm_point{i}_input')
            
            # Clear content
            ans_input.clear()
            point_input.clear()
            
            # Reset style
            ans_input.setStyleSheet(readonly_style)
            point_input.setStyleSheet(readonly_style)
            
            # Set readonly
            ans_input.setReadOnly(True)
            point_input.setReadOnly(True)
            
            # Reset font
            ans_input.setFont(QFont("Arial", 10))
            point_input.setFont(QFont("Arial", 10))

    def load_fm_database_file(self):
        """Load Fast Money database file from user selection"""
        try:
            # Get the current directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            default_db_dir = os.path.join(current_dir, "db")
            
            # Open file dialog starting in the default database directory
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Load Fast Money Round questions",
                default_db_dir,  # Set default directory
                "Database Files (*.db);;All Files (*)"
            )
            
            if file_path:
                # Verify if it's the correct database file
                if os.path.basename(file_path) != "Fast-Money Questions.db":
                    self.statusBar().showMessage("Please select 'Fast-Money Questions.db' file", 3000)
                    return
                    
                # Connect to the selected database
                conn = sqlite3.connect(file_path)
                cursor = conn.cursor()
                
                # Get all questions
                cursor.execute('''
                    SELECT id, question 
                    FROM fast_money_questions 
                    ORDER BY id
                ''')
                questions = cursor.fetchall()
                
                # Clear existing items in listbox
                self.fm_queued_questions_listBox.clear()
                
                # Add questions to the listbox
                for question_id, question in questions:
                    self.fm_queued_questions_listBox.addItem(f"Question {question_id}")
                
                self.statusBar().showMessage(f"Loaded {len(questions)} Fast Money questions successfully!", 3000)
                
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Database error: {str(e)}", 3000)
            logging.error(f"Database error in load_fm_database_file: {str(e)}")
        except Exception as e:
            self.statusBar().showMessage(f"Error loading file: {str(e)}", 3000)
            logging.error(f"Error in load_fm_database_file: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def save_fm_modified_question(self):
        """Save modifications to an existing Fast Money question"""
        # Get the current border color from fm_game_questions_input stylesheet
        current_style = self.fm_game_questions_input.styleSheet()
        is_edit_mode = "#ea7620" in current_style  # Check if orange border is present
        
        if is_edit_mode:
            # Get current selected item
            current_item = self.fm_queued_questions_listBox.currentItem()
            if not current_item:
                self.statusBar().showMessage("No question selected to update", 3000)
                return
                
            # Extract question ID from list item text
            question_id = int(current_item.text().split()[1])
            
            # Get updated values
            question = self.fm_game_questions_input.toPlainText()
            answers = []
            points = []
            
            # Collect answers and points
            for i in range(1, 6):
                answer_input = getattr(self, f'fm_ans{i}_input')
                point_input = getattr(self, f'fm_point{i}_input')
                
                answer = answer_input.text()
                point = point_input.text()
                
                if answer and point:
                    answers.append(answer)
                    points.append(point)
            
            try:
                # Get the current directory and construct the database path
                current_dir = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.join(current_dir, "db", "Fast-Money Questions.db")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Update question
                cursor.execute('''
                    UPDATE fast_money_questions 
                    SET question = ? 
                    WHERE id = ?
                ''', (question, question_id))
                
                # Delete old answers
                cursor.execute('DELETE FROM fast_money_answers WHERE question_id = ?', (question_id,))
                        
                # Insert updated answers
                for answer, point in zip(answers, points):
                    cursor.execute('''
                        INSERT INTO fast_money_answers (question_id, answer, points)
                        VALUES (?, ?, ?)
                    ''', (question_id, answer, point))
                
                conn.commit()
                
                # Reset all inputs to default state
                readonly_style = """
                    background-color: #c8c8c8;
                    color: #000000;
                    border: 1px solid #c8c8c8;
                    border-radius: 5px;
                """
                
                # Reset content and style
                self.fm_game_questions_input.setReadOnly(True)
                self.fm_game_questions_input.setStyleSheet(readonly_style)
                self.fm_game_questions_input.setFont(QFont("Arial", 10))
                
                for i in range(1, 6):
                    ans_input = getattr(self, f'fm_ans{i}_input')
                    point_input = getattr(self, f'fm_point{i}_input')
                    
                    # Set readonly
                    ans_input.setReadOnly(True)
                    point_input.setReadOnly(True)
                    
                    # Reset style
                    ans_input.setStyleSheet(readonly_style)
                    point_input.setStyleSheet(readonly_style)
                    
                    # Reset font
                    ans_input.setFont(QFont("Arial", 10))
                    point_input.setFont(QFont("Arial", 10))
                
                self.statusBar().showMessage("Fast Money question updated successfully!", 3000)
    
                # Update the last selected item and refresh display
                if current_item:
                    self.last_selected_fm_item = current_item
                    self.display_selected_fm_question(current_item)
                
                # After successful update, reload and reorder questions
                try:
                    cursor.execute('SELECT id FROM fast_money_questions ORDER BY id')
                    questions = cursor.fetchall()
                    
                    self.fm_queued_questions_listBox.clear()
                    
                    for index, (question_id,) in enumerate(questions, 1):
                        self.fm_queued_questions_listBox.addItem(f"Question {index}")
                        
                    # Update database ordering
                    for index, (old_id,) in enumerate(questions, 1):
                        if old_id != index:
                            cursor.execute('UPDATE fast_money_questions SET id = ? WHERE id = ?', (index, old_id))
                            cursor.execute('UPDATE fast_money_answers SET question_id = ? WHERE question_id = ?', (index, old_id))
                    
                    conn.commit()
                    
                except sqlite3.Error as e:
                    self.statusBar().showMessage(f"Database error: {str(e)}", 3000)
                    
            except sqlite3.Error as e:
                self.statusBar().showMessage(f"Database error: {str(e)}", 3000)
            finally:
                if 'conn' in locals():
                    conn.close()

    def delete_selected_fm_question(self):
        """Delete selected Fast Money question"""
        current_item = self.fm_queued_questions_listBox.currentItem()
        if not current_item:
            self.statusBar().showMessage("Please select a Fast Money question to delete", 3000)
            return

        # Confirmation dialog
        reply = self.show_message_box(
            'Confirm Deletion',
            "Are you sure you want to delete this Fast Money question?",
            QMessageBox.Question,
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return

        try:
            # Extract question ID from the item text
            question_id = int(current_item.text().split()[1])

            # Get the current directory and construct the database path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, "db", "Fast-Money Questions.db")
            
            # Connect to database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Delete answers first
            cursor.execute('DELETE FROM fast_money_answers WHERE question_id = ?', (question_id,))

            # Delete the question
            cursor.execute('DELETE FROM fast_money_questions WHERE id = ?', (question_id,))

            # Get all remaining questions ordered by ID
            cursor.execute('SELECT id FROM fast_money_questions ORDER BY id')
            questions = cursor.fetchall()
            
            # Clear and repopulate the listbox
            self.fm_queued_questions_listBox.clear()
            
            # Add questions with sequential numbers
            for index, (question_id,) in enumerate(questions, 1):
                self.fm_queued_questions_listBox.addItem(f"Question {index}")
                
            # Update the database to reflect the new ordering
            for index, (old_id,) in enumerate(questions, 1):
                if old_id != index:
                    # Update the question ID
                    cursor.execute('UPDATE fast_money_questions SET id = ? WHERE id = ?', (index, old_id))
                    # Update related answers
                    cursor.execute('UPDATE fast_money_answers SET question_id = ? WHERE question_id = ?', (index, old_id))

            # Commit the changes
            conn.commit()

            # Clear the input fields
            self.fm_game_questions_input.clear()
            for i in range(1, 6):
                getattr(self, f'fm_ans{i}_input').clear()
                getattr(self, f'fm_point{i}_input').clear()

            # Provide feedback
            self.statusBar().showMessage("Fast Money question deleted successfully!", 3000)

        except sqlite3.Error as e:
            self.statusBar().showMessage(f"Database error: {str(e)}", 3000)
        except Exception as e:
            self.statusBar().showMessage(f"Error deleting Fast Money question: {str(e)}", 3000)
        finally:
            if 'conn' in locals():
                conn.close()

#__________________________________Fast Money Timer__________________________________

    def setup_fm_timer(self):
        """Set up Fast Money timer functionality"""
        self.fm_timer = QTimer(self)
        self.fm_timer.timeout.connect(self.update_fm_timer)
        self.fm_remaining_time = 0
        
        # Set default value to empty string
        self.fm_timer_input.setText("")
        
        # Add validator to only accept numbers
        self.fm_timer_input.setValidator(QIntValidator(1, 999, self))
        
        # Connect button to start_timer method
        self.fm_startTimer_btn.clicked.connect(self.start_fm_timer)

    def start_fm_timer(self):
        """Start countdown timer for Fast Money round"""
        try:
            # Get time from input, default to 00 if empty
            time_str = self.fm_timer_input.text().strip()
            if not time_str:
                time_str = "0"
                self.fm_timer_input.setText(time_str)
            
            # Convert input to integer
            seconds = int(time_str)
            if seconds <= 0:
                seconds = 0
                self.fm_timer_input.setText("0")

            # Initialize timer
            self.fm_remaining_time = seconds
            self.fm_timer_input.setText(str(self.fm_remaining_time))
            
            # Change button style to indicate active timer
            self.fm_startTimer_btn.setStyleSheet("""
                QPushButton {
                    background-color: #006f3a;
                    color: #ffffff;
                    border: 3px solid #e97523;
                    border-radius: 0px;
                    padding: 3px;
                }
            """)
            self.fm_startTimer_btn.setText("Timer Running..")
            self.fm_startTimer_btn.setEnabled(False)
            
            # Start timer with 1-second intervals
            self.fm_timer.start(1000)
            
        except ValueError:
            # If any error occurs, default to 00 seconds
            self.fm_timer_input.setText("0")
            self.fm_remaining_time = 0
            self.fm_timer.start(1000)

    def update_fm_timer(self):
        """Update Fast Money timer display and handle timeout"""
        self.fm_remaining_time -= 1
        
        # Format time with two decimal places (25.00)
        display_time = f"{self.fm_remaining_time}"
        
        # Update both control panel and Fast Money window displays
        self.fm_timer_input.setText(str(self.fm_remaining_time))
        if self.fast_money_window:
            self.fast_money_window.fm_countdown.setText(display_time)
        
        if self.fm_remaining_time <= 0:
            # Stop timer
            self.fm_timer.stop()
            
            # Reset timer input to 00
            self.fm_timer_input.setText("0")
            if self.fast_money_window:
                self.fast_money_window.fm_countdown.setText("")
            
            # Reset button style and text
            self.fm_startTimer_btn.setStyleSheet("""
                QPushButton {
                    background-color: #008f4a;
                    color: #ffffff;
                    border: none;
                    border-radius: 0px;
                    padding: 3px;
                }
                QPushButton:hover {
                    background-color: #00a65a;
                }
                QPushButton:pressed {
                    background-color: #006f3a;
                }
            """)
            self.fm_startTimer_btn.setText("Start Timer")
            self.fm_startTimer_btn.setEnabled(True)
            
            # Play timeout sound
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                sound_path = os.path.join(current_dir, "res", "sound", "FMNoPoints.mp3")
                self.answer_sound_player.setMedia(
                    QMediaContent(QUrl.fromLocalFile(sound_path))
                )
                self.answer_sound_player.play()
            except Exception as e:
                print(f"Error playing timeout sound: {str(e)}")

#__________________________________Fast Money Answers__________________________________

    def initialize_fm_buttons_state(self):
        """Set all Fast Money buttons to disabled state on startup"""
        disabled_style = """
            QPushButton {
                background-color: #dcdcdc;
                color: #777777;
                border: 1px solid #cccccc;
                border-radius: 0px;
                padding: 5px;
            }
        """
        
        # Disable Round 1 buttons
        for i in range(1, 6):
            ans_btn = getattr(self, f'fm_R1Ans{i}_btn')
            point_btn = getattr(self, f'fm_R1Point{i}_btn')
            
            ans_btn.setEnabled(False)
            point_btn.setEnabled(False)
            ans_btn.setStyleSheet(disabled_style)
            point_btn.setStyleSheet(disabled_style)
        
        # Disable Round 2 buttons
        for i in range(1, 6):
            ans_btn = getattr(self, f'fm_R2Ans{i}_btn')
            point_btn = getattr(self, f'fm_R2Point{i}_btn')
            
            ans_btn.setEnabled(False)
            point_btn.setEnabled(False)
            ans_btn.setStyleSheet(disabled_style)
            point_btn.setStyleSheet(disabled_style)

    def update_fm_answer_buttons_state(self):
        """Update Fast Money answer and point buttons state based on input values"""
        # Define styles
        disabled_style = """
            QPushButton {
                background-color: #dcdcdc;
                color: #777777;
                border: 1px solid #cccccc;
                border-radius: 0px;
                padding: 5px;
            }
        """
        
        enabled_style = """
            QPushButton {
                background-color: #008f4a;
                color: #ffffff;
                border: none;
                border-radius: 0px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #00a65a;
            }
            QPushButton:pressed {
                background-color: #006f3a;
            }
        """
        
        # Update Round 1 buttons
        for i in range(1, 6):
            # Get the input and button widgets
            ans_input = getattr(self, f'fm_R1Ans{i}_input')
            point_input = getattr(self, f'fm_R1Point{i}_input')
            ans_btn = getattr(self, f'fm_R1Ans{i}_btn')
            point_btn = getattr(self, f'fm_R1Point{i}_btn')
            
            # Check each input separately
            if ans_input.text().strip():
                ans_btn.setEnabled(True)
                ans_btn.setStyleSheet(enabled_style)
            else:
                ans_btn.setEnabled(False)
                ans_btn.setStyleSheet(disabled_style)
                
            if point_input.text().strip():
                point_btn.setEnabled(True)
                point_btn.setStyleSheet(enabled_style)
            else:
                point_btn.setEnabled(False)
                point_btn.setStyleSheet(disabled_style)
        
        # Update Round 2 buttons
        for i in range(1, 6):
            # Get the input and button widgets
            ans_input = getattr(self, f'fm_R2Ans{i}_input')
            point_input = getattr(self, f'fm_R2Point{i}_input')
            ans_btn = getattr(self, f'fm_R2Ans{i}_btn')
            point_btn = getattr(self, f'fm_R2Point{i}_btn')
            
            # Check each input separately
            if ans_input.text().strip():
                ans_btn.setEnabled(True)
                ans_btn.setStyleSheet(enabled_style)
            else:
                ans_btn.setEnabled(False)
                ans_btn.setStyleSheet(disabled_style)
                
            if point_input.text().strip():
                point_btn.setEnabled(True)
                point_btn.setStyleSheet(enabled_style)
            else:
                point_btn.setEnabled(False)
                point_btn.setStyleSheet(disabled_style)

    def display_fm_answer(self, round_num, answer_num):
        """Display Fast Money answer in the Fast Money window"""
        try:
            # Check if Fast Money window exists and is visible
            if not self.fast_money_window or not self.fast_money_window.isVisible():
                self.statusBar().showMessage("Please open Fast Money window first!", 3000)
                return
                
            # Get the input value
            ans_input = getattr(self, f'fm_R{round_num}Ans{answer_num}_input')
            answer_text = ans_input.text().strip().upper()  # Convert to uppercase
            
            # Get the corresponding label in Fast Money window
            ans_label = getattr(self.fast_money_window, f'fmp{round_num}_ans{answer_num}')
            
            # Display the answer
            ans_label.setText(answer_text)
            ans_label.setFont(QFont("Consolas", 30))
            
            # Play reveal sound
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                sound_path = os.path.join(current_dir, "res", "sound", "hit.mp3")
                if os.path.exists(sound_path):
                    self.answer_sound_player.setMedia(
                        QMediaContent(QUrl.fromLocalFile(sound_path))
                    )
                    self.answer_sound_player.play()
            except Exception as e:
                print(f"Sound playback error (non-critical): {str(e)}")
                    
        except Exception as e:
            print(f"Error displaying Fast Money answer: {str(e)}")

    def display_fm_point(self, round_num, point_num):
        """Display Fast Money point in the Fast Money window"""
        try:
            # Check if Fast Money window exists and is visible
            if not self.fast_money_window or not self.fast_money_window.isVisible():
                self.statusBar().showMessage("Please open Fast Money window first!", 3000)
                return
                
            # Get the input value
            point_input = getattr(self, f'fm_R{round_num}Point{point_num}_input')
            point_text = point_input.text().strip()
            
            # Get the corresponding label in Fast Money window
            point_label = getattr(self.fast_money_window, f'fmp{round_num}_point{point_num}')
            
            # Display the point
            point_label.setText(point_text)
            point_label.setFont(QFont("Consolas", 30))
            
            # Play appropriate sound based on point value and winning sound state
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                
                # Determine which sound to play
                if point_text and int(point_text) > 0:
                    if hasattr(self, 'fm_winning_sound_active') and self.fm_winning_sound_active:
                        sound_file = "win-answer.mp3"
                    else:
                        sound_file = "FMCorrect.mp3"
                else:
                    sound_file = "strike.mp3"
                
                sound_path = os.path.join(current_dir, "res", "sound", sound_file)
                if os.path.exists(sound_path):
                    self.answer_sound_player.setMedia(
                        QMediaContent(QUrl.fromLocalFile(sound_path))
                    )
                    self.answer_sound_player.play()
            except Exception as e:
                print(f"Sound playback error (non-critical): {str(e)}")
                
            # Update total points after revealing new point
            self.update_fm_total_points()
                    
        except Exception as e:
            print(f"Error displaying Fast Money point: {str(e)}")

    def update_fm_total_points(self):
        """Calculate and update total points for Fast Money rounds"""
        try:
            total_points = 0
            
            # Sum up revealed points from Round 1
            for i in range(1, 6):
                point_label = getattr(self.fast_money_window, f'fmp1_point{i}')
                point_text = point_label.text().strip()
                if point_text:
                    try:
                        total_points += int(point_text)
                    except ValueError:
                        continue
            
            # Sum up revealed points from Round 2
            for i in range(1, 6):
                point_label = getattr(self.fast_money_window, f'fmp2_point{i}')
                point_text = point_label.text().strip()
                if point_text:
                    try:
                        total_points += int(point_text)
                    except ValueError:
                        continue
            
            # Update total points display in both windows
            if self.fast_money_window:
                # Update Fast Money window display
                self.fast_money_window.fm_TotalPlayer_Point.setText(str(total_points) if total_points > 0 else "")
                # Update control panel display
                self.fm_totalPoints_input.setText(str(total_points) if total_points > 0 else "")
                
        except Exception as e:
            print(f"Error updating Fast Money total points: {str(e)}")

    def clear_fm_questions(self):
        """Clear all Fast Money inputs and displays"""
        try:
            # Clear Round 1 and 2 inputs in control panel
            for i in range(1, 6):
                # Clear Round 1 inputs
                getattr(self, f'fm_R1Ans{i}_input').clear()
                getattr(self, f'fm_R1Point{i}_input').clear()
                
                # Clear Round 2 inputs
                getattr(self, f'fm_R2Ans{i}_input').clear()
                getattr(self, f'fm_R2Point{i}_input').clear()
            
            # Clear Fast Money window displays if it exists
            if self.fast_money_window:
                for i in range(1, 6):
                    # Clear Round 1 displays
                    getattr(self.fast_money_window, f'fmp1_ans{i}').setText("")
                    getattr(self.fast_money_window, f'fmp1_point{i}').setText("")
                    
                    # Clear Round 2 displays
                    getattr(self.fast_money_window, f'fmp2_ans{i}').setText("")
                    getattr(self.fast_money_window, f'fmp2_point{i}').setText("")
                
                # Clear total points
                self.fast_money_window.fm_TotalPlayer_Point.setText("")
                self.fm_totalPoints_input.setText("")
            
            # Update button states after clearing
            self.update_fm_answer_buttons_state()
            
            # Show success message
            self.statusBar().showMessage("Fast Money questions cleared!", 3000)
            
        except Exception as e:
            print(f"Error clearing Fast Money questions: {str(e)}")
            self.statusBar().showMessage("Error clearing Fast Money questions", 3000)

#__________________________________Fast Money Winning Sound__________________________________

    def setup_fm_winning_sound_button(self):
        """Setup Fast Money winning sound button and its state"""
        self.fm_winMusic_btn.setStyleSheet("""
            QPushButton {
                background-color: #008f4a;
                color: #ffffff;
                border: none;
                border-radius: 0px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #00a65a;
            }
            QPushButton:pressed {
                background-color: #006f3a;
            }
        """)
        self.fm_winMusic_btn.clicked.connect(self.toggle_fm_winning_sound)
        self.fm_winning_sound_active = False
        self.fm_winMusic_btn.setEnabled(True)

    def toggle_fm_winning_sound(self):
        """Toggle Fast Money winning sound state"""
        self.fm_winning_sound_active = not self.fm_winning_sound_active
        if self.fm_winning_sound_active:
            # Change button style to indicate active state
            self.fm_winMusic_btn.setStyleSheet("""
                QPushButton {
                    background-color: #006f3a;
                    color: #ffffff;
                    border: 3px solid #e97523;
                    border-radius: 0px;
                    padding: 3px;
                }
            """)
            self.fm_winMusic_btn.setText("Win Music Active..")
            self.statusBar().showMessage("Fast Money winning sound activated", 3000)
        else:
            # Reset button style to default
            self.fm_winMusic_btn.setStyleSheet("""
                QPushButton {
                    background-color: #008f4a;
                    color: #ffffff;
                    border: none;
                    border-radius: 0px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #00a65a;
                }
                QPushButton:pressed {
                    background-color: #006f3a;
                }
            """)
            self.fm_winMusic_btn.setText("Win Music")
            self.statusBar().showMessage("Fast Money winning sound deactivated", 3000)



    def show_message_box(self, title, text, icon_type=QMessageBox.Information, buttons=QMessageBox.Ok):
        """
        Shows a customized message box with clean, modern styling.
        
        Args:
            title (str): The title of the message box
            text (str): The main message text
            icon_type (QMessageBox.Icon): The type of icon to display
            buttons (QMessageBox.StandardButtons): The buttons to display
        """
        msg_box = QMessageBox()
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.FramelessWindowHint)
        msg_box.setWindowFlags(msg_box.windowFlags() & ~Qt.FramelessWindowHint)
        
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setIcon(icon_type)
        msg_box.setStandardButtons(buttons)
        msg_box.setWindowIcon(QIcon("res/mipmap/icon.png"))
        
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                color: #333333;
                font-size: 12px;
                font-family: 'Segoe UI';
                padding: 10px;
            }
            QPushButton {
                background-color: #008f4a;
                color: white;
                border: none;
                padding: 5px 15px;
                min-width: 60px;
                font-family: 'Segoe UI';
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #00a65a;
            }
            QPushButton:pressed {
                background-color: #006f3a;
            }
            QPushButton[text="&No"] {
                background-color: #cc0000;
            }
            QPushButton[text="&No"]:hover {
                background-color: #ff0000;
            }
            QPushButton[text="&No"]:pressed {
                background-color: #990000;
            }
        """)
        
        # Center on screen
        screen = QApplication.primaryScreen().geometry()
        msg_box.move(
            screen.center().x() - msg_box.width() // 2,
            screen.center().y() - msg_box.height() // 2
        )
        
        return msg_box.exec_()

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    
    # Use Fusion style for consistent cross-platform appearance across Windows, macOS, and Linux
    app.setStyle('Fusion')

    # Force a high-contrast light palette so macOS Dark Mode doesn't cause white text on light backgrounds
    from PyQt5.QtGui import QPalette, QColor
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor('#f9f9f9'))
    palette.setColor(QPalette.WindowText, QColor('#222222'))
    palette.setColor(QPalette.Base, QColor('#ffffff'))
    palette.setColor(QPalette.AlternateBase, QColor('#f0f0f0'))
    palette.setColor(QPalette.ToolTipBase, QColor('#ffffff'))
    palette.setColor(QPalette.ToolTipText, QColor('#222222'))
    palette.setColor(QPalette.Text, QColor('#222222'))
    palette.setColor(QPalette.Button, QColor('#f0f0f0'))
    palette.setColor(QPalette.ButtonText, QColor('#222222'))
    palette.setColor(QPalette.Highlight, QColor('#004aad'))
    palette.setColor(QPalette.HighlightedText, QColor('#ffffff'))
    app.setPalette(palette)

    widget = FamilyFeud_ControlPanel(0)
    widget.show()
    sys.exit(app.exec_())