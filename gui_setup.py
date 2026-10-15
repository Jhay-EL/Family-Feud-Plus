from PyQt5.QtWidgets import (
    QWidget, QScrollArea, QTabWidget, QLabel, QPushButton, QComboBox, QLineEdit, QTextEdit, QFrame, QListWidget
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QUrl, Qt
import os
from ui_adjustments import adjust_ui_elements


def setup_gui(self, parent):
    if parent == 0:
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setGeometry(0, 0, 1280, 720)  

        self.ControlPanel_Window = QWidget()
        self.ControlPanel_Window.setStyleSheet("background-color: #f9f9f9;")
        self.ControlPanel_Window.setGeometry(0, 0, 1280, 720)

        self.scroll.setWidget(self.ControlPanel_Window)
        self.setCentralWidget(self.scroll)
    else:
        self.ControlPanel_Window = QFrame(parent)
        self.ControlPanel_Window.setStyleSheet("background-color: #ffffff;")

    self.family = type('family', (object,), {})()
    self.family.feud = type('feud', (object,), {})()
    self.family.feud.game = type('game', (object,), {})()
    self.family.feud.game.tab = QTabWidget(self.ControlPanel_Window)
    self.family.feud.game.tab.setStyleSheet("""
        QTabWidget::pane {
            border: 1px solid #dcdcdc;
            background-color: #f9f9f9;
            top: -1px;
        }
        QTabBar::tab {
            background-color: #e5e5e5;
            color: #333333;
            padding: 8px 24px;
            margin-right: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            border: 1px solid #cccccc;
            border-bottom: none;
            font-family: Arial, sans-serif;
            font-size: 13px;
            font-weight: bold;
        }
        QTabBar::tab:selected {
            background-color: #004aad;
            color: #ffffff;
            border-color: #004aad;
        }
        QTabBar::tab:hover:!selected {
            background-color: #d8d8d8;
            color: #000000;
        }
    """)
    
     # Welcome Screen Table ------------------------------------------------------------------------------------------------------------------------------------------------------------

    self.Welcome_screen_table = QWidget()
    self.Welcome_screen_table.setStyleSheet("background-color: #f9f9f9;")
    
    self.welcomeScreen = type('welcomeScreen', (object,), {})()
    self.welcomeScreen.image = QLabel(self.Welcome_screen_table)
    
    pixmap = QPixmap("res/bg/Welcome Screen BG.png")
    if pixmap.isNull():
        print("Error: Image not found or cannot be loaded.")
    else:
        scaled_pixmap = pixmap.scaled(
            self.welcomeScreen.image.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.welcomeScreen.image.setPixmap(scaled_pixmap)
        self.welcomeScreen.image.setScaledContents(False)

    button_style_general = """
        QPushButton {
            background-color: #008f4a;
            color: #ffffff;
            border: none;
            border-radius: 10px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #00a65a;
        }
        QPushButton:pressed {
            background-color: #006f3a;
        }
    """
    
    button_style_quit = """
        QPushButton {
            background-color: #b80000;
            color: #ffffff;
            border: none;
            border-radius: 10px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #cc0000;
        }
        QPushButton:pressed {
            background-color: #990000;
        }
    """
    
    self.welcome = type('welcome', (object,), {})()
    self.welcome.screen = type('screen', (object,), {})()
    self.welcome.screen.title = type('title', (object,), {})()
    self.welcome.screen.title.label = QLabel("Family Feud+", self.Welcome_screen_table)
    self.welcome.screen.title.label.setAlignment(Qt.AlignLeft)
    self.welcome.screen.title.label.setStyleSheet("color: #004aad;")
    self.welcome.screen.title.label.setFont(QFont("Arial", 20, QFont.Bold))  
    self.welcome.screen.description = type('description', (object,), {})()
    self.welcome.screen.description.label = QLabel(
        "Guessing the most popular answers to survey questions", self.Welcome_screen_table)

    self.welcome.screen.description.label.setAlignment(Qt.AlignLeft)
    self.welcome.screen.description.label.setStyleSheet("color: #004aad;")
    self.welcome.screen.description.label.setFont(QFont("Arial", 10))
    self.deploy = type('deploy', (object,), {})()
    
    self.deploy.titleScreen = type('titleScreen', (object,), {})()
    self.deploy.titleScreen.btn = QPushButton("Title Screen", self.Welcome_screen_table)
    self.deploy.titleScreen.btn.setStyleSheet("""
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
    self.deploy.titleScreen.btn.setFont(QFont("Arial", 10))
    self.deploy.titleScreen.btn.setCursor(Qt.ArrowCursor)

    self.deploy.faceOff = type('faceOff', (object,), {})()
    self.deploy.faceOff.btn = QPushButton("Face Off Round", self.Welcome_screen_table)
    self.deploy.faceOff.btn.setStyleSheet("""
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
    self.deploy.faceOff.btn.setFont(QFont("Arial", 10))
    self.deploy.faceOff.btn.setCursor(Qt.ArrowCursor)

    self.deploy.fastMoney = type('fastMoney', (object,), {})()
    self.deploy.fastMoney.btn = QPushButton("Fast Money Round", self.Welcome_screen_table)
    self.deploy.fastMoney.btn.setStyleSheet("""
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
    self.deploy.fastMoney.btn.setFont(QFont("Arial", 10))
    self.deploy.fastMoney.btn.setCursor(Qt.ArrowCursor)

    self.game = type('game', (object,), {})()
    self.game.mechanics = type('mechanics', (object,), {})()
    self.game.mechanics.btn = QPushButton("Game Mechanics", self.Welcome_screen_table)
    self.game.mechanics.btn.setStyleSheet("""
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
    self.game.mechanics.btn.setFont(QFont("Arial", 10))
    self.game.mechanics.btn.setCursor(Qt.ArrowCursor)
    
    self.select = type('select', (object,), {})()
    self.select.the = type('the', (object,), {})()
    self.select.the.display = type('display', (object,), {})()

    self.select.the.display.label = QLabel("Select the display to deploy the game screen", self.Welcome_screen_table)
    self.select.the.display.label.setAlignment(Qt.AlignLeft)
    self.select.the.display.label.setStyleSheet("color: #004aad;")
    self.select.the.display.label.setFont(QFont("Arial", 10))

    self.display = type('display', (object,), {})()
    self.display.selection = type('selection', (object,), {})()
    self.display.selection.comboBox = QComboBox(self.Welcome_screen_table)
    self.display.selection.comboBox.setFont(QFont("Arial", 10))
    self.display.selection.comboBox.setCursor(Qt.ArrowCursor)
    combobox_style = """
        QComboBox {
            background-color: #ffffff;
            color: #000000;
            border: 2px solid #008f4a;
            padding: 5px;
        }
        QComboBox:hover {
            border: 2px solid #00a65a;
        }
        QComboBox::drop-down {
            border: none;
        }
    """
    self.display.selection.comboBox.setStyleSheet(combobox_style)
    self.display.selection.comboBox.addItem("Choose display")
    self.populate_display_comboBox()
    self.display.selection.comboBox.setCurrentIndex(0)
    
    self.ws = type('ws', (object,), {})()
    self.ws.force = type('force', (object,), {})()
    self.ws.force.quit = type('quit', (object,), {})()
    self.ws.force.quit.btn = QPushButton("Quit", self.Welcome_screen_table)
    self.ws.force.quit.btn.setStyleSheet("""
        QPushButton {
            background-color: #b80000;
            color: #ffffff;
            border: none;
            border-radius: 0px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #d40000;
        }
        QPushButton:pressed {
            background-color: #8b0000;
        }
    """)
    self.ws.force.quit.btn.setFont(QFont("Arial", 10))
    self.ws.force.quit.btn.setCursor(Qt.ArrowCursor)
    self.ws.force.quit.btn.clicked.connect(self.force_quit)

    # Face Off Round Table ------------------------------------------------------------------------------------------------------------------------------------------------------------

    self.Face_off_table = QWidget(self.family.feud.game.tab)
    self.Face_off_table.setStyleSheet("background-color: #f9f9f9;")

    self.family_feud_faceOff_round_label = QLabel("Face-off Round", self.Face_off_table)
    self.family_feud_faceOff_round_label.setAlignment(Qt.AlignLeft)
    self.family_feud_faceOff_round_label.setStyleSheet("color: #004aad;")
    self.family_feud_faceOff_round_label.setFont(QFont("Arial", 20, QFont.Bold))

    self.enter_names_label = QLabel("Enter the names of the team playing:", self.Face_off_table)
    self.enter_names_label.setAlignment(Qt.AlignLeft)
    self.enter_names_label.setStyleSheet("color: #004aad;")
    self.enter_names_label.setFont(QFont("Arial", 10))

    self.team_A_name_input = QLineEdit(self.Face_off_table)
    self.team_A_name_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.team_A_name_input.setFont(QFont("Arial", 10))
    self.team_A_name_input.setText("Team A")

    self.team_B_name_input = QLineEdit(self.Face_off_table)
    self.team_B_name_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.team_B_name_input.setFont(QFont("Arial", 10))
    self.team_B_name_input.setText("Team B")

    self.team_A_points_label = QLabel("Team A Points:", self.Face_off_table)
    self.team_A_points_label.setAlignment(Qt.AlignLeft)
    self.team_A_points_label.setStyleSheet("color: #004aad;")
    self.team_A_points_label.setFont(QFont("Arial", 10))

    self.team_B_points_label = QLabel("Team B Points:", self.Face_off_table)
    self.team_B_points_label.setAlignment(Qt.AlignLeft)
    self.team_B_points_label.setStyleSheet("color: #004aad;")
    self.team_B_points_label.setFont(QFont("Arial", 10))

    self.points_box_A = QLineEdit(self.Face_off_table)
    self.points_box_A.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.points_box_A.setFont(QFont("Arial", 10))
    self.points_box_A.setReadOnly(True)

    self.points_box_B = QLineEdit(self.Face_off_table)
    self.points_box_B.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.points_box_B.setFont(QFont("Arial", 10))
    self.points_box_B.setReadOnly(True)
    
    self.team_A_strikes_label = QLabel("Strikes:", self.Face_off_table)
    self.team_A_strikes_label.setAlignment(Qt.AlignLeft)
    self.team_A_strikes_label.setStyleSheet("color: #004aad;")
    self.team_A_strikes_label.setFont(QFont("Arial", 10))

    self.strike_box_A = QLineEdit(self.Face_off_table)
    self.strike_box_A.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.strike_box_A.setFont(QFont("Arial", 10))
    self.strike_box_A.setReadOnly(True)
    self.team_B_strikes_label = QLabel("Strikes:", self.Face_off_table)
    self.team_B_strikes_label.setAlignment(Qt.AlignLeft)
    self.team_B_strikes_label.setStyleSheet("color: #004aad;")
    self.team_B_strikes_label.setFont(QFont("Arial", 10))

    self.strike_box_B = QLineEdit(self.Face_off_table)
    self.strike_box_B.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.strike_box_B.setFont(QFont("Arial", 10))
    self.strike_box_B.setReadOnly(True)

    self.A_reward_btn = QPushButton("Reward / Steal Points", self.Face_off_table)
    self.A_reward_btn.setStyleSheet("""
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
    self.A_reward_btn.setFont(QFont("Arial", 10))

    self.B_reward_btn = QPushButton("Reward / Steal Points", self.Face_off_table)
    self.B_reward_btn.setStyleSheet("""
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
    self.B_reward_btn.setFont(QFont("Arial", 10))

    self.A_strike_btn = QPushButton("Strike", self.Face_off_table)
    self.A_strike_btn.setStyleSheet("""
        QPushButton {
            background-color: #b80000;
            color: #ffffff;
            border: none;
            border-radius: 0px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #d40000;
        }
        QPushButton:pressed {
            background-color: #8b0000;
        }
    """)
    self.A_strike_btn.setFont(QFont("Arial", 10))
    self.A_strike_btn.clicked.connect(self.play_strike_sound)

    self.B_strike_btn = QPushButton("Strike", self.Face_off_table)
    self.B_strike_btn.setStyleSheet("""
        QPushButton {
            background-color: #b80000;
            color: #ffffff;
            border: none;
            border-radius: 0px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #d40000;
        }
        QPushButton:pressed {
            background-color: #8b0000;
        }
    """)
    self.B_strike_btn.setFont(QFont("Arial", 10))
    self.B_strike_btn.clicked.connect(self.play_strike_sound)


    self.game_audio_control_label = QLabel("Game Audio Control", self.Face_off_table)
    self.game_audio_control_label.setAlignment(Qt.AlignLeft)
    self.game_audio_control_label.setStyleSheet("color: #004aad;")
    self.game_audio_control_label.setFont(QFont("Arial", 10))

    self.intro_music_btn = QPushButton("Intro Music", self.Face_off_table)
    self.intro_music_btn.setStyleSheet("""
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
    self.intro_music_btn.setFont(QFont("Arial", 10))
    self.intro_music_btn.clicked.connect(self.play_intro_sound)

    self.outro_music_btn = QPushButton("Outro Music", self.Face_off_table)
    self.outro_music_btn.setStyleSheet("""
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
    self.outro_music_btn.setFont(QFont("Arial", 10))
    self.outro_music_btn.clicked.connect(self.play_outro_sound)


    self.face_off_music_btn = QPushButton("Face-off v.1", self.Face_off_table)
    self.face_off_music_btn.setStyleSheet("""
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
    self.face_off_music_btn.setFont(QFont("Arial", 10))
    self.face_off_music_btn.clicked.connect(self.play_FaceOff_sound)

    self.correct_ans_music_btn = QPushButton("Correct Ans.", self.Face_off_table)
    self.correct_ans_music_btn.setStyleSheet("""
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
    self.correct_ans_music_btn.setFont(QFont("Arial", 10))
    self.correct_ans_music_btn.clicked.connect(self.play_CorrectAnswer_sound)

    self.winning_sound_btn = QPushButton("Winning Sound", self.Face_off_table)
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
    self.winning_sound_btn.setFont(QFont("Arial", 10))
    self.winning_sound_btn.clicked.connect(self.activate_winning_sound)


    self.strike_music_btn = QPushButton("Strike/Timer", self.Face_off_table)
    self.strike_music_btn.setStyleSheet("""
        QPushButton {
            background-color: #b80000;
            color: #ffffff;
            border: none;
            border-radius: 0px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #d40000;
        }
        QPushButton:pressed {
            background-color: #8b0000;
        }
    """)
    self.strike_music_btn.setFont(QFont("Arial", 10))
    self.strike_music_btn.clicked.connect(self.play_strike_sound)

    self.round_multiplier_label = QLabel("Round multiplier and timer", self.Face_off_table)
    self.round_multiplier_label.setAlignment(Qt.AlignLeft)
    self.round_multiplier_label.setStyleSheet("color: #004aad;")
    self.round_multiplier_label.setFont(QFont("Arial", 10))

    self.x3_round_btn = QPushButton("x3 Round", self.Face_off_table)
    self.x3_round_btn.setStyleSheet("""
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
    self.x3_round_btn.setFont(QFont("Arial", 10))
    self.x3_round_btn.clicked.connect(self.toggle_x3_round)


    self.start_timer_btn = QPushButton("Start Timer", self.Face_off_table)
    self.start_timer_btn.setStyleSheet("""
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
    self.start_timer_btn.setFont(QFont("Arial", 10))
    self.start_timer_btn.clicked.connect(self.start_timer)


    self.x2_round_btn = QPushButton("x2 Round", self.Face_off_table)
    self.x2_round_btn.setStyleSheet("""
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
    self.x2_round_btn.setFont(QFont("Arial", 10))
    self.x2_round_btn.clicked.connect(self.toggle_x2_round)


    self.timer_input = QLineEdit(self.Face_off_table)
    self.timer_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.timer_input.setFont(QFont("Arial", 10))
    self.timer_input.setText("3")

    self.game_questions_view_label = QLabel("Game Questions View", self.Face_off_table)
    self.game_questions_view_label.setAlignment(Qt.AlignLeft)
    self.game_questions_view_label.setStyleSheet("color: #004aad;")
    self.game_questions_view_label.setFont(QFont("Arial", 10))

    self.game_questions_input = QTextEdit(self.Face_off_table)
    self.game_questions_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.game_questions_input.setFont(QFont("Arial", 10))
    self.game_questions_input.setReadOnly(True)

    self.point1_input = QLineEdit(self.Face_off_table)
    self.point1_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.point1_input.setFont(QFont("Arial", 10))
    self.point1_input.setReadOnly(True)

    self.point2_input = QLineEdit(self.Face_off_table)
    self.point2_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.point2_input.setFont(QFont("Arial", 10))
    self.point2_input.setReadOnly(True)

    self.point3_input = QLineEdit(self.Face_off_table)
    self.point3_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.point3_input.setFont(QFont("Arial", 10))
    self.point3_input.setReadOnly(True)

    self.point4_input = QLineEdit(self.Face_off_table)
    self.point4_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.point4_input.setFont(QFont("Arial", 10))
    self.point4_input.setReadOnly(True)

    self.point5_input = QLineEdit(self.Face_off_table)
    self.point5_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.point5_input.setFont(QFont("Arial", 10))
    self.point5_input.setReadOnly(True)

    self.point6_input = QLineEdit(self.Face_off_table)
    self.point6_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.point6_input.setFont(QFont("Arial", 10))
    self.point6_input.setReadOnly(True)

    self.point7_input = QLineEdit(self.Face_off_table)
    self.point7_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.point7_input.setFont(QFont("Arial", 10))
    self.point7_input.setReadOnly(True)

    self.point8_input = QLineEdit(self.Face_off_table)
    self.point8_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.point8_input.setFont(QFont("Arial", 10))
    self.point8_input.setReadOnly(True)

    self.ans1_btn = QPushButton("Answer 1", self.Face_off_table)
    self.ans1_btn.setStyleSheet("""
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
    self.ans1_btn.setFont(QFont("Arial", 10))
    self.ans1_btn.clicked.connect(self.play_answer_sound)

    self.ans2_btn = QPushButton("Answer 2", self.Face_off_table)
    self.ans2_btn.setStyleSheet("""
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
    self.ans2_btn.setFont(QFont("Arial", 10))   
    self.ans2_btn.clicked.connect(self.play_answer_sound)

    self.ans3_btn = QPushButton("Answer 3", self.Face_off_table)
    self.ans3_btn.setStyleSheet("""
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
    self.ans3_btn.setFont(QFont("Arial", 10))
    self.ans3_btn.clicked.connect(self.play_answer_sound)

    self.ans4_btn = QPushButton("Answer 4", self.Face_off_table)
    self.ans4_btn.setStyleSheet("""
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
    self.ans4_btn.setFont(QFont("Arial", 10))
    self.ans4_btn.clicked.connect(self.play_answer_sound)

    self.ans5_btn = QPushButton("Answer 5", self.Face_off_table)
    self.ans5_btn.setStyleSheet("""
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
    self.ans5_btn.setFont(QFont("Arial", 10))
    self.ans5_btn.clicked.connect(self.play_answer_sound)

    self.ans6_btn = QPushButton("Answer 6", self.Face_off_table)
    self.ans6_btn.setStyleSheet("""
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
    self.ans6_btn.setFont(QFont("Arial", 10))
    self.ans6_btn.clicked.connect(self.play_answer_sound)

    self.ans7_btn = QPushButton("Answer 7", self.Face_off_table)
    self.ans7_btn.setStyleSheet("""
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
    self.ans7_btn.setFont(QFont("Arial", 10))
    self.ans7_btn.clicked.connect(self.play_answer_sound)

    self.ans8_btn = QPushButton("Answer 8", self.Face_off_table)
    self.ans8_btn.setStyleSheet("""
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
    self.ans8_btn.setFont(QFont("Arial", 10))
    self.ans8_btn.clicked.connect(self.play_answer_sound)

    self.total_points_input = QLineEdit(self.Face_off_table)
    self.total_points_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.total_points_input.setFont(QFont("Arial", 10))
    self.total_points_input.setReadOnly(True)

    self.total_points_label = QLabel("Total Points:", self.Face_off_table)
    self.total_points_label.setAlignment(Qt.AlignLeft)
    self.total_points_label.setStyleSheet("color: #004aad;")
    self.total_points_label.setFont(QFont("Arial", 10))

    self.show_answers_count_btn = QPushButton("Show answer count", self.Face_off_table)
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
    self.show_answers_count_btn.setFont(QFont("Arial", 10))
    self.show_answers_count_btn.clicked.connect(self.play_ShowAnswerCount_sound)

    self.clear_answers_count_btn = QPushButton("Clear answer count", self.Face_off_table)
    self.clear_answers_count_btn.setStyleSheet("""
        QPushButton {
            background-color: #b80000;
            color: #ffffff;
            border: none;
            border-radius: 0px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #d40000;
        }
        QPushButton:pressed {
            background-color: #8b0000;
        }
    """)
    self.clear_answers_count_btn.setFont(QFont("Arial", 10))

    self.show_answers_count_label = QLabel("Show answers count on Face-off window", self.Face_off_table)
    self.show_answers_count_label.setAlignment(Qt.AlignLeft)
    self.show_answers_count_label.setStyleSheet("color: #004aad;")
    self.show_answers_count_label.setFont(QFont("Arial", 10))

    self.queued_questions_listbox = QListWidget(self.Face_off_table)
    self.queued_questions_listbox.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.queued_questions_listbox.setFont(QFont("Arial", 10))


    self.add_questions_to_database_label = QLabel("Add questions to the database", self.Face_off_table)
    self.add_questions_to_database_label.setAlignment(Qt.AlignLeft)
    self.add_questions_to_database_label.setStyleSheet("color: #004aad;")
    self.add_questions_to_database_label.setFont(QFont("Arial", 10))

    self.load_file_btn = QPushButton("Load from file", self.Face_off_table)
    self.load_file_btn.setStyleSheet("""
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
    self.load_file_btn.setFont(QFont("Arial", 10))

    self.manual_add_btn = QPushButton("Manual add questions", self.Face_off_table)
    self.manual_add_btn.setStyleSheet("""
        QPushButton {
            background-color: #ea7620;
            color: #ffffff;
            border: none;
            border-radius: 0px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #fa8630;
        }
        QPushButton:pressed {
            background-color: #da6610;
        }
    """)
    self.manual_add_btn.setFont(QFont("Arial", 10))

    self.edit_questions_and_answers_label = QLabel("Edit questions and answers from the database", self.Face_off_table)
    self.edit_questions_and_answers_label.setAlignment(Qt.AlignLeft)
    self.edit_questions_and_answers_label.setStyleSheet("color: #004aad;")
    self.edit_questions_and_answers_label.setFont(QFont("Arial", 10))

    self.modify_btn = QPushButton("Modify", self.Face_off_table)
    self.modify_btn.setStyleSheet("""
        QPushButton {
            background-color: #ea7620;
            color: #ffffff;
            border: none;
            border-radius: 0px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #fa8630;
        }
        QPushButton:pressed {
            background-color: #da6610;
        }
    """)
    self.modify_btn.setFont(QFont("Arial", 10))

    self.save_btn = QPushButton("Save", self.Face_off_table)
    self.save_btn.setStyleSheet("""
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
    self.save_btn.setFont(QFont("Arial", 10))

    self.delete_btn = QPushButton("Delete", self.Face_off_table)
    self.delete_btn.setStyleSheet("""
        QPushButton {
            background-color: #b80000;
            color: #ffffff;
            border: none;
            border-radius: 0px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #d40000;
        }
        QPushButton:pressed {
            background-color: #8b0000;
        }
    """)
    self.delete_btn.setFont(QFont("Arial", 10))

    self.start_over_clear_log_label = QLabel("Start over or clear the log of the game", self.Face_off_table)
    self.start_over_clear_log_label.setAlignment(Qt.AlignLeft)
    self.start_over_clear_log_label.setStyleSheet("color: #004aad;")
    self.start_over_clear_log_label.setFont(QFont("Arial", 10))

    self.log_next_round = QPushButton("Log, Next round", self.Face_off_table)
    self.log_next_round.setStyleSheet("""
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
    self.log_next_round.setFont(QFont("Arial", 10))

    self.clear_log_btn = QPushButton("Reset All", self.Face_off_table)
    self.clear_log_btn.setStyleSheet("""
        QPushButton {
            background-color: #b80000;
            color: #ffffff;
            border: none;
            border-radius: 0px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #d40000;
        }
        QPushButton:pressed {
            background-color: #8b0000;
        }
    """)
    self.clear_log_btn.setFont(QFont("Arial", 10))

    self.B_round1_points_box = QLineEdit(self.Face_off_table)
    self.B_round1_points_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.B_round1_points_box.setFont(QFont("Arial", 10))
    self.B_round1_points_box.setReadOnly(True)
    self.B_points_label = QLabel("Points", self.Face_off_table)
    self.B_points_label.setAlignment(Qt.AlignLeft)
    self.B_points_label.setStyleSheet("color: #004aad;")
    self.B_points_label.setFont(QFont("Arial", 10))

    self.B_round1_label = QLabel("R1", self.Face_off_table)
    self.B_round1_label.setAlignment(Qt.AlignLeft)
    self.B_round1_label.setStyleSheet("color: #004aad;")
    self.B_round1_label.setFont(QFont("Arial", 10))

    self.B_round2_points_box = QLineEdit(self.Face_off_table)
    self.B_round2_points_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.B_round2_points_box.setFont(QFont("Arial", 10))
    self.B_round2_points_box.setReadOnly(True)
    self.B_round2_label = QLabel("R2", self.Face_off_table)
    self.B_round2_label.setAlignment(Qt.AlignLeft)
    self.B_round2_label.setStyleSheet("color: #004aad;")
    self.B_round2_label.setFont(QFont("Arial", 10))

    self.B_round3_points_box = QLineEdit(self.Face_off_table)
    self.B_round3_points_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.B_round3_points_box.setFont(QFont("Arial", 10))
    self.B_round3_points_box.setReadOnly(True)
    self.B_round3_label = QLabel("R3", self.Face_off_table)
    self.B_round3_label.setAlignment(Qt.AlignLeft)
    self.B_round3_label.setStyleSheet("color: #004aad;")
    self.B_round3_label.setFont(QFont("Arial", 10))

    self.B_round4_points_box = QLineEdit(self.Face_off_table)
    self.B_round4_points_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.B_round4_points_box.setFont(QFont("Arial", 10))
    self.B_round4_points_box.setReadOnly(True)

    self.B_round4_label = QLabel("R4", self.Face_off_table)
    self.B_round4_label.setAlignment(Qt.AlignLeft)
    self.B_round4_label.setStyleSheet("color: #004aad;")
    self.B_round4_label.setFont(QFont("Arial", 10))

    self.B_round1_strike_box = QLineEdit(self.Face_off_table)
    self.B_round1_strike_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.B_round1_strike_box.setFont(QFont("Arial", 10))
    self.B_round1_strike_box.setReadOnly(True)

    self.B_strikes_label = QLabel("Strikes", self.Face_off_table)
    self.B_strikes_label.setAlignment(Qt.AlignLeft)
    self.B_strikes_label.setStyleSheet("color: #004aad;")
    self.B_strikes_label.setFont(QFont("Arial", 10))

    self.B_round2_strike_box = QLineEdit(self.Face_off_table)
    self.B_round2_strike_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.B_round2_strike_box.setFont(QFont("Arial", 10))
    self.B_round2_strike_box.setReadOnly(True)

    self.B_round3_strike_box = QLineEdit(self.Face_off_table)
    self.B_round3_strike_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.B_round3_strike_box.setFont(QFont("Arial", 10))
    self.B_round3_strike_box.setReadOnly(True)

    self.B_round4_strike_box = QLineEdit(self.Face_off_table)
    self.B_round4_strike_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.B_round4_strike_box.setFont(QFont("Arial", 10))
    self.B_round4_strike_box.setReadOnly(True)
    self.A_round1_points_box = QLineEdit(self.Face_off_table)
    self.A_round1_points_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.A_round1_points_box.setFont(QFont("Arial", 10))
    self.A_round1_points_box.setReadOnly(True)

    self.A_points_label = QLabel("Points", self.Face_off_table)
    self.A_points_label.setAlignment(Qt.AlignLeft)
    self.A_points_label.setStyleSheet("color: #004aad;")
    self.A_points_label.setFont(QFont("Arial", 10))

    self.A_round1_label = QLabel("R1", self.Face_off_table)
    self.A_round1_label.setAlignment(Qt.AlignLeft)
    self.A_round1_label.setStyleSheet("color: #004aad;")
    self.A_round1_label.setFont(QFont("Arial", 10))

    self.A_round2_points_box = QLineEdit(self.Face_off_table)
    self.A_round2_points_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.A_round2_points_box.setFont(QFont("Arial", 10))
    self.A_round2_points_box.setReadOnly(True)

    self.A_round2_label = QLabel("R2", self.Face_off_table)
    self.A_round2_label.setAlignment(Qt.AlignLeft)
    self.A_round2_label.setStyleSheet("color: #004aad;")
    self.A_round2_label.setFont(QFont("Arial", 10))

    self.A_round3_points_box = QLineEdit(self.Face_off_table)
    self.A_round3_points_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.A_round3_points_box.setFont(QFont("Arial", 10))
    self.A_round3_points_box.setReadOnly(True)

    self.A_round3_label = QLabel("R3", self.Face_off_table)
    self.A_round3_label.setAlignment(Qt.AlignLeft)
    self.A_round3_label.setStyleSheet("color: #004aad;")
    self.A_round3_label.setFont(QFont("Arial", 10))

    self.A_round4_points_box = QLineEdit(self.Face_off_table)
    self.A_round4_points_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.A_round4_points_box.setFont(QFont("Arial", 10))
    self.A_round4_points_box.setReadOnly(True)

    self.A_round4_label = QLabel("R4", self.Face_off_table)
    self.A_round4_label.setAlignment(Qt.AlignLeft)
    self.A_round4_label.setStyleSheet("color: #004aad;")
    self.A_round4_label.setFont(QFont("Arial", 10))

    self.A_round1_strike_box = QLineEdit(self.Face_off_table)
    self.A_round1_strike_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.A_round1_strike_box.setFont(QFont("Arial", 10))
    self.A_round1_strike_box.setReadOnly(True)

    self.A_strikes_label = QLabel("Strikes", self.Face_off_table)
    self.A_strikes_label.setAlignment(Qt.AlignLeft)
    self.A_strikes_label.setStyleSheet("color: #004aad;")
    self.A_strikes_label.setFont(QFont("Arial", 10))

    self.A_round2_strike_box = QLineEdit(self.Face_off_table)
    self.A_round2_strike_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.A_round2_strike_box.setFont(QFont("Arial", 10))
    self.A_round2_strike_box.setReadOnly(True)

    self.A_round3_strike_box = QLineEdit(self.Face_off_table)
    self.A_round3_strike_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.A_round3_strike_box.setFont(QFont("Arial", 10))
    self.A_round3_strike_box.setReadOnly(True)

    self.A_round4_strike_box = QLineEdit(self.Face_off_table)
    self.A_round4_strike_box.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.A_round4_strike_box.setFont(QFont("Arial", 10))
    self.A_round4_strike_box.setReadOnly(True)

    self.sec_label = QLabel(".sec", self.Face_off_table)
    self.sec_label.setAlignment(Qt.AlignLeft)
    self.sec_label.setStyleSheet("color: #004aad;")
    self.sec_label.setFont(QFont("Arial", 10))

    self.supported_file_type_label = QLabel(".db only supported", self.Face_off_table)
    self.supported_file_type_label.setAlignment(Qt.AlignLeft)
    self.supported_file_type_label.setStyleSheet("color: #004aad;")
    self.supported_file_type_label.setFont(QFont("Arial", 10))

#----------------------------------- Fast Money Round Table -----------------------------------

    self.Fast_Money_Round_Table = QWidget(self.family.feud.game.tab)
    self.Fast_Money_Round_Table.setStyleSheet("background-color: #f9f9f9;")

    self.family_feud_fast_money_round_label = QLabel("Fast Money Round", self.Fast_Money_Round_Table)
    self.family_feud_fast_money_round_label.setAlignment(Qt.AlignLeft)
    self.family_feud_fast_money_round_label.setStyleSheet("color: #004aad;")
    self.family_feud_fast_money_round_label.setFont(QFont("Arial", 20, QFont.Bold))

    self.select_team_to_play_fm_label = QLabel("Select team to play the Fast Money round", self.Fast_Money_Round_Table)
    self.select_team_to_play_fm_label.setAlignment(Qt.AlignLeft)
    self.select_team_to_play_fm_label.setStyleSheet("color: #004aad;")
    self.select_team_to_play_fm_label.setFont(QFont("Arial", 10))

    self.team_listBox = QComboBox(self.Fast_Money_Round_Table)
    self.team_listBox.setFont(QFont("Arial", 10))
    self.team_listBox.addItems(["Choose Team"])
    self.team_listBox.setCurrentIndex(0)
    self.team_listBox.setStyleSheet("""
        QComboBox {
            background-color: #ffffff;
            color: #000000;
            border: 2px solid #008f4a;
            padding: 5px;
        }
        QComboBox:hover {
            border: 2px solid #00a65a;
        }
        QComboBox::drop-down {
            border: none;
        }
    """)

    self.team_A_name_input.textChanged.connect(self.update_team_listBox)
    self.team_B_name_input.textChanged.connect(self.update_team_listBox)

    self.game_question_view_label = QLabel("Game questions view", self.Fast_Money_Round_Table)
    self.game_question_view_label.setAlignment(Qt.AlignLeft)
    self.game_question_view_label.setStyleSheet("color: #004aad;")
    self.game_question_view_label.setFont(QFont("Arial", 10))

    self.fm_game_questions_input = QTextEdit(self.Fast_Money_Round_Table)
    self.fm_game_questions_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_game_questions_input.setFont(QFont("Arial", 10))
    self.fm_game_questions_input.setReadOnly(True)

    self.fm_point1_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_point1_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_point1_input.setFont(QFont("Arial", 10))
    self.fm_point1_input.setReadOnly(True)

    self.fm_point2_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_point2_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_point2_input.setFont(QFont("Arial", 10))
    self.fm_point2_input.setReadOnly(True)

    self.fm_point3_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_point3_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_point3_input.setFont(QFont("Arial", 10))
    self.fm_point3_input.setReadOnly(True)

    self.fm_point4_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_point4_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_point4_input.setFont(QFont("Arial", 10))
    self.fm_point4_input.setReadOnly(True)

    self.fm_point5_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_point5_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_point5_input.setFont(QFont("Arial", 10))
    self.fm_point5_input.setReadOnly(True)

    self.fm_add_questions_to_database_label = QLabel("Add or load questions and answer to the database", self.Fast_Money_Round_Table)
    self.fm_add_questions_to_database_label.setAlignment(Qt.AlignLeft)
    self.fm_add_questions_to_database_label.setStyleSheet("color: #004aad;")
    self.fm_add_questions_to_database_label.setFont(QFont("Arial", 10))

    self.fm_load_from_file_btn = QPushButton("Load from file", self.Fast_Money_Round_Table)
    self.fm_load_from_file_btn.setStyleSheet("""
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
    self.fm_load_from_file_btn.setFont(QFont("Arial", 10))
    self.fm_load_from_file_btn.clicked.connect(self.load_fm_database_file)


    self.fm_manual_add_questions_btn = QPushButton("Manual Add questions", self.Fast_Money_Round_Table)
    self.fm_manual_add_questions_btn.setStyleSheet("""
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
    self.fm_manual_add_questions_btn.setFont(QFont("Arial", 10))
    self.fm_manual_add_questions_btn.clicked.connect(lambda: self.toggle_fm_edit_mode(self.fm_manual_add_questions_btn))


    self.fm_edit_questions_and_answers_label = QLabel("Edit questions and answers from the database", self.Fast_Money_Round_Table)
    self.fm_edit_questions_and_answers_label.setAlignment(Qt.AlignLeft)
    self.fm_edit_questions_and_answers_label.setStyleSheet("color: #004aad;")
    self.fm_edit_questions_and_answers_label.setFont(QFont("Arial", 10))

    self.fm_mod_btn = QPushButton("Modify", self.Fast_Money_Round_Table)
    self.fm_mod_btn.setStyleSheet("""
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
    self.fm_mod_btn.setFont(QFont("Arial", 10))
    self.fm_mod_btn.clicked.connect(lambda: self.toggle_fm_edit_mode(self.fm_mod_btn))

    self.fm_save_btn = QPushButton("Save", self.Fast_Money_Round_Table)
    self.fm_save_btn.setStyleSheet("""
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
    self.fm_save_btn.setFont(QFont("Arial", 10))
    self.fm_save_btn.clicked.connect(self.save_fm_modified_question)


    self.fm_delete_btn = QPushButton("Delete", self.Fast_Money_Round_Table)
    self.fm_delete_btn.setStyleSheet("""
        QPushButton {
            background-color: #b80000;
            color: #ffffff;
            border: none;
            border-radius: 0px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #d40000;
        }
        QPushButton:pressed {
            background-color: #8b0000;
        }
    """)
    self.fm_delete_btn.setFont(QFont("Arial", 10))
    self.fm_delete_btn.clicked.connect(self.delete_selected_fm_question)


    self.click_the_ans_btn_to_reveal_label = QLabel("Click the answer button to reveal to the Fast Money round window", self.Fast_Money_Round_Table)
    self.click_the_ans_btn_to_reveal_label.setAlignment(Qt.AlignLeft)
    self.click_the_ans_btn_to_reveal_label.setStyleSheet("color: #004aad;")
    self.click_the_ans_btn_to_reveal_label.setFont(QFont("Arial", 10))

    self.fm_R1Ans1_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R1Ans1_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R1Ans1_input.setFont(QFont("Arial", 10))

    self.contestant_answers_label = QLabel("Contestant answers", self.Fast_Money_Round_Table)
    self.contestant_answers_label.setAlignment(Qt.AlignLeft)
    self.contestant_answers_label.setStyleSheet("color: #004aad;")
    self.contestant_answers_label.setFont(QFont("Arial", 10))

    self.player1_answers_label = QLabel("Player 1 answers", self.Fast_Money_Round_Table)
    self.player1_answers_label.setAlignment(Qt.AlignLeft)
    self.player1_answers_label.setStyleSheet("color: #004aad;")
    self.player1_answers_label.setFont(QFont("Arial", 10))

    self.fm_R1Ans2_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R1Ans2_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R1Ans2_input.setFont(QFont("Arial", 10))

    self.fm_R1Ans3_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R1Ans3_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R1Ans3_input.setFont(QFont("Arial", 10))

    self.fm_R1Ans4_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R1Ans4_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R1Ans4_input.setFont(QFont("Arial", 10))

    self.fm_R1Ans5_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R1Ans5_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R1Ans5_input.setFont(QFont("Arial", 10))

    self.player2_answers_label = QLabel("Player 2 answers", self.Fast_Money_Round_Table)
    self.player2_answers_label.setAlignment(Qt.AlignLeft)
    self.player2_answers_label.setStyleSheet("color: #004aad;")
    self.player2_answers_label.setFont(QFont("Arial", 10))

    self.fm_R2Ans1_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R2Ans1_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R2Ans1_input.setFont(QFont("Arial", 10))

    self.fm_R2Ans2_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R2Ans2_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R2Ans2_input.setFont(QFont("Arial", 10))

    self.fm_R2Ans3_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R2Ans3_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R2Ans3_input.setFont(QFont("Arial", 10))

    self.fm_R2Ans4_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R2Ans4_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R2Ans4_input.setFont(QFont("Arial", 10))

    self.fm_R2Ans5_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R2Ans5_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R2Ans5_input.setFont(QFont("Arial", 10))

    self.fm_R1Ans1_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R1Ans1_btn.setStyleSheet("""
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
    self.fm_R1Ans1_btn.setFont(QFont("Arial", 10))

    self.fm_R1Ans2_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R1Ans2_btn.setStyleSheet("""
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
    self.fm_R1Ans2_btn.setFont(QFont("Arial", 10))

    self.fm_R1Ans3_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R1Ans3_btn.setStyleSheet("""
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
    self.fm_R1Ans3_btn.setFont(QFont("Arial", 10))

    self.fm_R1Ans4_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R1Ans4_btn.setStyleSheet("""
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
    self.fm_R1Ans4_btn.setFont(QFont("Arial", 10))

    self.fm_R1Ans5_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R1Ans5_btn.setStyleSheet("""
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
    self.fm_R1Ans5_btn.setFont(QFont("Arial", 10))

    self.fm_R2Ans1_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R2Ans1_btn.setStyleSheet("""
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
    self.fm_R2Ans1_btn.setFont(QFont("Arial", 10))

    self.fm_R2Ans2_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R2Ans2_btn.setStyleSheet("""
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
    self.fm_R2Ans2_btn.setFont(QFont("Arial", 10))

    self.fm_R2Ans3_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R2Ans3_btn.setStyleSheet("""
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
    self.fm_R2Ans3_btn.setFont(QFont("Arial", 10))

    self.fm_R2Ans4_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R2Ans4_btn.setStyleSheet("""
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
    self.fm_R2Ans4_btn.setFont(QFont("Arial", 10))

    self.fm_R2Ans5_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R2Ans5_btn.setStyleSheet("""
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
    self.fm_R2Ans5_btn.setFont(QFont("Arial", 10))

    self.fm_R1Point1_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R1Point1_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R1Point1_input.setFont(QFont("Arial", 10))

    self.fm_R1Point2_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R1Point2_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R1Point2_input.setFont(QFont("Arial", 10))

    self.fm_R1Point3_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R1Point3_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R1Point3_input.setFont(QFont("Arial", 10))

    self.fm_R1Point4_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R1Point4_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R1Point4_input.setFont(QFont("Arial", 10))

    self.fm_R1Point5_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R1Point5_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R1Point5_input.setFont(QFont("Arial", 10))

    self.fm_R2Point1_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R2Point1_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R2Point1_input.setFont(QFont("Arial", 10))

    self.fm_R2Point2_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R2Point2_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R2Point2_input.setFont(QFont("Arial", 10))

    self.fm_R2Point3_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R2Point3_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R2Point3_input.setFont(QFont("Arial", 10))

    self.fm_R2Point4_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R2Point4_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R2Point4_input.setFont(QFont("Arial", 10))

    self.fm_R2Point5_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_R2Point5_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_R2Point5_input.setFont(QFont("Arial", 10))

    self.fm_R1Point1_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R1Point1_btn.setStyleSheet("""
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
    self.fm_R1Point1_btn.setFont(QFont("Arial", 10))

    self.fm_R1Point2_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R1Point2_btn.setStyleSheet("""
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
    self.fm_R1Point2_btn.setFont(QFont("Arial", 10))

    self.fm_R1Point3_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R1Point3_btn.setStyleSheet("""
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
    self.fm_R1Point3_btn.setFont(QFont("Arial", 10))

    self.fm_R1Point4_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R1Point4_btn.setStyleSheet("""
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
    self.fm_R1Point4_btn.setFont(QFont("Arial", 10))

    self.fm_R1Point5_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R1Point5_btn.setStyleSheet("""
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
    self.fm_R1Point5_btn.setFont(QFont("Arial", 10))

    self.fm_R2Point1_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R2Point1_btn.setStyleSheet("""
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
    self.fm_R2Point1_btn.setFont(QFont("Arial", 10))

    self.fm_R2Point2_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R2Point2_btn.setStyleSheet("""
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
    self.fm_R2Point2_btn.setFont(QFont("Arial", 10))

    self.fm_R2Point3_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R2Point3_btn.setStyleSheet("""
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
    self.fm_R2Point3_btn.setFont(QFont("Arial", 10))

    self.fm_R2Point4_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R2Point4_btn.setStyleSheet("""
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
    self.fm_R2Point4_btn.setFont(QFont("Arial", 10))

    self.fm_R2Point5_btn = QPushButton("Reveal", self.Fast_Money_Round_Table)
    self.fm_R2Point5_btn.setStyleSheet("""
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
    self.fm_R2Point5_btn.setFont(QFont("Arial", 10))

    self.fm_queued_questions_listBox = QListWidget(self.Fast_Money_Round_Table)
    self.fm_queued_questions_listBox.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_queued_questions_listBox.setFont(QFont("Arial", 10))
    self.fm_queued_questions_listBox.itemClicked.connect(self.display_selected_fm_question)


    self.queued_questions_label = QLabel("Queued questions", self.Fast_Money_Round_Table)
    self.queued_questions_label.setAlignment(Qt.AlignLeft)
    self.queued_questions_label.setStyleSheet("color: #004aad;")
    self.queued_questions_label.setFont(QFont("Arial", 10))

    self.fm_timer_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_timer_input.setStyleSheet("background-color: #efefef; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_timer_input.setFont(QFont("Arial", 10))

    self.set_timer_label = QLabel("Set timer to the game", self.Fast_Money_Round_Table)
    self.set_timer_label.setAlignment(Qt.AlignLeft)
    self.set_timer_label.setStyleSheet("color: #004aad;")
    self.set_timer_label.setFont(QFont("Arial", 10))

    self.fm_startTimer_btn = QPushButton("Start timer", self.Fast_Money_Round_Table)
    self.fm_startTimer_btn.setStyleSheet("""
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
    self.fm_startTimer_btn.setFont(QFont("Arial", 10))

    self.fm_ans1_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_ans1_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_ans1_input.setFont(QFont("Arial", 10))
    self.fm_ans1_input.setReadOnly(True)

    self.fm_ans2_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_ans2_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_ans2_input.setFont(QFont("Arial", 10))
    self.fm_ans2_input.setReadOnly(True)

    self.fm_ans3_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_ans3_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_ans3_input.setFont(QFont("Arial", 10))
    self.fm_ans3_input.setReadOnly(True)

    self.fm_ans4_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_ans4_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_ans4_input.setFont(QFont("Arial", 10))
    self.fm_ans4_input.setReadOnly(True)

    self.fm_ans5_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_ans5_input.setStyleSheet("background-color: #c8c8c8; color: #000000; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_ans5_input.setFont(QFont("Arial", 10))
    self.fm_ans5_input.setReadOnly(True)

    self.win_music_label = QLabel("Winning Answer Sound", self.Fast_Money_Round_Table)
    self.win_music_label.setAlignment(Qt.AlignLeft)
    self.win_music_label.setStyleSheet("color: #004aad;")
    self.win_music_label.setFont(QFont("Arial", 10))

    self.fm_winMusic_btn = QPushButton("Winning Answer Sound", self.Fast_Money_Round_Table)
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
    self.fm_winMusic_btn.setFont(QFont("Arial", 10))

    self.fm_clearQuestions_btn = QPushButton("Clear questions", self.Fast_Money_Round_Table)
    self.fm_clearQuestions_btn.setStyleSheet("""
        QPushButton {
            background-color: #b80000;
            color: #ffffff;
            border: none;
            border-radius: 0px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #d40000;
        }
        QPushButton:pressed {
            background-color: #8b0000;
        }
    """)
    self.fm_clearQuestions_btn.setFont(QFont("Arial", 10))
    self.fm_clearQuestions_btn.clicked.connect(self.clear_fm_questions)



    self.fm_startOver_btn = QPushButton("Start Over", self.Fast_Money_Round_Table)
    self.fm_startOver_btn.setStyleSheet("""
        QPushButton {
            background-color: #b80000;
            color: #ffffff;
            border: none;
            border-radius: 0px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #d40000;
        }
        QPushButton:pressed {
            background-color: #8b0000;
        }
    """)
    self.fm_startOver_btn.setFont(QFont("Arial", 10))

    self.fm_saveQandA_btn = QPushButton("Save", self.Fast_Money_Round_Table)
    self.fm_saveQandA_btn.setStyleSheet("""
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
    self.fm_saveQandA_btn.setFont(QFont("Arial", 10))
    self.fm_saveQandA_btn.clicked.connect(self.save_fm_question_to_database)

    self.fm_totalPoints_input = QLineEdit(self.Fast_Money_Round_Table)
    self.fm_totalPoints_input.setStyleSheet("background-color: #c8c8c8; color: #004aad; border: 1px solid #c8c8c8; border-radius: 5px;")
    self.fm_totalPoints_input.setFont(QFont("Arial", 10))
    self.fm_totalPoints_input.setReadOnly(True)

    self.fm_totalPoints_label = QLabel("Total:", self.Fast_Money_Round_Table)
    self.fm_totalPoints_label.setAlignment(Qt.AlignLeft)
    self.fm_totalPoints_label.setStyleSheet("color: #004aad;")
    self.fm_totalPoints_label.setFont(QFont("Arial", 10))

    # ---------------------------------------------------- About the Game Project ----------------------------------------------------

    self.About_Table = QWidget(self.family.feud.game.tab)
    self.About_Table.setStyleSheet("background-color: #f9f9f9;")

    self.about_description_textBox = QTextEdit(self.About_Table)
    self.about_description_textBox.setReadOnly(True)
    self.about_description_textBox.setStyleSheet(
        "background-color: #ffffff; color: #222222; border: 1px solid #dcdcdc; border-radius: 6px; padding: 14px;"
    )
    self.about_description_textBox.setFont(QFont("Arial", 11))
    self.about_description_textBox.setHtml("""
        <style>
            body { font-family: Arial, Helvetica, sans-serif; font-size: 13px; color: #222222; line-height: 1.6; }
            h1 { color: #004aad; font-size: 18px; margin-top: 0px; margin-bottom: 6px; }
            h2 { color: #008f4a; font-size: 14px; margin-top: 18px; margin-bottom: 8px; border-bottom: 2px solid #008f4a; padding-bottom: 3px; text-transform: uppercase; }
            h3 { color: #004aad; font-size: 13px; margin-top: 12px; margin-bottom: 4px; }
            p { margin-top: 4px; margin-bottom: 8px; }
            ul { margin-top: 4px; margin-bottom: 10px; padding-left: 20px; }
            li { margin-bottom: 5px; }
            .box { background-color: #f3f7fc; border-left: 4px solid #004aad; padding: 10px 14px; margin: 10px 0; border-radius: 3px; }
            .strike { color: #b80000; font-weight: bold; }
            .win { color: #008f4a; font-weight: bold; }
        </style>

        <h1>Family Feud+ Production System & Operator Manual</h1>
        <p><b>Family Feud+</b> is a dual-screen digital game show platform inspired by classic television quiz shows. It is engineered to host authentic Family Feud competitions for parties, live events, school tournaments, and corporate team building.</p>

        <div class="box">
            <b>System Architecture (Dual-Monitor Operation):</b><br>
            • <b>Host Control Console:</b> Operated by the Game Master to control questions, reveal answers, manage strikes, tally points, and trigger audio cues.<br>
            • <b>Audience / Projector Display:</b> Full-screen presentation windows (Title Screen, Face-Off Round Board, Fast Money Round Board) routed to a secondary display facing contestants and spectators.
        </div>

        <h2>1. Game Flow & General Rules</h2>
        <ul>
            <li><b>Teams:</b> Two competing teams (<b>Team A</b> and <b>Team B</b>), typically 3 to 5 players each.</li>
            <li><b>Structure:</b> The match consists of <b>4 Face-Off Survey Rounds</b> followed by the <b>Fast Money Bonus Finale</b>.</li>
            <li><b>Survey Answers & Points:</b> Questions have between 4 to 8 top answers from surveyed respondents. Each answer carries point values equal to the number of people who gave that answer (up to 100 points per question).</li>
            <li><b>Point Multipliers:</b>
                <ul>
                    <li><b>Rounds 1 & 2:</b> Standard single points (1×).</li>
                    <li><b>Round 3:</b> Double points (2× multiplier toggle).</li>
                    <li><b>Round 4:</b> Triple points (3× multiplier toggle).</li>
                </ul>
            </li>
            <li><b>Advancement:</b> The team with the highest total score after 4 rounds advances to the Fast Money Round.</li>
        </ul>

        <h2>2. Face-Off Round Mechanics</h2>
        <h3>A. The Podium Face-Off</h3>
        <ul>
            <li>One player from each team steps up to the podium for the new survey question.</li>
            <li>The host reads the question. The first player to buzz in provides an answer.</li>
            <li>If they give the <b>#1 top answer</b> on the board, their team immediately wins control of the question.</li>
            <li>If their answer is on the board but not #1, the opposing player gets a turn to guess. Whichever player names the higher-ranking answer wins control.</li>
            <li>The winning team chooses to <b>Play</b> (keep the question) or <b>Pass</b> (force opponents to play).</li>
        </ul>

        <h3>B. Playing the Board & Strikes</h3>
        <ul>
            <li>The playing team attempts to reveal all remaining hidden answers on the board, one member at a time. No consultation is allowed among teammates during this phase.</li>
            <li><b>Correct Answer:</b> The host clicks the corresponding answer button on the control console. The answer and points reveal on the audience screen with the good-answer chime, adding points to the round bank.</li>
            <li><b>Incorrect Answer (Strike):</b> If an answer is not on the board or time expires:
                <ul>
                    <li>The host clicks the team's <span class="strike">Strike</span> button.</li>
                    <li>A large red <b>X</b> appears centered on the audience board accompanied by the strike buzzer.</li>
                    <li>Subsequent incorrect guesses trigger <b>XX</b> (Strike 2) and <b>XXX</b> (Strike 3).</li>
                </ul>
            </li>
        </ul>

        <h3>C. The 3-Strike Steal</h3>
        <ul>
            <li>If the playing team accumulates <span class="strike">3 Strikes</span> before clearing the board, the opposing team gets <b>ONE collective opportunity to steal</b>.</li>
            <li>The opposing team confers together, and their designated captain gives a single answer.</li>
            <li><span class="win">Successful Steal:</span> If their answer is on the board, the opposing team steals ALL accumulated points in that round.</li>
            <li><span class="strike">Failed Steal:</span> If their answer is not on the board, the original playing team retains their points.</li>
        </ul>

        <h3>D. Scoring & Round Archiving</h3>
        <ul>
            <li>Click <b>Reward / Steal Points</b> under Team A or Team B to award the accumulated bank to that team.</li>
            <li>Click <b>Log, Next round</b>: Records the points gained and strikes into the persistent R1–R4 match log and automatically resets the board for the next round.</li>
        </ul>

        <h2>3. Fast Money Round Mechanics (Finale)</h2>
        <ul>
            <li><b>Participants:</b> The winning team selects two representatives (Player 1 and Player 2).</li>
            <li><b>Format:</b> Both players answer the <b>same 5 rapid-fire survey questions</b>.</li>
            <li><b>Player 1 Phase:</b>
                <ul>
                    <li>Player 1 has <b>20 seconds</b> (or 25 seconds) on the clock.</li>
                    <li>The host starts the timer and reads question 1. Player 1 gives their top answers rapidly.</li>
                    <li>Player 2 is sequestered offstage or wears soundproof headphones so they cannot hear questions or answers.</li>
                </ul>
            </li>
            <li><b>Player 2 Phase:</b>
                <ul>
                    <li>Player 2 returns and has <b>25 seconds</b> on the clock.</li>
                    <li>If Player 2 duplicates an answer given by Player 1, the buzzer sounds and the host calls "Duplicate — give another answer".</li>
                </ul>
            </li>
            <li><b>Grand Prize Target (200 Points):</b>
                <ul>
                    <li>The host reveals each player's answers and points one by one on the audience screen.</li>
                    <li>If the combined total of both players reaches <span class="win">200 points or more</span>, the team wins the Fast Money Grand Prize, triggering the victory celebration fanfare!</li>
                </ul>
            </li>
        </ul>

        <h2>4. Host Operator & Control Deck Reference</h2>
        <ul>
            <li><b>Display Selection:</b> Choose the target audience monitor from the "Choose display" dropdown on the Welcome Screen, then deploy Title Screen, Face Off Round, or Fast Money Round full screen.</li>
            <li><b>Audio Deck:</b> Trigger real-time sound cues:
                <ul>
                    <li><i>Intro Music:</i> Returning from commercial / theme music.</li>
                    <li><i>Outro Music:</i> Show conclusion soundtrack.</li>
                    <li><i>Correct Ans:</i> Signature good-answer bell chime.</li>
                    <li><i>Strike / Timer:</i> Strike buzzer and countdown audio cues.</li>
                    <li><i>Winning Sound:</i> Fast Money victory fanfare.</li>
                </ul>
            </li>
            <li><b>Question Database Management:</b>
                <ul>
                    <li><b>Auto-Load:</b> Default databases load automatically from the <code>db/</code> directory.</li>
                    <li><b>Load from file:</b> Load external custom question packs (SQLite <code>.db</code> format).</li>
                    <li><b>Manual Add / Modify:</b> Add or edit questions, answers, and points directly within the software.</li>
                    <li><b>Delete:</b> Remove questions from the active database.</li>
                </ul>
            </li>
            <li><b>Audience Board Reset:</b> Click <i>Show answer count</i> to prepare hidden answer slots on the audience screen; click <i>Clear answer count</i> to wipe the board between questions.</li>
        </ul>

        <div class="box">
            <b>Disclaimer:</b> Family Feud+ is an independent fan-made project developed for educational, party, and social entertainment purposes. It is not affiliated with, endorsed by, or associated with FremantleMedia or the official Family Feud television game show.
        </div>
    """)

    self.about_title_label = QLabel("About & Game Mechanics", self.About_Table)
    self.about_title_label.setAlignment(Qt.AlignLeft)
    self.about_title_label.setStyleSheet("color: #004aad;")
    self.about_title_label.setFont(QFont("Arial", 20, QFont.Bold))

    self.family.feud.game.tab.addTab(self.Welcome_screen_table, "Welcome Screen")

    self.family.feud.game.tab.addTab(self.Face_off_table, "Face Off Round")

    self.family.feud.game.tab.addTab(self.Fast_Money_Round_Table, "Fast Money Round")

    self.family.feud.game.tab.addTab(self.About_Table, "About")

    adjust_ui_elements(self)