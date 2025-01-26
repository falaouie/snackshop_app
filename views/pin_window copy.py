from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QGridLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from .input_fields import UserInput
from . import styles

class PinView(QWidget):
    def __init__(self, user_id, auth_container, parent=None):
        super().__init__(parent or auth_container)
        self.user_id = user_id
        self.auth_container = auth_container
        self.setFixedSize(400, 600)
        self.setStyleSheet(styles.AuthStyles.CONTAINER)
        self._setup_ui()

        # Position in parent
        if parent or auth_container:
            parent_rect = (parent or auth_container).rect()
            self.move(
                (parent_rect.width() - self.width()) // 2,
                (parent_rect.height() - self.height()) // 2
            )

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # PIN Label
        self.lbl_pin = QLabel(f"Password for User ID {self.user_id}", alignment=Qt.AlignCenter)
        self.lbl_pin.setStyleSheet(styles.AuthStyles.LABEL_TEXT)
        layout.addWidget(self.lbl_pin)

        # Input Fields
        self.pin_input = UserInput(is_pin=True)
        layout.addWidget(self.pin_input)

        # Keypad container
        keypad_container = QVBoxLayout()
        keypad_container.setSpacing(15)
        
        # Number pad grid
        grid = QGridLayout()
        grid.setHorizontalSpacing(15)
        grid.setVerticalSpacing(15)
        
        # Number buttons 1-9
        positions = [(i//3, i%3) for i in range(9)]
        for idx, (row, col) in enumerate(positions):
            btn = QPushButton(str(idx+1))
            btn.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)
            btn.clicked.connect(lambda _, num=idx+1: self._on_number_click(num))
            grid.addWidget(btn, row, col)

        keypad_container.addLayout(grid)

        # Action buttons
        action_row = QHBoxLayout()
        action_row.setSpacing(15)
        
        self.btn_clear = QPushButton("Clear")
        btn_0 = QPushButton("0")
        self.btn_back = QPushButton("Back")
        
        for btn in [self.btn_clear, btn_0, self.btn_back]:
            btn.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)
            action_row.addWidget(btn)
        
        self.btn_clear.setEnabled(False)
        btn_0.clicked.connect(lambda: self._on_number_click(0))
        self.btn_clear.clicked.connect(self.pin_input.remove_digit)
        self.btn_back.clicked.connect(self._handle_back)

        keypad_container.addLayout(action_row)
        layout.addLayout(keypad_container)

        # Sign In button
        self.btn_sign_in = QPushButton("Sign In")
        self.btn_sign_in.setEnabled(False)
        self.btn_sign_in.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)
        layout.addWidget(self.btn_sign_in)

        # Connect signals
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
        self.auth_container.switch_to_user_id_view()  # Use auth_container reference

    def _handle_sign_in(self):
        """Handle Sign In button click"""
        if self.pin_input.is_complete():
            pin = "".join(self.pin_input.digits)
            self.submit_requested.emit(pin)

    def keyPressEvent(self, event):
        """Handle physical keyboard input"""
        key = event.key()
        
        # Number keys (0-9)
        if Qt.Key_0 <= key <= Qt.Key_9 and not self.pin_input.is_complete():
            digit = str(key - Qt.Key_0)
            self.pin_input.add_digit(digit)
        
        # Backspace
        elif key == Qt.Key_Backspace:
            self.pin_input.remove_digit()
        
        # Enter/Return
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            if self.pin_input.is_complete():
                self._handle_sign_in()
        
        # Ignore other keys
        else:
            super().keyPressEvent(event)