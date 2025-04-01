from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                            QPushButton, QGridLayout, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from components.input import UserInput
from styles.auth_styles import AuthStyles
from config.layouts import AuthLayoutConfig

class UserIDView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Get config instance
        self.config = AuthLayoutConfig.get_instance()
        self.parent_container = parent
        self.number_buttons = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)  # Align all to the top

        keypad_config = self.config.get_keypad_config()
        action_config = self.config.get_action_buttons_config()
        
        container_specs = self.config.get_auth_layout()

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
        
        # User ID Label
        label_container = QHBoxLayout()
        self.lbl_user_id = QLabel("User ID", alignment=Qt.AlignCenter)

        # Explicitly set fixed width and height
        label_width = container_specs['label_width']
        label_height = container_specs['label_height']
        self.lbl_user_id.setFixedSize(label_width, label_height)

        # set style
        self.lbl_user_id.setStyleSheet(AuthStyles.get_auth_label_text_style())

        # Apply font size
        font = QFont()
        font_size = container_specs['font_size']
        font.setPointSize(font_size)
        self.lbl_user_id.setFont(font)

        label_container.addStretch()
        label_container.addWidget(self.lbl_user_id)
        label_container.addStretch()
        
        layout.addLayout(label_container)
        
        # Add specific spacing between label and input
        layout.addSpacing(container_specs['label_to_input_spacing'])

        # Input Fields
        self.user_input = UserInput()
        layout.addWidget(self.user_input)
        
        # Add specific spacing between input and keypad
        layout.addSpacing(container_specs['input_to_keypad_spacing'])

        # Keypad
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
        self.btn_backspace = QPushButton("←")  # Backspace button with arrow symbol
        
        # Style the '0' button like other keypad buttons
        btn_0.setFixedSize(keypad_config['button_width'], 
                          keypad_config['button_height'])
        # set style
        btn_0.setStyleSheet(AuthStyles.get_keypad_button_style())
        btn_0.setFont(pad_font)

        # Style action buttons
        for btn in [self.btn_clear, self.btn_backspace]:
            btn.setFixedSize(action_config['action_width'], 
                           action_config['action_height'])
            # set style
            btn.setStyleSheet(AuthStyles.get_keypad_button_style())
            btn.setFont(pad_font)
        
        # Initialize action button states
        self.btn_clear.setEnabled(False)
        self.btn_backspace.setEnabled(False)
        
        # Connect buttons
        self.btn_clear.clicked.connect(self.user_input.clear_all)
        self.btn_backspace.clicked.connect(self.user_input.remove_digit)
        btn_0.clicked.connect(lambda: self._on_number_click(0))
        
        self.number_buttons.append(btn_0)

        action_row.addWidget(self.btn_clear)
        action_row.addWidget(btn_0)
        action_row.addWidget(self.btn_backspace)

        layout.addLayout(action_row)
        
        # Add spacing before Next button
        layout.addSpacing(15)  # A little more space before the next button

        # Next button container
        next_container = QHBoxLayout()
        next_container.setSpacing(action_config['buttons_spacing'])

        self.btn_next = QPushButton("Next")
        self.btn_next.setFixedSize(action_config['signin_width'], 
                                  action_config['signin_height'])
        self.btn_next.setEnabled(False)
        # set style
        self.btn_next.setStyleSheet(AuthStyles.get_keypad_button_style())
        self.btn_next.setFont(pad_font)
        self.btn_next.clicked.connect(self._handle_next)

        # Add button to container with stretches for centering
        next_container.addStretch()
        next_container.addWidget(self.btn_next)
        next_container.addStretch()

        # Add the container to main layout
        layout.addLayout(next_container)
        
        # Add a stretch at the end to push all content to the top
        layout.addStretch(1)

        self.user_input.input_changed.connect(self._update_button_states)

    def _update_button_states(self, digits):
        """Update button states based on input"""
        has_digits = self.user_input.has_digits()
        is_complete = self.user_input.is_complete()
        
        # Update Clear button
        self.btn_clear.setEnabled(has_digits)
        
        # Update Backspace button
        self.btn_backspace.setEnabled(has_digits)
        
        # Update Next button
        self.btn_next.setEnabled(is_complete)

        # set style
        self.btn_next.setStyleSheet(
            AuthStyles.get_next_btn_active_style()
            if is_complete
            else AuthStyles.get_keypad_button_style()
            )
        
        # Update number buttons (0-9)
        for btn in self.number_buttons:
            btn.setEnabled(not is_complete)

    def _show_invalid_user_id(self):
        self.lbl_user_id.setText("Invalid User ID")
        container_specs = self.config.get_auth_layout()
        # Explicitly set fixed width and height
        label_width =  container_specs['label_width']
        label_height = container_specs['label_height']
        self.lbl_user_id.setFixedSize(label_width, label_height)

        # set style
        self.lbl_user_id.setStyleSheet(AuthStyles.get_auth_label_invalid_style())

        # Apply font size
        font = QFont()
        font_size = container_specs['font_size']
        font.setPointSize(font_size)
        self.lbl_user_id.setFont(font)

    def _reset_user_id_label(self):
        self.lbl_user_id.setText("User ID")
        container_specs = self.config.get_auth_layout()
        # Explicitly set fixed width and height
        label_width =  container_specs['label_width']
        label_height = container_specs['label_height']
        self.lbl_user_id.setFixedSize(label_width, label_height)

        # set style
        self.lbl_user_id.setStyleSheet(AuthStyles.get_auth_label_text_style())

        # Apply font size
        font = QFont()
        font_size = container_specs['font_size']
        font.setPointSize(font_size)
        self.lbl_user_id.setFont(font)

    def _on_number_click(self, number):
        self.user_input.add_digit(str(number))
        self._reset_user_id_label()

    def _handle_next(self):
        if self.user_input.is_complete():
            user_id = "".join(self.user_input.digits)
            if user_id == self.parent_container.valid_user_id:
                self.parent_container.switch_to_pin_view(user_id)
            else:
                self._show_invalid_user_id()

    def keyPressEvent(self, event):
        key = event.key()
        
        if Qt.Key_0 <= key <= Qt.Key_9 and not self.user_input.is_complete():
            digit = str(key - Qt.Key_0)
            self.user_input.add_digit(digit)
            self._reset_user_id_label()
        elif key == Qt.Key_Backspace:
            self.user_input.remove_digit()
            self._reset_user_id_label()
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            if self.user_input.is_complete():
                self._handle_next()
        else:
            super().keyPressEvent(event)

    def clear_all(self):
        self.user_input.clear_all()
        self._reset_user_id_label()