from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QLabel, 
                            QPushButton, QGridLayout, QHBoxLayout, QStackedWidget, QWidget)
from PyQt5.QtCore import Qt
from .input_fields import UserInput
from .pin_view import PinView
from . import styles
from config.screen_config import screen_config

class AuthenticationContainer(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.valid_user_id = "1001"  # Hardcoded valid user ID
        self.number_buttons = []     # Initialize number buttons list
        
        # Get container size from screen config
        width = screen_config.get_size('auth_container_width')
        height = screen_config.get_size('auth_container_height')
        self.setFixedSize(width, height)
        
        self.setStyleSheet(styles.AuthStyles.CONTAINER)
        self._setup_ui()
        self.setFocusPolicy(Qt.StrongFocus)  # Enable keyboard focus

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        margin = screen_config.get_size('container_margin')
        layout.setContentsMargins(0, 0, 0, 0)
        
        # User ID View
        self.user_id_view = self._create_user_id_view()
        layout.addWidget(self.user_id_view)

    def _create_user_id_view(self):
        """Create and return the User ID view"""
        user_id_view = QWidget()
        layout = QVBoxLayout(user_id_view)
        
        # Get spacing and margins from screen config
        margin = screen_config.get_size('container_margin')
        spacing = screen_config.get_size('section_spacing')
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(spacing)

        # User ID Label
        self.lbl_user_id = QLabel("User ID", alignment=Qt.AlignCenter)
        self.lbl_user_id.setStyleSheet(styles.AuthStyles.LABEL_TEXT)
        layout.addWidget(self.lbl_user_id)

        # Input Fields
        self.user_input = UserInput()
        layout.addWidget(self.user_input)

        # Keypad
        grid = QGridLayout()
        keypad_spacing = screen_config.get_size('keypad_spacing')
        grid.setHorizontalSpacing(keypad_spacing)
        grid.setVerticalSpacing(keypad_spacing)

        # Number buttons 1-9
        positions = [(i//3, i%3) for i in range(9)]
        button_width = screen_config.get_size('keypad_button_width')
        button_height = screen_config.get_size('keypad_button_height')
        
        for idx, (row, col) in enumerate(positions):
            btn = QPushButton(str(idx+1))
            btn.setFixedSize(button_width, button_height)
            btn.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON.format(
                screen_config.get_size('keypad_font_size'),
                screen_config.get_size('keypad_padding')
            ))
            btn.clicked.connect(lambda _, num=idx+1: self._on_number_click(num))
            self.number_buttons.append(btn)
            grid.addWidget(btn, row, col)

        # Action buttons
        action_row = QHBoxLayout()
        action_row.setSpacing(keypad_spacing)
        
        # Get action button sizes
        action_width = screen_config.get_size('action_button_width')
        action_height = screen_config.get_size('action_button_height')

        self.btn_clear = QPushButton("Clear")
        btn_0 = QPushButton("0")
        self.btn_next = QPushButton("Next")
        
        # Style the '0' button like other keypad buttons
        btn_0.setFixedSize(button_width, button_height)
        btn_0.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON.format(
                screen_config.get_size('keypad_font_size'),
                screen_config.get_size('keypad_padding')
            ))

        # Style action buttons
        self.btn_clear.setFixedSize(action_width, action_height)
        self.btn_next.setFixedSize(action_width, action_height)
        
        # Set action button styles
        self.btn_clear.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)
        self.btn_next.setStyleSheet(styles.AuthStyles.KEYPAD_BUTTON)
        
        # Initialize action button states
        self.btn_clear.setEnabled(False)
        self.btn_next.setEnabled(False)
        
        # Connect buttons
        self.btn_clear.clicked.connect(self.user_input.remove_digit)
        btn_0.clicked.connect(lambda: self._on_number_click(0))
        self.btn_next.clicked.connect(self._handle_next)
        
        self.number_buttons.append(btn_0)  # Add 0 button to number buttons list

        action_row.addWidget(self.btn_clear)
        action_row.addWidget(btn_0)
        action_row.addWidget(self.btn_next)

        layout.addLayout(grid)
        layout.addLayout(action_row)

        # Connect input changes to button state updates
        self.user_input.input_changed.connect(self._update_button_states)

        return user_id_view

    def _on_number_click(self, number):
        self.user_input.add_digit(str(number))
        self._reset_user_id_label()

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
        if self.user_input.is_complete():
            user_id = "".join(self.user_input.digits)
            print(f"User ID entered: {user_id}")  # Debugging output
            if user_id == self.valid_user_id:
                self.switch_to_pin_view(user_id)
            else:
                self._show_invalid_user_id()

    def _show_invalid_user_id(self):
        self.lbl_user_id.setText("Invalid User ID")
        self.lbl_user_id.setStyleSheet(styles.AuthStyles.LABEL_TEXT_INVALID)

    def _reset_user_id_label(self):
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
            self._reset_user_id_label()
        
        # Backspace
        elif key == Qt.Key_Backspace:
            self.user_input.remove_digit()
            self._reset_user_id_label()
        
        # Enter/Return
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            if self.user_input.is_complete():
                self._handle_next()
        
        # Ignore other keys
        else:
            super().keyPressEvent(event)