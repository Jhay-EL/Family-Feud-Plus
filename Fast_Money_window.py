from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import sys
import os

class FastMoneyWindow(QWidget):
    BASE_WIDTH = 1280
    BASE_HEIGHT = 720

    def __init__(self, parent=None):
        super(FastMoneyWindow, self).__init__(parent)
        self.original_geometries = {}
        self.gui()

    def gui(self):
        # Set geometry and window title
        self.setGeometry(100, 100, self.BASE_WIDTH, self.BASE_HEIGHT)
        self.setWindowTitle("Fast Money Window")

        # Set background image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_image_path = os.path.join(current_dir, "res", "bg", "Fast Money Round.png")
        self.bg_pixmap = QPixmap(bg_image_path)
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(self.bg_pixmap)
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(0, 0, self.BASE_WIDTH, self.BASE_HEIGHT)

        # Create labels to replicate Tkinter layout
        self.fm_countdown = QLabel("", self)
        self.fm_countdown.setGeometry(561, 32, 180, 75)
        self.fm_countdown.setFont(QFont("Consolas", 50))
        self.fm_countdown.setStyleSheet("color: #ffffff;")
        self.fm_countdown.setAlignment(Qt.AlignCenter)

        # Player 1 Answers
        self.fmp1_ans1 = QLabel("", self)
        self.fmp1_ans1.setGeometry(80, 129, 440, 72)
        self.fmp1_ans1.setFont(QFont("Consolas", 30))
        self.fmp1_ans1.setStyleSheet("color: #ffffff;")
        self.fmp1_ans1.setAlignment(Qt.AlignCenter)

        self.fmp1_ans2 = QLabel("", self)
        self.fmp1_ans2.setGeometry(80, 225, 440, 72)
        self.fmp1_ans2.setFont(QFont("Consolas", 30))
        self.fmp1_ans2.setStyleSheet("color: #ffffff;")
        self.fmp1_ans2.setAlignment(Qt.AlignCenter)

        self.fmp1_ans3 = QLabel("", self)
        self.fmp1_ans3.setGeometry(80, 320, 440, 72)
        self.fmp1_ans3.setFont(QFont("Consolas", 30))
        self.fmp1_ans3.setStyleSheet("color: #ffffff;")
        self.fmp1_ans3.setAlignment(Qt.AlignCenter)

        self.fmp1_ans4 = QLabel("", self)
        self.fmp1_ans4.setGeometry(80, 416, 440, 72)
        self.fmp1_ans4.setFont(QFont("Consolas", 30))
        self.fmp1_ans4.setStyleSheet("color: #ffffff;")
        self.fmp1_ans4.setAlignment(Qt.AlignCenter)

        self.fmp1_ans5 = QLabel("", self)
        self.fmp1_ans5.setGeometry(80, 512, 440, 72)
        self.fmp1_ans5.setFont(QFont("Consolas", 30))
        self.fmp1_ans5.setStyleSheet("color: #ffffff;")
        self.fmp1_ans5.setAlignment(Qt.AlignCenter)

        # Player 2 Answers
        self.fmp2_ans1 = QLabel("", self)
        self.fmp2_ans1.setGeometry(690, 129, 430, 72)
        self.fmp2_ans1.setFont(QFont("Consolas", 30))
        self.fmp2_ans1.setStyleSheet("color: #ffffff;")
        self.fmp2_ans1.setAlignment(Qt.AlignCenter)

        self.fmp2_ans2 = QLabel("", self)
        self.fmp2_ans2.setGeometry(690, 225, 440, 72)
        self.fmp2_ans2.setFont(QFont("Consolas", 30))
        self.fmp2_ans2.setStyleSheet("color: #ffffff;")
        self.fmp2_ans2.setAlignment(Qt.AlignCenter)

        self.fmp2_ans3 = QLabel("", self)
        self.fmp2_ans3.setGeometry(690, 320, 440, 72)
        self.fmp2_ans3.setFont(QFont("Consolas", 30))
        self.fmp2_ans3.setStyleSheet("color: #ffffff;")
        self.fmp2_ans3.setAlignment(Qt.AlignCenter)

        self.fmp2_ans4 = QLabel("", self)
        self.fmp2_ans4.setGeometry(690, 416, 440, 72)
        self.fmp2_ans4.setFont(QFont("Consolas", 30))
        self.fmp2_ans4.setStyleSheet("color: #ffffff;")
        self.fmp2_ans4.setAlignment(Qt.AlignCenter)

        self.fmp2_ans5 = QLabel("", self)
        self.fmp2_ans5.setGeometry(690, 512, 440, 72)
        self.fmp2_ans5.setFont(QFont("Consolas", 30))
        self.fmp2_ans5.setStyleSheet("color: #ffffff;")
        self.fmp2_ans5.setAlignment(Qt.AlignCenter)

        # Player 1 Points
        self.fmp1_point1 = QLabel("", self)
        self.fmp1_point1.setGeometry(553, 129, 70, 72)
        self.fmp1_point1.setFont(QFont("Consolas", 30))
        self.fmp1_point1.setStyleSheet("color: #ffffff;")
        self.fmp1_point1.setAlignment(Qt.AlignCenter)

        self.fmp1_point2 = QLabel("", self)
        self.fmp1_point2.setGeometry(553, 225, 70, 72)
        self.fmp1_point2.setFont(QFont("Consolas", 30))
        self.fmp1_point2.setStyleSheet("color: #ffffff;")
        self.fmp1_point2.setAlignment(Qt.AlignCenter)

        self.fmp1_point3 = QLabel("", self)
        self.fmp1_point3.setGeometry(553, 320, 70, 72)
        self.fmp1_point3.setFont(QFont("Consolas", 30))
        self.fmp1_point3.setStyleSheet("color: #ffffff;")
        self.fmp1_point3.setAlignment(Qt.AlignCenter)

        self.fmp1_point4 = QLabel("", self)
        self.fmp1_point4.setGeometry(553, 416, 70, 72)
        self.fmp1_point4.setFont(QFont("Consolas", 30))
        self.fmp1_point4.setStyleSheet("color: #ffffff;")
        self.fmp1_point4.setAlignment(Qt.AlignCenter)

        self.fmp1_point5 = QLabel("", self)
        self.fmp1_point5.setGeometry(553, 512, 70, 72)
        self.fmp1_point5.setFont(QFont("Consolas", 30))
        self.fmp1_point5.setStyleSheet("color: #ffffff;")
        self.fmp1_point5.setAlignment(Qt.AlignCenter)

        # Player 2 Points
        self.fmp2_point1 = QLabel("", self)
        self.fmp2_point1.setGeometry(1160, 129, 70, 72)
        self.fmp2_point1.setFont(QFont("Consolas", 30))
        self.fmp2_point1.setStyleSheet("color: #ffffff;")
        self.fmp2_point1.setAlignment(Qt.AlignCenter)

        self.fmp2_point2 = QLabel("", self)
        self.fmp2_point2.setGeometry(1160, 225, 70, 72)
        self.fmp2_point2.setFont(QFont("Consolas", 30))
        self.fmp2_point2.setStyleSheet("color: #ffffff;")
        self.fmp2_point2.setAlignment(Qt.AlignCenter)

        self.fmp2_point3 = QLabel("", self)
        self.fmp2_point3.setGeometry(1160, 320, 70, 72)
        self.fmp2_point3.setFont(QFont("Consolas", 30))
        self.fmp2_point3.setStyleSheet("color: #ffffff;")
        self.fmp2_point3.setAlignment(Qt.AlignCenter)

        self.fmp2_point4 = QLabel("", self)
        self.fmp2_point4.setGeometry(1160, 416, 70, 72)
        self.fmp2_point4.setFont(QFont("Consolas", 30))
        self.fmp2_point4.setStyleSheet("color: #ffffff;")
        self.fmp2_point4.setAlignment(Qt.AlignCenter)

        self.fmp2_point5 = QLabel("", self)
        self.fmp2_point5.setGeometry(1160, 512, 70, 72)
        self.fmp2_point5.setFont(QFont("Consolas", 30))
        self.fmp2_point5.setStyleSheet("color: #ffffff;")
        self.fmp2_point5.setAlignment(Qt.AlignCenter)

        # Total Points
        self.fm_TotalPlayer_Point = QLabel("", self)
        self.fm_TotalPlayer_Point.setGeometry(910, 618, 300, 72)
        self.fm_TotalPlayer_Point.setFont(QFont("Consolas", 30))
        self.fm_TotalPlayer_Point.setStyleSheet("color: #ffffff;")
        self.fm_TotalPlayer_Point.setAlignment(Qt.AlignCenter)

        # Store original geometries
        self.store_original_geometries()

    def store_original_geometries(self):
        """Store the original geometries of all widgets."""
        widgets = [
            self.bg_label,
            self.fm_countdown,
            self.fmp1_ans1,
            self.fmp1_ans2,
            self.fmp1_ans3,
            self.fmp1_ans4,
            self.fmp1_ans5,
            self.fmp2_ans1,
            self.fmp2_ans2,
            self.fmp2_ans3,
            self.fmp2_ans4,
            self.fmp2_ans5,
            self.fmp1_point1,
            self.fmp1_point2,
            self.fmp1_point3,
            self.fmp1_point4,
            self.fmp1_point5,
            self.fmp2_point1,
            self.fmp2_point2,
            self.fmp2_point3,
            self.fmp2_point4,
            self.fmp2_point5,
            self.fm_TotalPlayer_Point,
        ]

        for widget in widgets:
            geom = widget.geometry()
            self.original_geometries[widget] = geom

    def resizeEvent(self, event):
        """Handle the window resize to make UI responsive."""
        new_width = self.width()
        new_height = self.height()

        # Calculate scale factors
        x_scale = new_width / self.BASE_WIDTH
        y_scale = new_height / self.BASE_HEIGHT

        for widget, geom in self.original_geometries.items():
            new_x = int(geom.x() * x_scale)
            new_y = int(geom.y() * y_scale)
            new_w = int(geom.width() * x_scale)
            new_h = int(geom.height() * y_scale)
            widget.setGeometry(new_x, new_y, new_w, new_h)

        # Update background image
        scaled_pixmap = self.bg_pixmap.scaled(new_width, new_height, aspectRatioMode=1)
        self.bg_label.setPixmap(scaled_pixmap)

        super().resizeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FastMoneyWindow()
    window.show()
    sys.exit(app.exec_())