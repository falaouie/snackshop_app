from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QLabel, 
                            QPushButton, QGridLayout, QHBoxLayout, QWidget)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize
from . import styles

class AuthenticationContainer(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 600)
        self.setStyleSheet(styles.AuthStyles.CONTAINER)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Logo Section
        logo_label = QLabel()
        pixmap = QPixmap("assets/images/silver_system_logo.png")
        scaled_pixmap = pixmap.scaled(
            QSize(300, 150), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setStyleSheet(styles.AuthStyles.LOGO_CONTAINER)
        layout.addWidget(logo_label)

        # User ID Label
        lbl_user_id = QLabel("User ID", alignment=Qt.AlignCenter)
        lbl_user_id.setStyleSheet("font-size: 18px; color: #333;")
        layout.addWidget(lbl_user_id)

        # Input Fields (Placeholder)
        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setSpacing(10)
        for _ in range(4):
            box = QLabel()
            box.setFixedSize(40, 40)
            box.setStyleSheet("border: 2px solid #ddd; border-radius: 5px;")
            input_layout.addWidget(box)
        layout.addWidget(input_container)

        # Keypad
        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        
        # Number buttons 1-9
        positions = [(i//3, i%3) for i in range(9)]
        for idx, (row, col) in enumerate(positions):
            btn = QPushButton(str(idx+1))
            btn.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)
            grid.addWidget(btn, row, col)

        # Action buttons
        action_row = QHBoxLayout()
        btn_clear = QPushButton("Clear")
        btn_0 = QPushButton("0")
        btn_next = QPushButton("Next")
        
        # Apply KEYPAD_BUTTON style to all
        for btn in [btn_clear, btn_0, btn_next]:
            btn.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)
            # btn.setFixedSize(70, 50)

        action_row.addWidget(btn_clear)
        action_row.addWidget(btn_0)
        action_row.addWidget(btn_next)

        layout.addLayout(grid)
        layout.addLayout(action_row)