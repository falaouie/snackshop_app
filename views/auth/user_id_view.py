from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                            QPushButton, QGridLayout, QHBoxLayout)
from PyQt5.QtCore import Qt
from components.input import UserInput
from styles.auth import AuthStyles
from styles.layouts import layout_config

class UserIDView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_container = parent
        self.number_buttons = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Get configurations
        spacing_config = layout_config.get_instance().get_spacing_config()
        label_config = layout_config.get_instance().get_label_config()
        keypad_config = layout_config.get_instance().get_keypad_config()
        action_config = layout_config.get_instance().get_action_buttons_config()
        
        # Apply spacing
        layout.setContentsMargins(spacing_config['container_margin'], 
                                spacing_config['container_margin'],
                                spacing_config['container_margin'], 
                                spacing_config['container_margin'])
        layout.setSpacing(spacing_config['section_spacing'])
        
        # User ID Label
        label_container = QHBoxLayout()
        self.lbl_user_id = QLabel("User ID", alignment=Qt.AlignCenter)
        self.lbl_user_id.setFixedSize(label_config['width'], label_config['height'])
        self.lbl_user_id.setStyleSheet(AuthStyles.LABEL_TEXT(
            spacing_config['label_padding'],
            label_config['font_size']
        ))
        
        label_container.addStretch()
        label_container.addWidget(self.lbl_user_id)
        label_container.addStretch()
        
        layout.addLayout(label_container)

        # Input Fields
        self.user_input = UserInput()
        layout.addWidget(self.user_input)

        # Keypad
        grid = QGridLayout()
        grid.setSpacing(keypad_config['spacing'])

        # Number buttons 1-9
        positions = [(i//3, i%3) for i in range(9)]
        
        for idx, (row, col) in enumerate(positions):
            btn = QPushButton(str(idx+1))
            btn.setFixedSize(keypad_config['button_width'], 
                           keypad_config['button_height'])
            btn.setStyleSheet(AuthStyles.KEYPAD_BUTTON(
                keypad_config['font_size'],
                keypad_config['padding']
            ))
            btn.clicked.connect(lambda _, num=idx+1: self._on_number_click(num))
            self.number_buttons.append(btn)
            grid.addWidget(btn, row, col)

        # Action buttons
        action_row = QHBoxLayout()
        action_row.setSpacing(keypad_config['spacing'])

        self.btn_clear = QPushButton("Clear")
        btn_0 = QPushButton("0")
        self.btn_next = QPushButton("Next")
        
        # Style the '0' button like other keypad buttons
        btn_0.setFixedSize(keypad_config['button_width'], 
                          keypad_config['button_height'])
        btn_0.setStyleSheet(AuthStyles.KEYPAD_BUTTON(
            keypad_config['font_size'],
            keypad_config['padding']
        ))

        # Style action buttons
        for btn in [self.btn_clear, self.btn_next]:
            btn.setFixedSize(action_config['action_width'], 
                           action_config['action_height'])
            btn.setStyleSheet(AuthStyles.KEYPAD_BUTTON(
                keypad_config['font_size'],
                keypad_config['padding']
            ))
        
        # Initialize action button states
        self.btn_clear.setEnabled(False)
        self.btn_next.setEnabled(False)
        
        # Connect buttons
        self.btn_clear.clicked.connect(self.user_input.remove_digit)
        btn_0.clicked.connect(lambda: self._on_number_click(0))
        self.btn_next.clicked.connect(self._handle_next)
        
        self.number_buttons.append(btn_0)

        action_row.addWidget(self.btn_clear)
        action_row.addWidget(btn_0)
        action_row.addWidget(self.btn_next)

        layout.addLayout(grid)
        layout.addLayout(action_row)

        self.user_input.input_changed.connect(self._update_button_states)

    def _update_button_states(self, digits):
        """Update button states based on input"""
        has_digits = self.user_input.has_digits()
        is_complete = self.user_input.is_complete()
        
        # Update Clear button
        self.btn_clear.setEnabled(has_digits)
        
        # Get configurations for styling
        keypad_config = layout_config.get_instance().get_keypad_config()
        
        # Update Next button
        self.btn_next.setEnabled(is_complete)
        self.btn_next.setStyleSheet(
            AuthStyles.NEXT_BUTTON_ACTIVE(
                keypad_config['font_size'],
                keypad_config['padding']
            ) if is_complete
            else AuthStyles.KEYPAD_BUTTON(
                keypad_config['font_size'],
                keypad_config['padding']
            )
        )
        
        # Update number buttons (0-9)
        for btn in self.number_buttons:
            btn.setEnabled(not is_complete)

    def _show_invalid_user_id(self):
        self.lbl_user_id.setText("Invalid User ID")
        spacing_config = layout_config.get_instance().get_spacing_config()
        label_config = layout_config.get_instance().get_label_config()
        self.lbl_user_id.setStyleSheet(AuthStyles.LABEL_TEXT_INVALID(
            spacing_config['label_padding'],
            label_config['font_size']
        ))

    def _reset_user_id_label(self):
        self.lbl_user_id.setText("User ID")
        spacing_config = layout_config.get_instance().get_spacing_config()
        label_config = layout_config.get_instance().get_label_config()
        self.lbl_user_id.setStyleSheet(AuthStyles.LABEL_TEXT(
            spacing_config['label_padding'],
            label_config['font_size']
        ))

    # Other methods remain unchanged as they don't use configuration
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