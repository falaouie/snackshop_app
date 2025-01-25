from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QLabel, 
                            QPushButton, QGridLayout, QHBoxLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize
from .input_fields import UserIDInput
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

        # Input Fields
        self.user_input = UserIDInput()
        layout.addWidget(self.user_input)

        # Keypad
        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        
        # Store number buttons for later reference
        self.number_buttons = []
        
        # Number buttons 1-9
        positions = [(i//3, i%3) for i in range(9)]
        for idx, (row, col) in enumerate(positions):
            btn = QPushButton(str(idx+1))
            btn.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)
            btn.clicked.connect(lambda _, num=idx+1: self._on_number_click(num))
            self.number_buttons.append(btn)
            grid.addWidget(btn, row, col)

        # Action buttons
        action_row = QHBoxLayout()
        self.btn_clear = QPushButton("Clear")
        btn_0 = QPushButton("0")
        self.btn_next = QPushButton("Next")
        
        # Initialize buttons
        self.btn_clear.setEnabled(False)
        self.btn_next.setEnabled(False)
        self.btn_clear.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)
        self.btn_next.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)
        
        # Connect buttons
        self.btn_clear.clicked.connect(self.user_input.remove_digit)
        btn_0.clicked.connect(lambda: self._on_number_click(0))
        
        # Style 0 button
        btn_0.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)
        self.number_buttons.append(btn_0)  # Add 0 button to number buttons list

        action_row.addWidget(self.btn_clear)
        action_row.addWidget(btn_0)
        action_row.addWidget(self.btn_next)

        layout.addLayout(grid)
        layout.addLayout(action_row)

        # Connect input changes to button state updates
        self.user_input.input_changed.connect(self._update_button_states)

    def _on_number_click(self, number):
        self.user_input.add_digit(str(number))

    def _update_button_states(self, digits):
      """Update button states based on input"""
      has_digits = self.user_input.has_digits()
      is_complete = self.user_input.is_complete()
      
      # Update Clear button
      self.btn_clear.setEnabled(has_digits)
      
      # Update Next button
      self.btn_next.setEnabled(is_complete)
      self.btn_next.setStyleSheet(
          styles.AuthStyles.NEXT_BUTTON_ACTIVE if is_complete
          else styles.AuthStyles.KEYPAD_BUTTON
      )
      
      # Update number buttons (0-9)
      for btn in self.number_buttons:
          btn.setEnabled(not is_complete)