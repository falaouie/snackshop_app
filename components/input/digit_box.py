from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from styles.auth import AuthStyles
from config.screen_config import screen_config

class DigitBox(QLabel):
    """A single digit box for PIN/ID input display"""
    
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
        """Update the displayed digit and styling"""
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