from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from styles.auth_styles import AuthStyles
from styles.layouts import layout_config 

class DigitBox(QLabel):
    """A single digit box for PIN/ID input display"""
    
    def __init__(self, is_pin=False):
        super().__init__()
        self.is_pin = is_pin  # Whether this is a PIN input
        
        # Get sizes from layout_config
        digit_box_config = layout_config.get_instance().get_digit_box_config()

        self.setFixedSize(digit_box_config['width'], digit_box_config['height'])
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(AuthStyles.DIGIT_BOX_EMPTY(
            digit_box_config['padding'],
            digit_box_config['font_size']
        ))
        
    def update_digit(self, value):
        """Update the displayed digit and styling"""
        digit_box_config = layout_config.get_instance().get_digit_box_config()

        if value:
            display_value = "*" if self.is_pin else value
            self.setText(display_value)
            self.setStyleSheet(AuthStyles.DIGIT_BOX_FILLED(
                digit_box_config['padding'],
                digit_box_config['font_size']
            ))
        else:
            self.clear()
            self.setStyleSheet(AuthStyles.DIGIT_BOX_EMPTY(
                digit_box_config['padding'],
                digit_box_config['font_size']
            ))