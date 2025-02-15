from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from styles.auth import AuthStyles 
from config.screen_config import screen_config

class DigitBox(QLabel):
    def __init__(self, is_pin=False):
        super().__init__()
        self.is_pin = is_pin  # Whether this is a PIN input
        # Get sizes from config
        digit_width = screen_config.get_size('digit_input_width')
        digit_height = screen_config.get_size('digit_input_height')
        self.setFixedSize(digit_width, digit_height)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(AuthStyles.DIGIT_BOX_EMPTY(
            screen_config.get_size('digit_padding'),
            screen_config.get_size('digit_font_size')
        ))
        
    def update_digit(self, value):
        if value:
            display_value = "*" if self.is_pin else value
            self.setText(display_value)
            self.setStyleSheet(AuthStyles.DIGIT_BOX_FILLED(
                screen_config.get_size('digit_padding'),
                screen_config.get_size('digit_font_size')
            ))
        else:
            self.clear()
            self.setStyleSheet(AuthStyles.DIGIT_BOX_EMPTY(
                screen_config.get_size('digit_padding'),
                screen_config.get_size('digit_font_size')
            ))

class UserInput(QWidget):
    input_changed = pyqtSignal(list)  # Signal when input changes
    
    def __init__(self, is_pin=False):
        super().__init__()
        self.is_pin = is_pin  # Whether this is a PIN input
        self.digits = ["", "", "", ""]  # Track input digits
        self.current_position = 0       # Current digit being edited
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QHBoxLayout()
        # Get margin and spacing from config
        digit_margin = screen_config.get_size('container_margin')
        digit_spacing = screen_config.get_size('section_spacing')
        layout.setContentsMargins(0, digit_margin//2, 0, digit_margin//2)
        layout.setSpacing(digit_spacing)
        
        self.digit_boxes = []
        for _ in range(4):
            box = DigitBox(is_pin=self.is_pin)  # Pass is_pin to DigitBox
            self.digit_boxes.append(box)
            layout.addWidget(box)
            
        self.setLayout(layout)
        
    def add_digit(self, digit):
        if self.current_position < 4:
            self.digits[self.current_position] = digit
            self.digit_boxes[self.current_position].update_digit(digit)
            self.current_position += 1
            self.input_changed.emit(self.digits)
            
    def remove_digit(self):
        if self.current_position > 0:
            self.current_position -= 1
            self.digits[self.current_position] = ""
            self.digit_boxes[self.current_position].update_digit("")
            self.input_changed.emit(self.digits)
            
    def clear_all(self):
        self.digits = ["", "", "", ""]
        self.current_position = 0
        for box in self.digit_boxes:
            box.update_digit("")
        self.input_changed.emit(self.digits)
        
    def has_digits(self):
        """Check if any digits are entered"""
        return any(self.digits)
        
    def is_complete(self):
        """Check if all 4 digits are entered"""
        return all(self.digits)