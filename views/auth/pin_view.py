from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                           QGridLayout, QHBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from components.input import UserInput
from views.pos.pos_view import POSView
from styles.auth_styles import AuthStyles
from config.layouts import AuthLayoutConfig

class PinView(QWidget):
    def __init__(self, user_name, auth_container, parent=None):
        super().__init__(parent or auth_container)
        self.user_id = user_name
        self.auth_container = auth_container
        self.valid_pin = "9856"  # Hardcoded valid PIN
        self.user_name = "Fadi"

        # Get config instance
        self.config = AuthLayoutConfig.get_instance()
        self.number_buttons = []
        
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)  # Align all to the top

        # Get container dimensions
        container_specs = self.config.get_auth_layout()
        keypad_config = self.config.get_keypad_config()
        action_config = self.config.get_action_buttons_config()

        # Explicitly set fixed width and height from config
        width = container_specs['container_width']
        height = container_specs['container_height']
        self.setFixedSize(width, height)

        # Set container margins
        layout.setContentsMargins(
            container_specs['container_margin'],
            container_specs['container_margin'],
            container_specs['container_margin'],
            container_specs['container_margin']
        )
        
        # Remove the generic spacing and add specific ones where needed
        layout.setSpacing(0)  # No default spacing between all elements

        # Add top margin before the label
        layout.addSpacing(container_specs['label_top_margin'])
        
        # PIN Label
        label_container = QHBoxLayout()
        self.lbl_pin = QLabel(f"PIN for User {self.user_name}", alignment=Qt.AlignCenter)
        
        # Explicitly set fixed width and height
        label_width = container_specs['label_width']
        label_height = container_specs['label_height']
        self.lbl_pin.setFixedSize(label_width, label_height)

        # set style
        self.lbl_pin.setStyleSheet(AuthStyles.get_auth_label_text_style())

        # Apply font size
        font = QFont()
        font_size = container_specs['font_size']
        font.setPointSize(font_size)
        self.lbl_pin.setFont(font)
        
        # Add stretch before and after the label to center it
        label_container.addStretch()
        label_container.addWidget(self.lbl_pin)
        label_container.addStretch()
        
        layout.addLayout(label_container)
        
        # Add specific spacing between label and input
        layout.addSpacing(container_specs['label_to_input_spacing'])

        # Input Fields
        self.pin_input = UserInput(is_pin=True)
        layout.addWidget(self.pin_input)
        
        # Add specific spacing between input and keypad
        layout.addSpacing(container_specs['input_to_keypad_spacing'])

        # Number pad grid
        grid = QGridLayout()
        # Use specific keypad button spacing
        grid.setSpacing(keypad_config['buttons_spacing'])

        pad_font = QFont()
        pad_font_size = keypad_config['font_size']
        pad_font.setPointSize(pad_font_size)
        
        # Number buttons 1-9
        positions = [(i//3, i%3) for i in range(9)]
        
        for idx, (row, col) in enumerate(positions):
            btn = QPushButton(str(idx+1))
            btn.setFixedSize(keypad_config['button_width'], 
                            keypad_config['button_height'])
            # set style
            btn.setStyleSheet(AuthStyles.get_keypad_button_style())
            btn.setFont(pad_font)
            
            btn.clicked.connect(lambda _, num=idx+1: self._on_number_click(num))
            self.number_buttons.append(btn)
            grid.addWidget(btn, row, col)

        layout.addLayout(grid)
        
        # Add specific spacing between keypad and action buttons
        layout.addSpacing(container_specs['keypad_to_action_spacing'])

        # Action buttons
        action_row = QHBoxLayout()
        action_row.setSpacing(action_config['buttons_spacing'])
        
        self.btn_clear = QPushButton("Clear All")
        btn_0 = QPushButton("0")
        self.btn_cancel = QPushButton("Cancel")
        
        # Style the '0' button like other keypad buttons
        btn_0.setFixedSize(keypad_config['button_width'], 
                          keypad_config['button_height'])
        # set style
        btn_0.setStyleSheet(AuthStyles.get_keypad_button_style())
        btn_0.setFont(pad_font)
        self.number_buttons.append(btn_0)

        # Style action buttons
        for btn in [self.btn_clear, self.btn_cancel]:
            btn.setFixedSize(action_config['action_width'], 
                            action_config['action_height'])
            # set style
            btn.setStyleSheet(AuthStyles.get_keypad_button_style())
            btn.setFont(pad_font)
        
        # Initialize button states
        self.btn_clear.setEnabled(False)
        
        # Connect buttons
        btn_0.clicked.connect(lambda: self._on_number_click(0))
        self.btn_clear.clicked.connect(self.pin_input.clear_all)
        self.btn_cancel.clicked.connect(self._handle_cancel)

        action_row.addWidget(self.btn_clear)
        action_row.addWidget(btn_0)
        action_row.addWidget(self.btn_cancel)

        layout.addLayout(action_row)
        
        # Add spacing before the buttons row
        layout.addSpacing(15)  # A little more space before the buttons row
        
        # Sign In button row
        signin_container = QHBoxLayout()
        signin_container.setSpacing(action_config['buttons_spacing'])
        
        self.btn_sign_in = QPushButton("Sign In")
        self.btn_sign_in.setFixedSize(action_config['signin_width'], 
                                    action_config['signin_height'])
        
        self.btn_sign_in.setStyleSheet(AuthStyles.get_keypad_button_style())
        self.btn_sign_in.setFont(pad_font)
        
        self.btn_sign_in.setEnabled(False)
        
        # Connect button
        self.btn_sign_in.clicked.connect(self._handle_sign_in)
        
        # Center the button
        signin_container.addStretch()
        signin_container.addWidget(self.btn_sign_in)
        signin_container.addStretch()
        
        layout.addLayout(signin_container)
        
        # Add a stretch at the end to push everything to the top
        layout.addStretch(1)

        # Connect signals
        self.pin_input.input_changed.connect(self._update_button_states)

    def _on_number_click(self, number):
        """Handle number button clicks"""
        self.pin_input.add_digit(str(number))
        self._reset_pin_label()  # Reset label when typing starts

    def _reset_pin_label(self):
        """Restore PIN label to original state"""
        self.lbl_pin.setText(f"PIN for User {self.user_name}")
        
        container_specs = self.config.get_auth_layout()
        # Explicitly set fixed width and height
        label_width = container_specs['label_width']
        label_height = container_specs['label_height']
        self.lbl_pin.setFixedSize(label_width, label_height)

        # set style
        self.lbl_pin.setStyleSheet(AuthStyles.get_auth_label_text_style())

        # Apply font size
        font = QFont()
        font_size = container_specs['font_size']
        font.setPointSize(font_size)
        self.lbl_pin.setFont(font)

    def _update_button_states(self, digits):
        """Update button states based on input"""
        has_digits = self.pin_input.has_digits()
        is_complete = self.pin_input.is_complete()
        
        # Update Clear button
        self.btn_clear.setEnabled(has_digits)
        
        # Update Sign In button
        self.btn_sign_in.setEnabled(is_complete)
        
        # set style
        self.btn_sign_in.setStyleSheet(
            AuthStyles.get_next_btn_active_style()
            if is_complete
            else AuthStyles.get_keypad_button_style()
        )
        
        # Update number buttons (0-9)
        for btn in self.number_buttons:
            btn.setEnabled(not is_complete)

    def _handle_cancel(self):
        """Handle Cancel button click"""
        # Reset the label and input before going cancel
        self._reset_pin_label()
        self.pin_input.clear_all()
        # Import here to avoid circular import
        from ..view_manager import ViewManager
        # Use ViewManager to switch to user ID view
        ViewManager.get_instance().switch_to_user_id_view()

    def _handle_sign_in(self):
        """Handle Sign In button click"""
        if self.pin_input.is_complete():
            entered_pin = "".join(self.pin_input.digits)
            if entered_pin == self.valid_pin:
                # Import here to avoid circular import
                from ..view_manager import ViewManager
                ViewManager.get_instance().switch_to_pos_view(self.user_id, self.user_name)
            else:
                self._show_invalid_pin()

    def _show_invalid_pin(self):
        """Show invalid PIN message and clear input"""
        self.lbl_pin.setText(f"Invalid PIN for User {self.user_name}")
        
        container_specs = self.config.get_auth_layout()
        # Explicitly set fixed width and height
        label_width = container_specs['label_width']
        label_height = container_specs['label_height']
        self.lbl_pin.setFixedSize(label_width, label_height)

        # set style
        self.lbl_pin.setStyleSheet(AuthStyles.get_auth_label_invalid_style())

        # Apply font size
        font = QFont()
        font_size = container_specs['font_size']
        font.setPointSize(font_size)
        self.lbl_pin.setFont(font)
        
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
        
        # Escape (for cancel)
        elif key == Qt.Key_Escape:
            self._handle_cancel()
        
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