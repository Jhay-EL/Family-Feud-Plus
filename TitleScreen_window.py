from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import cv2
import os
import sys
import gc

class TitleScreen(QMainWindow):
    def __init__(self, parent=None):
        super(TitleScreen, self).__init__(parent)
        self.setWindowTitle("Title Screen")
        self.setMinimumSize(1280, 720)
        self.set_icon()
        self.capture = None
        self.imgtk = None
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border: none;")

        self.central_widget = QWidget(self)
        self.central_widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.video_label = QLabel(self.central_widget)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.video_label)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.video_path = os.path.join(current_dir, "res", "bg", "Title Screen.mp4")

        self.load_video()

        # Initialize media player
        self.media_player = QMediaPlayer()
        self.setup_audio()

    def load_video(self):
        # Set video capture properties for better performance
        self.capture = cv2.VideoCapture(self.video_path)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 3)

        if not self.capture.isOpened():
            QMessageBox.critical(self, "Error", f"Cannot open video file: {self.video_path}")
            return

        # Get video properties
        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.frame_delay = int(1000 / self.fps)

        self.play_video()

    def play_video(self):
        if self.capture is None:
            return

        ret, frame = self.capture.read()
        if not ret:
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.capture.read()
            if not ret:
                return

        try:
            # Get the current size of the central widget
            current_width = self.central_widget.width()
            current_height = self.central_widget.height()

            # Optimize frame processing
            frame = cv2.resize(frame, (current_width, current_height), interpolation=cv2.INTER_LINEAR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert frame to QImage
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.imgtk = QPixmap.fromImage(img)
            self.video_label.setPixmap(self.imgtk)

            # Schedule next frame using calculated delay
            QTimer.singleShot(self.frame_delay, self.play_video)

        except Exception as e:
            print(f"Error processing frame: {str(e)}")

    def setup_audio(self):
        """Setup and schedule the intro audio"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.first_audio_path = os.path.join(current_dir, "res", "sound", "family-feud-returning-from-commercial.mp3")
            self.second_audio_path = os.path.join(current_dir, "res", "sound", "family-feud-theme.mp3")
            
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.first_audio_path)))
            
            # Schedule first audio playback with 10ms delay
            QTimer.singleShot(10, self.play_first_audio)
        except Exception as e:
            print(f"Error setting up audio: {str(e)}")

    def play_first_audio(self):
        """Play the first intro audio and schedule second audio"""
        try:
            self.media_player.play()
            # Connect to mediaStatusChanged to detect when first audio finishes
            self.media_player.mediaStatusChanged.connect(self.on_first_audio_finished)
        except Exception as e:
            print(f"Error playing first audio: {str(e)}")
            
    def on_first_audio_finished(self, status):
        """Handle first audio completion and start second audio"""
        if status == QMediaPlayer.EndOfMedia:
            # Disconnect to avoid multiple connections
            self.media_player.mediaStatusChanged.disconnect(self.on_first_audio_finished)
            # Set and play second audio
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.second_audio_path)))
            self.media_player.play()

    def closeEvent(self, event):
        """Clean up resources when window is closed"""
        try:
            if self.capture is not None:
                self.capture.release()
            self.media_player.stop()  # Stop audio playback
            self.imgtk = None
            gc.collect()
        except Exception as e:
            print(f"Error in closeEvent: {str(e)}")
        event.accept()

    def set_icon(self):
        """Set the window icon"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(current_dir, "res", "mipmap", "Family-Feud-Logo.ico")
            self.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            print(f"Error setting icon: {str(e)}")

# Main execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = TitleScreen()
    a.show()
    sys.exit(app.exec_())
