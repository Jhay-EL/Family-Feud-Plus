import sys
import os
import cv2
import gc
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QFont, QCursor, QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from pathlib import Path

logging.basicConfig(level=logging.INFO)
class FaceOff_Window(QWidget):
    def __init__(self, parent=None):
        super(FaceOff_Window, self).__init__(parent)
        self.setGeometry(0, 0, 1280, 720)
        self.original_width = 1280
        self.original_height = 720
        self.ui_elements = []  # To store UI elements and their original geometry
        self.original_font_sizes = {}  # Add this line to store original font sizes
        
        # Setup background music
        self.bgm_player = QMediaPlayer()
        current_dir = Path(__file__).resolve().parent
        bgm_path = current_dir / "res" / "sound" / "faceoff_bgm.mp3"
        self.bgm_player.setMedia(QMediaContent(QUrl.fromLocalFile(str(bgm_path))))
        self.bgm_player.setVolume(1)
        self.bgm_player.play()
        
        self.gui()
        
        # Hide all preview answers by default
        for i in range(1, 9):
            rect = getattr(self, f'gw_AnsDisplay{i}')
            label = getattr(self, f'gw_AnsLabel{i}')
            rect.hide()
            label.hide()
    
    def gui(self):
        
        self.setup_video_background()
    
        self.gw_XImage = QLabel(self)
        target_height = 600
        original_ratio = 2048/2048  
        target_width = int(target_height * original_ratio)
        x_pixmap = QPixmap("res/mipmap/X.png").scaled(target_width, target_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.gw_XImage.setPixmap(x_pixmap)
        self.gw_XImage.setAlignment(Qt.AlignCenter)
        x, y = (self.width() - target_width) // 2, (self.height() - target_height) // 2
        self.gw_XImage.setGeometry(x, y, target_width, target_height)
        self.ui_elements.append((self.gw_XImage, QRect(x, y, target_width, target_height)))
        self.gw_XImage.hide()  

        self.gw_XXImage = QLabel(self)
        original_ratio = 4200/2048
        target_width = int(target_height * original_ratio)
        xx_pixmap = QPixmap("res/mipmap/XX.png").scaled(target_width, target_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.gw_XXImage.setPixmap(xx_pixmap)
        self.gw_XXImage.setAlignment(Qt.AlignCenter)
        x, y = (self.width() - target_width) // 2, (self.height() - target_height) // 2
        self.gw_XXImage.setGeometry(x, y, target_width, target_height)
        self.ui_elements.append((self.gw_XXImage, QRect(x, y, target_width, target_height)))
        self.gw_XXImage.hide()
        
        self.gw_XXXImage = QLabel(self)
        original_ratio = 6344/2048
        target_width = int(target_height * original_ratio)
        xxx_pixmap = QPixmap("res/mipmap/XXX.png").scaled(target_width, target_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.gw_XXXImage.setPixmap(xxx_pixmap)
        self.gw_XXXImage.setAlignment(Qt.AlignCenter)
        x, y = (self.width() - target_width) // 2, (self.height() - target_height) // 2
        self.gw_XXXImage.setGeometry(x, y, target_width, target_height)
        self.ui_elements.append((self.gw_XXXImage, QRect(x, y, target_width, target_height)))
        self.gw_XXXImage.hide()

#-----------------------------------------------------------------------------------------------

        self.gw_TeamAName = QLabel("Team A Name", self)
        self.gw_TeamAName.setAlignment(Qt.AlignCenter)  # Set alignment to center
        self.gw_TeamAName.setStyleSheet("color: #ffffff;")
        self.gw_TeamAName.setFont(QFont("Consolas", 30, QFont.Bold))
        self.gw_TeamAName.setCursor(QCursor(Qt.ArrowCursor))
        self.gw_TeamAName.setGeometry(20, 35, 390, 72)  # Reduced y by 10
        self.ui_elements.append((self.gw_TeamAName, QRect(20, 35, 390, 72)))
    
        # Team B Name Label
        self.gw_TeamBName = QLabel("Team B Name", self)
        self.gw_TeamBName.setAlignment(Qt.AlignCenter)  # Set alignment to center
        self.gw_TeamBName.setStyleSheet("color: #ffffff;")
        self.gw_TeamBName.setFont(QFont("Consolas", 30, QFont.Bold))
        self.gw_TeamBName.setCursor(QCursor(Qt.ArrowCursor))
        self.gw_TeamBName.setGeometry(870, 35, 390, 72)  # Reduced y by 10
        self.ui_elements.append((self.gw_TeamBName, QRect(870, 35, 390, 72)))
    
        # Points Label
        self.gw_Points = QLabel("", self)
        self.gw_Points.setAlignment(Qt.AlignCenter)  # Set alignment to center
        self.gw_Points.setStyleSheet("color: #ffffff;")
        self.gw_Points.setFont(QFont("Consolas", 72))
        self.gw_Points.setCursor(QCursor(Qt.ArrowCursor))
        self.gw_Points.setGeometry(560, 45, 160, 172)  # Reduced y by 10
        self.ui_elements.append((self.gw_Points, QRect(560, 45, 160, 172)))
    
        # Team A Points Label
        self.gw_TeamAPoints = QLabel("", self)
        self.gw_TeamAPoints.setAlignment(Qt.AlignCenter)  # Set alignment to center
        self.gw_TeamAPoints.setStyleSheet("color: #ffffff;")
        self.gw_TeamAPoints.setFont(QFont("Consolas", 50))
        self.gw_TeamAPoints.setCursor(QCursor(Qt.ArrowCursor))
        self.gw_TeamAPoints.setGeometry(42, 140, 150, 92)  # No change needed
        self.ui_elements.append((self.gw_TeamAPoints, QRect(42, 140, 150, 92)))
    
        # Team B Points Label
        self.gw_TeamBPoints = QLabel("", self)
        self.gw_TeamBPoints.setAlignment(Qt.AlignCenter)  # Set alignment to center
        self.gw_TeamBPoints.setStyleSheet("color: #ffffff;")
        self.gw_TeamBPoints.setFont(QFont("Consolas", 50))
        self.gw_TeamBPoints.setCursor(QCursor(Qt.ArrowCursor))
        self.gw_TeamBPoints.setGeometry(1088, 140, 150, 92)  # No change needed
        self.ui_elements.append((self.gw_TeamBPoints, QRect(1088, 140, 150, 92)))

#-----------------------------------------------------------------------------------------------

        # Answer Labels and Points
        Preview_answers = [("1", 330, 279), ("2", 330, 376), ("3", 330, 472), ("4", 330, 568),
                   ("5", 880, 279), ("6", 880, 376), ("7", 880, 472), ("8", 880, 568)]  
        
        for i, (txt, x, y) in enumerate(Preview_answers):
            # Create the number label
            label = QLabel(txt, self)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: #004aad;") # Changed to black for better visibility on white background
            label.setFont(QFont("Arial", 30, QFont.Bold))
            label.setCursor(QCursor(Qt.ArrowCursor))
            
            # Create background rectangle
            rect = QWidget(self)
            rect.setStyleSheet("""
                QWidget {
                    background-color: #FFFFFF;
                    border-radius: 25px;
                    border: 4px solid #f9b451;
                }
            """)
            rect_width = 50
            rect.setGeometry(x, y, rect_width, 50)
            
            # Position label on top of rectangle
            label.setGeometry(x, y, rect_width, 50)
            label.raise_()
            
            # Store both widgets
            self.ui_elements.append((rect, QRect(x, y, rect_width, 50)))
            self.ui_elements.append((label, QRect(x, y, rect_width, 50)))
            
            # Store references
            setattr(self, f'gw_AnsDisplay{i+1}', rect)
            setattr(self, f'gw_AnsLabel{i+1}', label)

#-----------------------------------------------------------------------------------------------

        # Answer Labels and Points
        answers = [("", 120, 270), ("", 120, 367), 
                   ("", 120, 463), ("", 120, 560),
                   ("", 670, 270), ("", 670, 367),  
                   ("", 670, 463), ("", 670, 560)]  
    
        points_positions = [(510, 270), (510, 367), (510, 463), (510, 560),  # Reduced y by 10 for gw_Points2
                            (1070, 270), (1070, 367), (1070, 463), (1070, 560)]  # Reduced y by 10 for gw_Points6

        for i, (text, x, y) in enumerate(answers):
            label = QLabel(text, self)
            label.setAlignment(Qt.AlignCenter)  # Set alignment to center
            label.setStyleSheet("color: #ffffff;")
            label.setFont(QFont("Consolas", 30))
            label.setCursor(QCursor(Qt.ArrowCursor))
            label_width = 390 if x == 120 else 400
            label.setGeometry(x, y, label_width, 62)
            self.ui_elements.append((label, QRect(x, y, label_width, 62)))
            setattr(self, f'gw_Ans{i+1}', label)
    
            points_label = QLabel("", self)
            points_label.setAlignment(Qt.AlignCenter)  # Set alignment to center
            points_label.setStyleSheet("color: #ffffff;")
            points_label.setFont(QFont("Consolas", 30))
            points_label.setCursor(QCursor(Qt.ArrowCursor))
            px, py = points_positions[i]
            points_label.setGeometry(px, py, 100, 62)
            self.ui_elements.append((points_label, QRect(px, py, 100, 62)))
            setattr(self, f'gw_Points{i+1}', points_label)
    
        # After creating each label, store its original font size
        # Add this after each label creation and font setting
        for widget, _ in self.ui_elements:
            self.original_font_sizes[widget] = widget.font().pointSize()
    
    def setup_video_background(self):
        # Create a QLabel to display the video
        self.video_label = QLabel(self)
        self.video_label.setGeometry(0, 0, 1280, 720)
        self.video_label.lower()  # Ensure the video label is behind other widgets

    # Instead of using __file__, use sys.argv[0] to get current directory
        current_dir = Path(__file__).resolve().parent
        self.video_path = current_dir / "res" / "bg" / "FaceOff Round.mp4"

        # Open video capture
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            logging.error(f"Cannot open video file: {self.video_path}")
        # Instead of sys.exit(), you might raise an exception or handle the error gracefully.
        # sys.exit()
            return

        # Get frame rate of the video
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        if self.fps == 0:
            self.fps = 30  # Default to 30 fps if unable to get fps from video
        self.frame_delay = int(1000 / self.fps)

        # Start timer to play video
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)
        self.timer.start(self.frame_delay)

        # Add cleanup timer
        self.cleanup_timer = QTimer(self)
        self.cleanup_timer.timeout.connect(self.perform_cleanup)
        self.cleanup_timer.start(30000)  # Cleanup every 30 seconds

        # Handle window close event
        self.destroyed.connect(self.cleanup_on_close)
        
    def next_frame(self):
        try:
            ret, frame = self.cap.read()
            if not ret:
                # Loop the video
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
                if not ret:
                    logging.error("Cannot read video frames.")
                    self.timer.stop()
                    return
                
            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to QImage
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
            # Scale image to fill the window completely
            window_size = self.size()
            qimg_scaled = qimg.scaled(window_size, 
                                    Qt.IgnoreAspectRatio,  # Changed to ignore aspect ratio
                                    Qt.SmoothTransformation)
            
            # Set the final pixmap
            self.video_label.setPixmap(QPixmap.fromImage(qimg_scaled))
            
        except Exception as e:
            logging.error(f"Error in next_frame: {e}")
    
    def perform_cleanup(self):
        """Periodic cleanup to prevent memory buildup"""
        try:
            gc.collect()
            logging.info("Cleanup performed")
        except Exception as e:
            logging.error(f"Error in cleanup: {e}")
    
    def cleanup_on_close(self):
        """Clean up resources when window is closed"""
        try:
            self.timer.stop()
            self.cleanup_timer.stop()
            self.bgm_player.stop()
            if self.cap is not None:
                self.cap.release()
            gc.collect()
        except Exception as e:
            logging.error(f"Error in cleanup_on_close: {e}")
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        # Calculate scaling factors
        width_ratio = self.width() / self.original_width
        height_ratio = self.height() / self.original_height
        
        # Update positions and sizes using both ratios independently
        for widget, rect in self.ui_elements:
            # Scale position and size using respective ratios
            new_rect = QRect(
                int(rect.x() * width_ratio),
                int(rect.y() * height_ratio),
                int(rect.width() * width_ratio),
                int(rect.height() * height_ratio)
            )
            widget.setGeometry(new_rect)
            
            # Scale font size using the average of both ratios
            scale_factor = (width_ratio + height_ratio) / 2
            original_size = self.original_font_sizes[widget]
            new_font_size = int(original_size * scale_factor)  # Convert to integer
            
            # Set reasonable limits for font scaling
            min_size = 8  # Minimum readable font size
            max_size = original_size * 2  # Maximum size is 200% of original
            
            new_font_size = max(min_size, min(new_font_size, max_size))
            
            font = widget.font()
            font.setPointSize(new_font_size)  # Use setPointSize instead of setPointSizeF
            widget.setFont(font)
        
        # Resize video label to fill entire window
        self.video_label.setGeometry(0, 0, self.width(), self.height())
    
    def closeEvent(self, event):
        """Clean up resources when window is closed"""
        self.cleanup_on_close()
        event.accept()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = FaceOff_Window()
    a.show()
    sys.exit(app.exec_())