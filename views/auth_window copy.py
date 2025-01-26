from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QLabel, 
                            QPushButton, QGridLayout, QHBoxLayout, QStackedWidget, QWidget)
from PyQt5.QtCore import Qt
from .input_fields import UserInput
from .pin_window import PinView
from . import styles

class AuthenticationContainer(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.valid_user_id = "1001"  # Hardcoded valid user ID
        self.number_buttons = []     # Initialize number buttons list
        self.setFixedSize(400, 600)
        self.setStyleSheet(styles.AuthStyles.CONTAINER)
        self._setup_ui()
        self.setFocusPolicy(Qt.StrongFocus)  # Enable keyboard focus

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # User ID View
        self.user_id_view = self._create_user_id_view()
        layout.addWidget(self.user_id_view)

    def _create_user_id_view(self):
        """Create and return the User ID view"""
        user_id_view = QWidget()  # Create a QWidget for the User ID view
        layout = QVBoxLayout(user_id_view)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # User ID Label
        self.lbl_user_id = QLabel("User ID", alignment=Qt.AlignCenter)
        # self.lbl_user_id.setStyleSheet("font-size: 18px; color: #333;")
        self.lbl_user_id.setStyleSheet(styles.AuthStyles.LABEL_TEXT)
        layout.addWidget(self.lbl_user_id)

        # Input Fields
        self.user_input = UserInput()
        layout.addWidget(self.user_input)

        # Keypad
        grid = QGridLayout()
        grid.setHorizontalSpacing(15)
        grid.setVerticalSpacing(15)
        # grid.setStyleSheet(styles.AuthStyles.CONTAINER)
        # Number buttons 1-9
        positions = [(i//3, i%3) for i in range(9)]
        for idx, (row, col) in enumerate(positions):
            btn = QPushButton(str(idx+1))
            btn.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)
            btn.clicked.connect(lambda _, num=idx+1: self._on_number_click(num))
            self.number_buttons.append(btn)  # Add to number buttons list
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
        self.btn_next.clicked.connect(self._handle_next)
        
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

        return user_id_view  # Return the QWidget

    def _on_number_click(self, number):
        self.user_input.add_digit(str(number))
        self._reset_user_id_label()  # Restore label when typing starts

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

    def _handle_next(self):
        """Handle Next button click or Enter key"""
        if self.user_input.is_complete():
            user_id = "".join(self.user_input.digits)
            print(f"User ID entered: {user_id}")  # Debugging output
            if user_id == self.valid_user_id:
                self.switch_to_pin_view(user_id)  # Switch to PIN view
            else:
                self._show_invalid_user_id()  # Show error and clear input

    def _show_invalid_user_id(self):
        """Show invalid user ID message and clear input"""
        self.lbl_user_id.setText("Invalid User ID")
        self.lbl_user_id.setStyleSheet(styles.AuthStyles.LABEL_TEXT_INVALID)
        self.user_input.clear_all()

    def _reset_user_id_label(self):
        """Restore User ID label to original state"""
        self.lbl_user_id.setText("User ID")
        self.lbl_user_id.setStyleSheet(styles.AuthStyles.LABEL_TEXT)

    def switch_to_pin_view(self, user_id):
        if hasattr(self, 'user_id_view'):
            self.user_id_view.hide()
        
        if not hasattr(self, 'pin_view'):
            self.pin_view = PinView(user_id, self)
        self.pin_view.show()
        self.pin_view.setFocus()

    def switch_to_user_id_view(self):
        if hasattr(self, 'pin_view'):
            self.pin_view.hide()
        self.user_id_view.show()
        self.user_input.clear_all()
        self.user_id_view.setFocus()

    def keyPressEvent(self, event):
        """Handle physical keyboard input"""
        key = event.key()
        
        # Number keys (0-9)
        if Qt.Key_0 <= key <= Qt.Key_9 and not self.user_input.is_complete():
            digit = str(key - Qt.Key_0)
            self.user_input.add_digit(digit)
            self._reset_user_id_label()  # Reset label when typing starts
        
        # Backspace
        elif key == Qt.Key_Backspace:
            self.user_input.remove_digit()
            self._reset_user_id_label()  # Reset label when removing digits
        
        # Enter/Return
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            if self.user_input.is_complete():
                self._handle_next()
        
        # Ignore other keys
        else:
            super().keyPressEvent(event)