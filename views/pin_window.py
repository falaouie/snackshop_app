from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QGridLayout, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap
from .input_fields import UserIDInput  # Reuse the input fields component
from . import styles

class PinView(QFrame):
    submit_requested = pyqtSignal(str)  # Signal for submitting PIN
    
    def __init__(self, user_id, auth_container, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.auth_container = auth_container  # Store reference to auth container
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

        # PIN Label
        self.lbl_pin = QLabel(f"Password for User ID {self.user_id}", alignment=Qt.AlignCenter)
        self.lbl_pin.setStyleSheet("font-size: 18px; color: #333;")
        layout.addWidget(self.lbl_pin)

        # Input Fields
        self.pin_input = UserIDInput()
        layout.addWidget(self.pin_input)

        # Keypad
        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        
        # Number buttons 1-9
        positions = [(i//3, i%3) for i in range(9)]
        for idx, (row, col) in enumerate(positions):
            btn = QPushButton(str(idx+1))
            btn.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)
            btn.clicked.connect(lambda _, num=idx+1: self._on_number_click(num))
            grid.addWidget(btn, row, col)

        # Action buttons
        action_row = QHBoxLayout()
        self.btn_clear = QPushButton("Clear")
        btn_0 = QPushButton("0")
        self.btn_back = QPushButton("Back")
        
        # Initialize buttons
        self.btn_clear.setEnabled(False)
        self.btn_clear.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)
        self.btn_back.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)
        
        # Connect buttons
        self.btn_clear.clicked.connect(self.pin_input.remove_digit)
        btn_0.clicked.connect(lambda: self._on_number_click(0))
        self.btn_back.clicked.connect(self._handle_back)
        
        # Style 0 button
        btn_0.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)

        action_row.addWidget(self.btn_clear)
        action_row.addWidget(btn_0)
        action_row.addWidget(self.btn_back)

        layout.addLayout(grid)
        layout.addLayout(action_row)

        # Sign In button
        self.btn_sign_in = QPushButton("Sign In")
        self.btn_sign_in.setEnabled(False)
        self.btn_sign_in.setStyleSheet(styles.AuthStyles.NEXT_BUTTON_ACTIVE)
        layout.addWidget(self.btn_sign_in, alignment=Qt.AlignCenter)

        # Connect input changes to button state updates
        self.pin_input.input_changed.connect(self._update_button_states)
        self.btn_sign_in.clicked.connect(self._handle_sign_in)

    def _on_number_click(self, number):
        self.pin_input.add_digit(str(number))

    def _update_button_states(self, digits):
        """Update button states based on input"""
        has_digits = self.pin_input.has_digits()
        is_complete = self.pin_input.is_complete()
        
        # Update Clear button
        self.btn_clear.setEnabled(has_digits)
        
        # Update Sign In button
        self.btn_sign_in.setEnabled(is_complete)
        self.btn_sign_in.setStyleSheet(
            styles.AuthStyles.NEXT_BUTTON_ACTIVE if is_complete
            else styles.AuthStyles.KEYPAD_BUTTON
        )
        
        # Update number buttons (0-9)
        for btn in self.findChildren(QPushButton):
            if btn.text().isdigit():
                btn.setEnabled(not is_complete)

    def _handle_back(self):
        """Handle Back button click"""
        self.parent().switch_to_user_id_view()

    def _handle_sign_in(self):
        """Handle Sign In button click"""
        if self.pin_input.is_complete():
            pin = "".join(self.pin_input.digits)
            self.submit_requested.emit(pin)

    def _handle_back(self):
        """Handle Back button click"""
        self.auth_container.switch_to_user_id_view()  # Use auth_container reference