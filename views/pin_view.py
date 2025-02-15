from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QLabel, QPushButton, 
                           QGridLayout, QHBoxLayout, QWidget, QMainWindow)
from PyQt5.QtCore import Qt, pyqtSignal
from .input_fields import UserInput
from .pos_view import POSView 
from styles.auth import AuthStyles
from config.screen_config import screen_config

class PinView(QWidget):
    def __init__(self, user_id, auth_container, parent=None):
        super().__init__(parent or auth_container)
        self.user_id = user_id
        self.auth_container = auth_container
        self.valid_pin = "9856"  # Hardcoded valid PIN
        
        # Get container size from screen config
        width = screen_config.get_size('auth_container_width')
        height = screen_config.get_size('auth_container_height')
        self.setFixedSize(width, height)
        
        self.setStyleSheet(AuthStyles.CONTAINER(
            screen_config.get_size('container_margin')
        ))
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        margin = screen_config.get_size('container_margin')
        spacing = screen_config.get_size('section_spacing')
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(spacing)

        # PIN Label
        label_container = QHBoxLayout()
        self.lbl_pin = QLabel(f"PIN for User ID {self.user_id}", alignment=Qt.AlignCenter)
        self.lbl_pin.setStyleSheet(AuthStyles.LABEL_TEXT(
            screen_config.get_size('label_padding'),
            screen_config.get_size('label_font_size')
        ))
        width = screen_config.get_size('auth_label_width')
        height = screen_config.get_size('auth_label_height')
        self.lbl_pin.setFixedSize(width, height)
        
        # Add stretch before and after the label to center it
        label_container.addStretch()
        label_container.addWidget(self.lbl_pin)
        label_container.addStretch()
        
        layout.addLayout(label_container)

        # Input Fields
        self.pin_input = UserInput(is_pin=True)
        layout.addWidget(self.pin_input)

        # Keypad container
        keypad_container = QVBoxLayout()
        keypad_container.setSpacing(screen_config.get_size('keypad_spacing'))
        
        # Number pad grid
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
            btn.setStyleSheet(AuthStyles.KEYPAD_BUTTON(
                screen_config.get_size('keypad_font_size'),
                screen_config.get_size('keypad_padding')
            ))
            btn.clicked.connect(lambda _, num=idx+1: self._on_number_click(num))
            grid.addWidget(btn, row, col)

        keypad_container.addLayout(grid)

        # Action buttons
        action_row = QHBoxLayout()
        action_row.setSpacing(keypad_spacing)
        
        # Get action button sizes
        action_width = screen_config.get_size('action_button_width')
        action_height = screen_config.get_size('action_button_height')

        self.btn_clear = QPushButton("Clear")
        btn_0 = QPushButton("0")
        self.btn_cancel = QPushButton("Cancel")
        
        # Style the '0' button like other keypad buttons
        btn_0.setFixedSize(button_width, button_height)
        btn_0.setStyleSheet(AuthStyles.KEYPAD_BUTTON(
            screen_config.get_size('keypad_font_size'),
            screen_config.get_size('keypad_padding')
        ))

        # Style action buttons
        for btn in [self.btn_clear, self.btn_cancel]:
            btn.setFixedSize(action_width, action_height)
            btn.setStyleSheet(AuthStyles.KEYPAD_BUTTON(
                screen_config.get_size('keypad_font_size'),
                screen_config.get_size('keypad_padding')
            ))
        
        self.btn_clear.setEnabled(False)
        btn_0.clicked.connect(lambda: self._on_number_click(0))
        self.btn_clear.clicked.connect(self.pin_input.remove_digit)
        self.btn_cancel.clicked.connect(self._handle_cancel)

        action_row.addWidget(self.btn_clear)
        action_row.addWidget(btn_0)
        action_row.addWidget(self.btn_cancel)

        keypad_container.addLayout(action_row)
        layout.addLayout(keypad_container)

        # Sign In container
        signin_container = QHBoxLayout()
        signin_container.setSpacing(0)

        self.btn_sign_in = QPushButton("Sign In")
        signin_width = screen_config.get_size('signin_button_width')
        signin_height = screen_config.get_size('signin_button_height')
        self.btn_sign_in.setFixedSize(signin_width, signin_height)
        self.btn_sign_in.setEnabled(False)
        self.btn_sign_in.setStyleSheet(AuthStyles.KEYPAD_BUTTON(
            screen_config.get_size('keypad_font_size'),
            screen_config.get_size('keypad_padding')
        ))

        # Add button to container with stretches for centering
        signin_container.addStretch()
        signin_container.addWidget(self.btn_sign_in)
        signin_container.addStretch()

        # Add the container to main layout
        layout.addLayout(signin_container)

        # Connect signals
        self.pin_input.input_changed.connect(self._update_button_states)
        self.btn_sign_in.clicked.connect(self._handle_sign_in)

    def _on_number_click(self, number):
        """Handle number button clicks"""
        self.pin_input.add_digit(str(number))
        self._reset_pin_label()  # Reset label when typing starts

    def _reset_pin_label(self):
        """Restore PIN label to original state"""
        self.lbl_pin.setText(f"PIN for User ID {self.user_id}")
        self.lbl_pin.setStyleSheet(AuthStyles.LABEL_TEXT(
            screen_config.get_size('label_padding'),
            screen_config.get_size('label_font_size')
        ))

    def _update_button_states(self, digits):
        """Update button states based on input"""
        has_digits = self.pin_input.has_digits()
        is_complete = self.pin_input.is_complete()
        
        # Update Clear button
        self.btn_clear.setEnabled(has_digits)
        
        # Update Sign In button
        self.btn_sign_in.setEnabled(is_complete)
        self.btn_sign_in.setStyleSheet(
            AuthStyles.NEXT_BUTTON_ACTIVE(
                screen_config.get_size('keypad_font_size'),
                screen_config.get_size('keypad_padding')
            ) if is_complete
            else AuthStyles.KEYPAD_BUTTON(
                screen_config.get_size('keypad_font_size'),
                screen_config.get_size('keypad_padding')
            )
        )
        
        # Update number buttons (0-9)
        for btn in self.findChildren(QPushButton):
            if btn.text().isdigit():
                btn.setEnabled(not is_complete)

    def _handle_cancel(self):
        """Handle Cancel button click"""
        # Reset the label and input before going cancel
        self._reset_pin_label()
        self.pin_input.clear_all()
        # Switch cancel to user ID view
        self.auth_container.switch_to_user_id_view()

    def _handle_sign_in(self):
        """Handle Sign In button click"""
        if self.pin_input.is_complete():
            entered_pin = "".join(self.pin_input.digits)
            if entered_pin == self.valid_pin:
                self._show_pos_view()
            else:
                self._show_invalid_pin()

    def _show_invalid_pin(self):
        """Show invalid PIN message and clear input"""
        self.lbl_pin.setText(f"Invalid PIN for User ID {self.user_id}")
        self.lbl_pin.setStyleSheet(AuthStyles.LABEL_TEXT_INVALID(
            screen_config.get_size('label_padding'),
            screen_config.get_size('label_font_size')
        ))
        self.pin_input.clear_all()
        self._update_button_states([])  # Reset button states

    def keyPressEvent(self, event):
        """Handle physical keyboard input"""
        key = event.key()
        
        # Number keys (0-9)
        if Qt.Key_0 <= key <= Qt.Key_9 and not self.pin_input.is_complete():
            digit = str(key - Qt.Key_0)
            self.pin_input.add_digit(digit)
            self._reset_pin_label()  # Reset label when typing starts

        # Backspace
        elif key == Qt.Key_Backspace:
            self.pin_input.remove_digit()
            self._reset_pin_label()  # Reset label when removing digits

        # Enter/Return
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            if self.pin_input.is_complete():
                self._handle_sign_in()
        
        # Ignore other keys
        else:
            super().keyPressEvent(event)

    def _show_pos_view(self):
        """Switch to POS view after successful login"""
        # Get the main window by traversing up the parent hierarchy
        parent = self.auth_container.parent()
        while parent and not isinstance(parent, QMainWindow):
            parent = parent.parent()
            
        if parent:
            main_window = parent  # This is our QMainWindow instance
            
            # Hide the auth container
            self.auth_container.hide()
            
            # Find and hide the logo container
            logo_label = main_window.findChild(QLabel)
            if logo_label:
                logo_label.hide()
            
            # Create and show POS view
            pos_view = POSView(self.user_id, main_window)
            main_window.setCentralWidget(pos_view)
            pos_view.show()