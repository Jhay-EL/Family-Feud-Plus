from PyQt5.QtCore import QRect, Qt  # Correct import for Qt
from PyQt5.QtGui import QPixmap

def adjust_ui_elements(widget):
    # Get the current size of the central widget
    central_width = widget.ControlPanel_Window.width()
    central_height = widget.ControlPanel_Window.height()

    # Define a proper stylesheet for QComboBox
    combobox_style = """
        QComboBox {
            background-color: #ffffff;
            color: #004aad;
            border: 2px solid #008f4a;
            border-radius: 5px;
            padding: 2px 24px 2px 8px;
            font-family: Arial;
            font-size: 11px;
            font-weight: bold;
        }
        QComboBox:hover {
            border: 2px solid #00a65a;
            background-color: #f7f7f7;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 22px;
            border-left: 1px solid #008f4a;
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
        }
        QComboBox::down-arrow {
            width: 0;
            height: 0;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 6px solid #004aad;
        }
    """

    # Apply the stylesheet to the combobox
    if hasattr(widget, 'display') and hasattr(widget.display, 'selection') and hasattr(widget.display.selection, 'comboBox'):
        widget.display.selection.comboBox.setStyleSheet(combobox_style)

    # Set the geometry for the combobox
    widget.display.selection.comboBox.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.555),
            int(central_width * 0.19),
            int(central_height * 0.044)
        )
    )

    # Adjust the QTabWidget to fill the central widget
    widget.family.feud.game.tab.setGeometry(QRect(0, 0, central_width, central_height))

    # Adjust all table pages to fit within the QTabWidget
    for table_attr in ['Welcome_screen_table', 'Face_off_table', 'Fast_Money_Round_Table', 'About_Table']:
        if hasattr(widget, table_attr):
            getattr(widget, table_attr).setGeometry(QRect(0, 0, central_width - 4, central_height - 35))

    # Adjust the welcome screen image proportionally
    image_width = int(central_width * 0.63)
    image_height = central_height - 11
    image_x = int(central_width * 0.37)
    widget.welcomeScreen.image.setGeometry(QRect(image_x, -10, image_width, image_height))

    # Rescale the pixmap to fit the new size only if the size has changed
    current_size = widget.welcomeScreen.image.size()
    if not widget.welcomeScreen.image.pixmap().isNull() and current_size != widget.welcomeScreen.image.pixmap().size():
        pixmap = QPixmap("res/bg/Welcome Screen BG.png")
        scaled_pixmap = pixmap.scaled(
            current_size,
            Qt.KeepAspectRatioByExpanding,  # Changed from KeepAspectRatio to KeepAspectRatioByExpanding
            Qt.SmoothTransformation
        )
        
        # Center and crop the scaled pixmap if needed
        if scaled_pixmap.width() > current_size.width() or scaled_pixmap.height() > current_size.height():
            x = max(0, (scaled_pixmap.width() - current_size.width()) // 2)
            y = max(0, (scaled_pixmap.height() - current_size.height()) // 2)
            scaled_pixmap = scaled_pixmap.copy(
                x, y, 
                min(scaled_pixmap.width(), current_size.width()),
                min(scaled_pixmap.height(), current_size.height())
            )
            
        widget.welcomeScreen.image.setPixmap(scaled_pixmap)

    # Adjust buttons proportionally
    widget.game.mechanics.btn.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.350),  # Added 5 points
            int(central_width * 0.19),
            int(central_height * 0.044)
        )
    )
    widget.deploy.titleScreen.btn.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.183),  # Added 5 points
            int(central_width * 0.19),
            int(central_height * 0.044)
        )
    )
    widget.deploy.faceOff.btn.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.238),  # Added 5 points
            int(central_width * 0.19),
            int(central_height * 0.044)
        )
    )
    widget.deploy.fastMoney.btn.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.294),  # Added 5 points
            int(central_width * 0.19),
            int(central_height * 0.044)
        )
    )
    widget.display.selection.comboBox.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.530),  # Added 5 points
            int(central_width * 0.19),
            int(central_height * 0.044)
        )
    )
    widget.welcome.screen.title.label.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.020),  # Added 5 points
            int(central_width * 0.15),
            int(central_height * 0.05)
        )
    )
    widget.welcome.screen.description.label.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.065),  # Added 5 points
            int(central_width * 0.33),
            int(central_height * 0.025)
        )
    )
    widget.ws.force.quit.btn.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.815),  # Added 5 points
            int(central_width * 0.19),
            int(central_height * 0.05)
        )
    )
    widget.select.the.display.label.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.495),  # Added 5 points
            int(central_width * 0.29),
            int(central_height * 0.025)
        )
    )
#------------------------------------ Face Off table elements ------------------------------------
    widget.enter_names_label.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.082),
            int(central_width * 0.32),
            int(central_height * 0.025)
        )
    )
    widget.team_A_name_input.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.114),
            int(central_width * 0.15),
            int(central_height * 0.044)
        )
    )
    widget.team_A_name_input.setAlignment(Qt.AlignCenter)
    
    widget.team_B_name_input.setGeometry(
        QRect(
            int(central_width * 0.21),
            int(central_height * 0.114),
            int(central_width * 0.15),
            int(central_height * 0.044)
        )
    )
    widget.team_B_name_input.setAlignment(Qt.AlignCenter)
    
    widget.team_A_points_label.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.183),
            int(central_width * 0.15),
            int(central_height * 0.025)
        )
    )
    widget.points_box_A.setGeometry(
        QRect(
            int(central_width * 0.13),
            int(central_height * 0.175),
            int(central_width * 0.06),
            int(central_height * 0.044)
        )
    )
    widget.points_box_A.setAlignment(Qt.AlignCenter)
    
    widget.team_B_points_label.setGeometry(
        QRect(
            int(central_width * 0.21),
            int(central_height * 0.183),
            int(central_width * 0.15),
            int(central_height * 0.025)
        )
    )
    widget.points_box_B.setGeometry(
        QRect(
            int(central_width * 0.30),
            int(central_height * 0.175),
            int(central_width * 0.06),
            int(central_height * 0.044)
        )
    )
    widget.points_box_B.setAlignment(Qt.AlignCenter)
    
    widget.team_A_strikes_label.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.245),
            int(central_width * 0.15),
            int(central_height * 0.025)
        )
    )
    widget.strike_box_A.setGeometry(
        QRect(
            int(central_width * 0.13),
            int(central_height * 0.237),
            int(central_width * 0.06),
            int(central_height * 0.044)
        )
    )
    widget.strike_box_A.setAlignment(Qt.AlignCenter)

    widget.team_B_strikes_label.setGeometry(
        QRect(
            int(central_width * 0.21),
            int(central_height * 0.245),
            int(central_width * 0.15),
            int(central_height * 0.025)
        )
    )
    widget.strike_box_B.setGeometry(
        QRect(
            int(central_width * 0.30),
            int(central_height * 0.237),
            int(central_width * 0.06),
            int(central_height * 0.044)
        )
    )
    widget.strike_box_B.setAlignment(Qt.AlignCenter)

    widget.A_reward_btn.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.308),
            int(central_width * 0.15),
            int(central_height * 0.044)
        )
    )
    widget.B_reward_btn.setGeometry(
        QRect(
            int(central_width * 0.21),
            int(central_height * 0.308),
            int(central_width * 0.15),
            int(central_height * 0.044)
        )
    )
    widget.A_strike_btn.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.364),
            int(central_width * 0.08),
            int(central_height * 0.044)
        )
    )
    widget.B_strike_btn.setGeometry(
        QRect(
            int(central_width * 0.21),
            int(central_height * 0.364),
            int(central_width * 0.08),
            int(central_height * 0.044)
        )
    )
    widget.B_points_label.setGeometry(
        QRect(
            int(central_width * 0.24),
            int(central_height * 0.4335),
            int(central_width * 0.05),
            int(central_height * 0.025)
        )
    )
    widget.A_points_label.setGeometry(
        QRect(
            int(central_width * 0.07),
            int(central_height * 0.4335),
            int(central_width * 0.06),
            int(central_height * 0.025)
        )
    )
    widget.B_round1_points_box.setGeometry(
        QRect(
            int(central_width * 0.24),
            int(central_height * 0.475),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.B_round1_points_box.setAlignment(Qt.AlignCenter)

    widget.A_round1_points_box.setGeometry(
        QRect(
            int(central_width * 0.07),
            int(central_height * 0.475),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.A_round1_points_box.setAlignment(Qt.AlignCenter)

    widget.B_round1_strike_box.setGeometry(
        QRect(
            int(central_width * 0.31),
            int(central_height * 0.475),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.B_round1_strike_box.setAlignment(Qt.AlignCenter)

    widget.A_round1_strike_box.setGeometry(
        QRect(
            int(central_width * 0.14),
            int(central_height * 0.475),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.A_round1_strike_box.setAlignment(Qt.AlignCenter)

    widget.B_round2_points_box.setGeometry(
        QRect(
            int(central_width * 0.24),
            int(central_height * 0.531),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.B_round2_points_box.setAlignment(Qt.AlignCenter)

    widget.A_round2_points_box.setGeometry(
        QRect(
            int(central_width * 0.07),
            int(central_height * 0.531),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.A_round2_points_box.setAlignment(Qt.AlignCenter)

    widget.B_round2_strike_box.setGeometry(
        QRect(
            int(central_width * 0.31),
            int(central_height * 0.531),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.B_round2_strike_box.setAlignment(Qt.AlignCenter)

    widget.A_round2_strike_box.setGeometry(
        QRect(
            int(central_width * 0.14),
            int(central_height * 0.531),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.A_round2_strike_box.setAlignment(Qt.AlignCenter)
    
    widget.B_round3_points_box.setGeometry(
        QRect(
            int(central_width * 0.24),
            int(central_height * 0.586),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.B_round3_points_box.setAlignment(Qt.AlignCenter)

    #------------------------------------A Round labels ------------------------------------
    widget.A_round1_label.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.489),
            int(central_width * 0.02),
            int(central_height * 0.025)
        )
    )    
    widget.A_round2_label.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.5445),
            int(central_width * 0.02),
            int(central_height * 0.025)
        )
    )    
    widget.A_round3_label.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.600),
            int(central_width * 0.02),
            int(central_height * 0.025)
        )
    )
    widget.A_round4_label.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.6555),
            int(central_width * 0.02),
            int(central_height * 0.025)
        )
    )
    #------------------------------------B Round labels ------------------------------------
    widget.B_round1_label.setGeometry(
        QRect(
            int(central_width * 0.21),
            int(central_height * 0.489),
            int(central_width * 0.02),
            int(central_height * 0.025)
        )
    )
    widget.B_round2_label.setGeometry(
        QRect(
            int(central_width * 0.21),
            int(central_height * 0.5445),
            int(central_width * 0.02),
            int(central_height * 0.025)
        )
    )
    widget.B_round3_label.setGeometry(
        QRect(
            int(central_width * 0.21),
            int(central_height * 0.600),
            int(central_width * 0.02),
            int(central_height * 0.025)
        )
    )
    widget.B_round4_label.setGeometry(
        QRect(
            int(central_width * 0.21),
            int(central_height * 0.6555),
            int(central_width * 0.02),
            int(central_height * 0.025)
        )
    )    
    #------------------------------------B Round points boxes ------------------------------------

    widget.A_round3_points_box.setGeometry(
        QRect(
            int(central_width * 0.07),
            int(central_height * 0.586),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.A_round3_points_box.setAlignment(Qt.AlignCenter)

    widget.B_round3_strike_box.setGeometry(
        QRect(
            int(central_width * 0.31),
            int(central_height * 0.586),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.B_round3_strike_box.setAlignment(Qt.AlignCenter)

    widget.A_round3_strike_box.setGeometry(
        QRect(
            int(central_width * 0.14),
            int(central_height * 0.586),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.A_round3_strike_box.setAlignment(Qt.AlignCenter)
    widget.B_round4_points_box.setGeometry(
        QRect(
            int(central_width * 0.24),
            int(central_height * 0.642),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.B_round4_points_box.setAlignment(Qt.AlignCenter)

    widget.A_round4_points_box.setGeometry(
        QRect(
            int(central_width * 0.07),
            int(central_height * 0.642),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.A_round4_points_box.setAlignment(Qt.AlignCenter)

    widget.B_round4_strike_box.setGeometry(
        QRect(
            int(central_width * 0.31),
            int(central_height * 0.642),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.B_round4_strike_box.setAlignment(Qt.AlignCenter)

    widget.A_round4_strike_box.setGeometry(
        QRect(
            int(central_width * 0.14),
            int(central_height * 0.642),
            int(central_width * 0.05),
            int(central_height * 0.044)
        )
    )
    widget.A_round4_strike_box.setAlignment(Qt.AlignCenter)

    widget.B_strikes_label.setGeometry(
        QRect(
            int(central_width * 0.31),
            int(central_height * 0.4335),
            int(central_width * 0.04),
            int(central_height * 0.025)
        )
    )
    widget.A_strikes_label.setGeometry(
        QRect(
            int(central_width * 0.14),
            int(central_height * 0.4335),
            int(central_width * 0.04),
            int(central_height * 0.025)
        )
    )
    widget.family_feud_faceOff_round_label.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.020),
            int(central_width * 0.36),
            int(central_height * 0.05)
        )
    )
    widget.game_questions_view_label.setGeometry(
        QRect(
            int(central_width * 0.38),
            int(central_height * 0.082),
            int(central_width * 0.32),
            int(central_height * 0.025)
        )
    )
    widget.game_questions_input.setGeometry(
        QRect(
            int(central_width * 0.38),
            int(central_height * 0.114),
            int(central_width * 0.33),
            int(central_height * 0.167)
        )
    )
    widget.ans1_btn.setGeometry(
        QRect(
            int(central_width * 0.38),
            int(central_height * 0.308),
            int(central_width * 0.25),
            int(central_height * 0.044)
        )
    )
    widget.point1_input.setGeometry(
        QRect(
            int(central_width * 0.65),
            int(central_height * 0.308),
            int(central_width * 0.06),
            int(central_height * 0.044)
        )
    )
    widget.point1_input.setAlignment(Qt.AlignCenter)

    widget.ans2_btn.setGeometry(
        QRect(
            int(central_width * 0.38),
            int(central_height * 0.364),
            int(central_width * 0.25),
            int(central_height * 0.044)
        )
    )
    widget.point2_input.setGeometry(
        QRect(
            int(central_width * 0.65),
            int(central_height * 0.364),
            int(central_width * 0.06),
            int(central_height * 0.044)
        )
    )
    widget.point2_input.setAlignment(Qt.AlignCenter)

    widget.ans3_btn.setGeometry(
        QRect(
            int(central_width * 0.38),
            int(central_height * 0.419),
            int(central_width * 0.25),
            int(central_height * 0.044)
        )
    )
    widget.point3_input.setGeometry(
        QRect(
            int(central_width * 0.65),
            int(central_height * 0.419),
            int(central_width * 0.06),
            int(central_height * 0.044)
        )
    )
    widget.point3_input.setAlignment(Qt.AlignCenter)

    widget.ans4_btn.setGeometry(
        QRect(
            int(central_width * 0.38),
            int(central_height * 0.475),
            int(central_width * 0.25),
            int(central_height * 0.044)
        )
    )
    widget.point4_input.setGeometry(
        QRect(
            int(central_width * 0.65),
            int(central_height * 0.475),
            int(central_width * 0.06),
            int(central_height * 0.044)
        )
    )
    widget.point4_input.setAlignment(Qt.AlignCenter)

    widget.ans5_btn.setGeometry(
        QRect(
            int(central_width * 0.38),
            int(central_height * 0.531),
            int(central_width * 0.25),
            int(central_height * 0.044)
        )
    )
    widget.point5_input.setGeometry(
        QRect(
            int(central_width * 0.65),
            int(central_height * 0.531),
            int(central_width * 0.06),
            int(central_height * 0.044)
        )
    )
    widget.point5_input.setAlignment(Qt.AlignCenter)

    widget.ans6_btn.setGeometry(
        QRect(
            int(central_width * 0.38),
            int(central_height * 0.586),
            int(central_width * 0.25),
            int(central_height * 0.044)
        )
    )
    widget.point6_input.setGeometry(
        QRect(
            int(central_width * 0.65),
            int(central_height * 0.586),
            int(central_width * 0.06),
            int(central_height * 0.044)
        )
    )
    widget.point6_input.setAlignment(Qt.AlignCenter)

    widget.ans7_btn.setGeometry(
        QRect(
            int(central_width * 0.38),
            int(central_height * 0.642),
            int(central_width * 0.25),
            int(central_height * 0.044)
        )
    )
    widget.point7_input.setGeometry(
        QRect(
            int(central_width * 0.65),
            int(central_height * 0.642),
            int(central_width * 0.06),
            int(central_height * 0.044)
        )
    )
    widget.point7_input.setAlignment(Qt.AlignCenter)

    widget.ans8_btn.setGeometry(
        QRect(
            int(central_width * 0.38),
            int(central_height * 0.697),
            int(central_width * 0.25),
            int(central_height * 0.044)
        )
    )
    widget.point8_input.setGeometry(
        QRect(
            int(central_width * 0.65),
            int(central_height * 0.697),
            int(central_width * 0.06),
            int(central_height * 0.044)
        )
    )
    widget.point8_input.setAlignment(Qt.AlignCenter)

    widget.total_points_label.setGeometry(
        QRect(
            int(central_width * 0.576),
            int(central_height * 0.765),
            int(central_width * 0.065),
            int(central_height * 0.025)
        )
    )
    widget.total_points_input.setGeometry(
        QRect(
            int(central_width * 0.65),
            int(central_height * 0.753),
            int(central_width * 0.06),
            int(central_height * 0.044)
        )
    )
    widget.total_points_input.setAlignment(Qt.AlignCenter)

    widget.show_answers_count_label.setGeometry(
        QRect(
            int(central_width * 0.38),
            int(central_height * 0.830),
            int(central_width * 0.2),
            int(central_height * 0.025)
        )
    )
    widget.show_answers_count_btn.setGeometry(
        QRect(
            int(central_width * 0.38),
            int(central_height * 0.864),
            int(central_width * 0.118),
            int(central_height * 0.044)
        )
    )
    widget.clear_answers_count_btn.setGeometry(
        QRect(
            int(central_width * 0.51),
            int(central_height * 0.864),
            int(central_width * 0.118),
            int(central_height * 0.044)
        )
    )
    widget.queued_questions_listbox.setGeometry(
        QRect(
            int(central_width * 0.73),
            int(central_height * 0.114),
            int(central_width * 0.23),
            int(central_height * 0.194)
        )
    )
    widget.add_questions_to_database_label.setGeometry(
        QRect(
            int(central_width * 0.73),
            int(central_height * 0.322),
            int(central_width * 0.23),
            int(central_height * 0.025)
        )
    )
    widget.load_file_btn.setGeometry(
        QRect(
            int(central_width * 0.73),
            int(central_height * 0.364),
            int(central_width * 0.11),
            int(central_height * 0.044)
        )
    )
    widget.manual_add_btn.setGeometry(
        QRect(
            int(central_width * 0.73),
            int(central_height * 0.419),
            int(central_width * 0.15),
            int(central_height * 0.044)
        )
    )
    widget.edit_questions_and_answers_label.setGeometry(
        QRect(
            int(central_width * 0.73),
            int(central_height * 0.489),
            int(central_width * 0.23),
            int(central_height * 0.025)
        )
    )
    widget.modify_btn.setGeometry(
        QRect(
            int(central_width * 0.73),
            int(central_height * 0.531),
            int(central_width * 0.07),
            int(central_height * 0.044)
        )
    )
    widget.save_btn.setGeometry(
        QRect(
            int(central_width * 0.81),
            int(central_height * 0.531),
            int(central_width * 0.06),
            int(central_height * 0.044)
        )
    )
    widget.delete_btn.setGeometry(
        QRect(
            int(central_width * 0.88),
            int(central_height * 0.531),
            int(central_width * 0.07),
            int(central_height * 0.044)
        )
    )
    widget.start_over_clear_log_label.setGeometry(
        QRect(
            int(central_width * 0.73),
            int(central_height * 0.830),
            int(central_width * 0.23),
            int(central_height * 0.025)
        )
    )
    widget.log_next_round.setGeometry(
        QRect(
            int(central_width * 0.73),
            int(central_height * 0.864),
            int(central_width * 0.13),
            int(central_height * 0.044)
        )
    )
    widget.clear_log_btn.setGeometry(
        QRect(
            int(central_width * 0.87),
            int(central_height * 0.864),
            int(central_width * 0.09),
            int(central_height * 0.044)
        )
    )
    widget.game_audio_control_label.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.7665),
            int(central_width * 0.32),
            int(central_height * 0.025)
        )
    )
    widget.intro_music_btn.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.8085),
            int(central_width * 0.10),
            int(central_height * 0.044)
        )
    )
    widget.face_off_music_btn.setGeometry(
        QRect(
            int(central_width * 0.15),
            int(central_height * 0.8085),
            int(central_width * 0.10),
            int(central_height * 0.044)
        )
    )
    widget.outro_music_btn.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.864),
            int(central_width * 0.10),
            int(central_height * 0.044)
        )
    )
    widget.correct_ans_music_btn.setGeometry(
        QRect(
            int(central_width * 0.15),
            int(central_height * 0.864),
            int(central_width * 0.10),
            int(central_height * 0.044)
        )
    )
    widget.winning_sound_btn.setGeometry(
        QRect(
            int(central_width * 0.26),
            int(central_height * 0.8085),
            int(central_width * 0.10),
            int(central_height * 0.044)
        )
    )
    widget.strike_music_btn.setGeometry(
        QRect(
            int(central_width * 0.26),
            int(central_height * 0.864),
            int(central_width * 0.10),
            int(central_height * 0.044)
        )
    )
    widget.round_multiplier_label.setGeometry(
        QRect(
            int(central_width * 0.73),
            int(central_height * 0.600),
            int(central_width * 0.32),
            int(central_height * 0.025)
        )
    )
    widget.x2_round_btn.setGeometry(
        QRect(
            int(central_width * 0.73),
            int(central_height * 0.642),
            int(central_width * 0.10),
            int(central_height * 0.044)
        )
    )
    widget.timer_input.setGeometry(
        QRect(
            int(central_width * 0.84),
            int(central_height * 0.642),
            int(central_width * 0.08),
            int(central_height * 0.044)
        )
    )
    widget.timer_input.setAlignment(Qt.AlignCenter)

    widget.x3_round_btn.setGeometry(
        QRect(
            int(central_width * 0.73),
            int(central_height * 0.697),
            int(central_width * 0.10),
            int(central_height * 0.044)
        )
    )
    widget.start_timer_btn.setGeometry(
        QRect(
            int(central_width * 0.84),
            int(central_height * 0.697),
            int(central_width * 0.12),
            int(central_height * 0.044)
        )
    )
    widget.sec_label.setGeometry(
        QRect(
            int(central_width * 0.93),
            int(central_height * 0.655),
            int(central_width * 0.05),
            int(central_height * 0.025)
        )
    )
    widget.supported_file_type_label.setGeometry(
        QRect(
            int(central_width * 0.847),
            int(central_height * 0.375),
            int(central_width * 0.12),
            int(central_height * 0.025)
        )
    )

    # ------------------------------------------------------------ Fast Money Round Table ------------------------------------------------------------

    widget.family_feud_fast_money_round_label.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.020),
            int(central_width * 0.36),
            int(central_height * 0.09)
        )
    )
    widget.select_team_to_play_fm_label.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.082),
            int(central_width * 0.204),
            int(central_height * 0.025)
        )
    )
    widget.team_listBox.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.112),
            int(central_width * 0.188),
            int(central_height * 0.046)
        )
    )
    widget.game_question_view_label.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.19),
            int(central_width * 0.321),
            int(central_height * 0.025)
        )
    )
    widget.fm_game_questions_input.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.221),
            int(central_width * 0.321),
            int(central_height * 0.159)
        )
    )
    widget.fm_point1_input.setGeometry(
        QRect(
            int(central_width * 0.306),
            int(central_height * 0.439),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_point1_input.setAlignment(Qt.AlignCenter)

    widget.fm_point2_input.setGeometry(
        QRect(
            int(central_width * 0.306),
            int(central_height * 0.497),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_point2_input.setAlignment(Qt.AlignCenter)

    widget.fm_point3_input.setGeometry(
        QRect(
            int(central_width * 0.306),
            int(central_height * 0.555),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_point3_input.setAlignment(Qt.AlignCenter)

    widget.fm_point4_input.setGeometry(
        QRect(
            int(central_width * 0.306),
            int(central_height * 0.613),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_point4_input.setAlignment(Qt.AlignCenter)

    widget.fm_point5_input.setGeometry(
        QRect(
            int(central_width * 0.306),
            int(central_height * 0.671),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_point5_input.setAlignment(Qt.AlignCenter)

    widget.fm_add_questions_to_database_label.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.756),
            int(central_width * 0.321),
            int(central_height * 0.025)
        )
    )
    widget.fm_load_from_file_btn.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.787),
            int(central_width * 0.110),
            int(central_height * 0.046)
        )
    )
    widget.fm_manual_add_questions_btn.setGeometry(
        QRect(
            int(central_width * 0.157),
            int(central_height * 0.787),
            int(central_width * 0.133),
            int(central_height * 0.046)
        )
    )
    widget.fm_edit_questions_and_answers_label.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.858),
            int(central_width * 0.321),
            int(central_height * 0.025)
        )
    )
    widget.fm_mod_btn.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.888),
            int(central_width * 0.078),
            int(central_height * 0.046)
        )
    )
    widget.fm_save_btn.setGeometry(
        QRect(
            int(central_width * 0.125),
            int(central_height * 0.888),
            int(central_width * 0.078),
            int(central_height * 0.046)
        )
    )
    widget.fm_delete_btn.setGeometry(
        QRect(
            int(central_width * 0.212),
            int(central_height * 0.888),
            int(central_width * 0.078),
            int(central_height * 0.046)
        )
    )
    widget.click_the_ans_btn_to_reveal_label.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.408),
            int(central_width * 0.321),
            int(central_height * 0.025)
        )
    )
    widget.fm_R1Ans1_input.setGeometry(
        QRect(
            int(central_width * 0.392),
            int(central_height * 0.163),
            int(central_width * 0.204),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Ans1_input.setAlignment(Qt.AlignCenter)

    widget.contestant_answers_label.setGeometry(
        QRect(
            int(central_width * 0.392),
            int(central_height * 0.082),
            int(central_width * 0.196),
            int(central_height * 0.025)
        )
    )
    widget.player1_answers_label.setGeometry(
        QRect(
            int(central_width * 0.392),
            int(central_height * 0.132),
            int(central_width * 0.196),
            int(central_height * 0.025)
        )
    )
    widget.fm_R1Ans2_input.setGeometry(
        QRect(
            int(central_width * 0.392),
            int(central_height * 0.221),
            int(central_width * 0.204),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Ans2_input.setAlignment(Qt.AlignCenter)
    
    widget.fm_R1Ans3_input.setGeometry(
        QRect(
            int(central_width * 0.392),
            int(central_height * 0.279),
            int(central_width * 0.204),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Ans3_input.setAlignment(Qt.AlignCenter)

    widget.fm_R1Ans4_input.setGeometry(
        QRect(
            int(central_width * 0.392),
            int(central_height * 0.337),
            int(central_width * 0.204),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Ans4_input.setAlignment(Qt.AlignCenter)

    widget.fm_R1Ans5_input.setGeometry(
        QRect(
            int(central_width * 0.392),
            int(central_height * 0.395),
            int(central_width * 0.204),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Ans5_input.setAlignment(Qt.AlignCenter)

    widget.player2_answers_label.setGeometry(
        QRect(
            int(central_width * 0.392),
            int(central_height * 0.464),
            int(central_width * 0.196),
            int(central_height * 0.025)
        )
    )
    widget.fm_R2Ans1_input.setGeometry(
        QRect(
            int(central_width * 0.392),
            int(central_height * 0.497),
            int(central_width * 0.204),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Ans1_input.setAlignment(Qt.AlignCenter)

    widget.fm_R2Ans2_input.setGeometry(
        QRect(
            int(central_width * 0.392),
            int(central_height * 0.555),
            int(central_width * 0.204),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Ans2_input.setAlignment(Qt.AlignCenter)

    widget.fm_R2Ans3_input.setGeometry(
        QRect(
            int(central_width * 0.392),
            int(central_height * 0.613),
            int(central_width * 0.204),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Ans3_input.setAlignment(Qt.AlignCenter)

    widget.fm_R2Ans4_input.setGeometry(
        QRect(
            int(central_width * 0.392),
            int(central_height * 0.671),
            int(central_width * 0.204),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Ans4_input.setAlignment(Qt.AlignCenter)

    widget.fm_R2Ans5_input.setGeometry(
        QRect(
            int(central_width * 0.392),
            int(central_height * 0.729),
            int(central_width * 0.204),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Ans5_input.setAlignment(Qt.AlignCenter)

    widget.fm_R1Ans1_btn.setGeometry(
        QRect(
            int(central_width * 0.603),
            int(central_height * 0.163),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Ans2_btn.setGeometry(
        QRect(
            int(central_width * 0.603),
            int(central_height * 0.221),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Ans3_btn.setGeometry(
        QRect(
            int(central_width * 0.603),
            int(central_height * 0.279),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Ans4_btn.setGeometry(
        QRect(
            int(central_width * 0.603),
            int(central_height * 0.337),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Ans5_btn.setGeometry(
        QRect(
            int(central_width * 0.603),
            int(central_height * 0.395),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Ans1_btn.setGeometry(
        QRect(
            int(central_width * 0.603),
            int(central_height * 0.497),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Ans2_btn.setGeometry(
        QRect(
            int(central_width * 0.603),
            int(central_height * 0.555),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Ans3_btn.setGeometry(
        QRect(
            int(central_width * 0.603),
            int(central_height * 0.613),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Ans4_btn.setGeometry(
        QRect(
            int(central_width * 0.603),
            int(central_height * 0.671),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Ans5_btn.setGeometry(
        QRect(
            int(central_width * 0.603),
            int(central_height * 0.729),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Point1_input.setGeometry(
        QRect(
            int(central_width * 0.666),
            int(central_height * 0.163),
            int(central_width * 0.039),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Point1_input.setAlignment(Qt.AlignCenter)

    widget.fm_R1Point2_input.setGeometry(
        QRect(
            int(central_width * 0.666),
            int(central_height * 0.221),
            int(central_width * 0.039),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Point2_input.setAlignment(Qt.AlignCenter)

    widget.fm_R1Point3_input.setGeometry(
        QRect(
            int(central_width * 0.666),
            int(central_height * 0.279),
            int(central_width * 0.039),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Point3_input.setAlignment(Qt.AlignCenter)

    widget.fm_R1Point4_input.setGeometry(
        QRect(
            int(central_width * 0.666),
            int(central_height * 0.337),
            int(central_width * 0.039),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Point4_input.setAlignment(Qt.AlignCenter)

    widget.fm_R1Point5_input.setGeometry(
        QRect(
            int(central_width * 0.666),
            int(central_height * 0.395),
            int(central_width * 0.039),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Point5_input.setAlignment(Qt.AlignCenter)

    widget.fm_R2Point1_input.setGeometry(
        QRect(
            int(central_width * 0.666),
            int(central_height * 0.497),
            int(central_width * 0.039),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Point1_input.setAlignment(Qt.AlignCenter)

    widget.fm_R2Point2_input.setGeometry(
        QRect(
            int(central_width * 0.666),
            int(central_height * 0.555),
            int(central_width * 0.039),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Point2_input.setAlignment(Qt.AlignCenter)

    widget.fm_R2Point3_input.setGeometry(
        QRect(
            int(central_width * 0.666),
            int(central_height * 0.613),
            int(central_width * 0.039),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Point3_input.setAlignment(Qt.AlignCenter)

    widget.fm_R2Point4_input.setGeometry(
        QRect(
            int(central_width * 0.666),
            int(central_height * 0.671),
            int(central_width * 0.039),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Point4_input.setAlignment(Qt.AlignCenter)

    widget.fm_R2Point5_input.setGeometry(
        QRect(
            int(central_width * 0.666),
            int(central_height * 0.729),
            int(central_width * 0.039),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Point5_input.setAlignment(Qt.AlignCenter)

    widget.fm_R1Point1_btn.setGeometry(
        QRect(
            int(central_width * 0.712),
            int(central_height * 0.163),
            int(central_width * 0.063),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Point2_btn.setGeometry(
        QRect(
            int(central_width * 0.712),
            int(central_height * 0.221),
            int(central_width * 0.063),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Point3_btn.setGeometry(
        QRect(
            int(central_width * 0.712),
            int(central_height * 0.279),
            int(central_width * 0.063),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Point4_btn.setGeometry(
        QRect(
            int(central_width * 0.712),
            int(central_height * 0.337),
            int(central_width * 0.063),
            int(central_height * 0.046)
        )
    )
    widget.fm_R1Point5_btn.setGeometry(
        QRect(
            int(central_width * 0.712),
            int(central_height * 0.395),
            int(central_width * 0.063),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Point1_btn.setGeometry(
        QRect(
            int(central_width * 0.712),
            int(central_height * 0.497),
            int(central_width * 0.063),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Point2_btn.setGeometry(
        QRect(
            int(central_width * 0.712),
            int(central_height * 0.555),
            int(central_width * 0.063),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Point3_btn.setGeometry(
        QRect(
            int(central_width * 0.712),
            int(central_height * 0.613),
            int(central_width * 0.063),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Point4_btn.setGeometry(
        QRect(
            int(central_width * 0.712),
            int(central_height * 0.671),
            int(central_width * 0.063),
            int(central_height * 0.046)
        )
    )
    widget.fm_R2Point5_btn.setGeometry(
        QRect(
            int(central_width * 0.712),
            int(central_height * 0.729),
            int(central_width * 0.063),
            int(central_height * 0.046)
        )
    )
    widget.fm_queued_questions_listBox.setGeometry(
        QRect(
            int(central_width * 0.806),
            int(central_height * 0.163),
            int(central_width * 0.157),
            int(central_height * 0.609)
        )
    )
    widget.queued_questions_label.setGeometry(
        QRect(
            int(central_width * 0.806),
            int(central_height * 0.132),
            int(central_width * 0.157),
            int(central_height * 0.025)
        )
    )
    widget.fm_timer_input.setGeometry(
        QRect(
            int(central_width * 0.391),
            int(central_height * 0.888),
            int(central_width * 0.086),
            int(central_height * 0.046)
        )
    )
    widget.fm_timer_input.setAlignment(Qt.AlignCenter)
    
    widget.set_timer_label.setGeometry(
        QRect(
            int(central_width * 0.391),
            int(central_height * 0.858),
            int(central_width * 0.203),
            int(central_height * 0.025)
        )
    )
    widget.fm_startTimer_btn.setGeometry(
        QRect(
            int(central_width * 0.485),
            int(central_height * 0.888),
            int(central_width * 0.109),
            int(central_height * 0.046)
        )
    )
    widget.fm_ans1_input.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.439),
            int(central_width * 0.250),
            int(central_height * 0.046)
        )
    )
    widget.fm_ans1_input.setAlignment(Qt.AlignCenter)

    widget.fm_ans2_input.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.497),
            int(central_width * 0.250),
            int(central_height * 0.046)
        )
    )
    widget.fm_ans2_input.setAlignment(Qt.AlignCenter)

    widget.fm_ans3_input.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.555),
            int(central_width * 0.250),
            int(central_height * 0.046)
        )
    )
    widget.fm_ans3_input.setAlignment(Qt.AlignCenter)

    widget.fm_ans4_input.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.613),
            int(central_width * 0.250),
            int(central_height * 0.046)
        )
    )
    widget.fm_ans4_input.setAlignment(Qt.AlignCenter)

    widget.fm_ans5_input.setGeometry(
        QRect(
            int(central_width * 0.039),
            int(central_height * 0.671),
            int(central_width * 0.250),
            int(central_height * 0.046)
        )
    )
    widget.fm_ans5_input.setAlignment(Qt.AlignCenter)

    widget.win_music_label.setGeometry(
        QRect(
            int(central_width * 0.627),
            int(central_height * 0.858),
            int(central_width * 0.157),
            int(central_height * 0.025)
        )
    )
    widget.fm_winMusic_btn.setGeometry(
        QRect(
            int(central_width * 0.627),
            int(central_height * 0.888),
            int(central_width * 0.157),
            int(central_height * 0.046)
        )
    )
    widget.fm_clearQuestions_btn.setGeometry(
        QRect(
            int(central_width * 0.806),
            int(central_height * 0.888),
            int(central_width * 0.157),
            int(central_height * 0.046)
        )
    )
    widget.fm_startOver_btn.setGeometry(
        QRect(
            int(central_width * 0.806),
            int(central_height * 0.830),
            int(central_width * 0.157),
            int(central_height * 0.046)
        )
    )
    widget.fm_saveQandA_btn.setGeometry(
        QRect(
            int(central_width * 0.305),
            int(central_height * 0.787),
            int(central_width * 0.055),
            int(central_height * 0.046)
        )
    )
    widget.fm_totalPoints_input.setGeometry(
        QRect(
            int(central_width * 0.666),
            int(central_height * 0.787),
            int(central_width * 0.039),
            int(central_height * 0.046)
        )
    )
    widget.fm_totalPoints_input.setAlignment(Qt.AlignCenter)
    
    widget.fm_totalPoints_label.setGeometry(
        QRect(
            int(central_width * 0.627),
            int(central_height * 0.8),
            int(central_width * 0.031),
            int(central_height * 0.025)
        )
    )

    # ------------------------------------------------------------------ About Table ----------------------------------

    # About Title Label
    widget.about_title_label.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.020),
            int(central_width * 0.92),
            int(central_height * 0.05)
        )
    )

    # About Description Text Box
    widget.about_description_textBox.setGeometry(
        QRect(
            int(central_width * 0.04),
            int(central_height * 0.08),
            int(central_width * 0.92),
            int(central_height * 0.85)
        )
    )