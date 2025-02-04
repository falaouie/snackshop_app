from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect

class ScreenConfig:
    """Handles screen detection and provides appropriate sizes for UI elements"""
    
    # Size configurations for different screen sizes
    SMALL = {
        # Logo dimensions
        'logo_width': 200,
        'logo_height': 100,

        # Auth container sizes
        'auth_container_width': 350,
        'auth_container_height': 400,
        
        # Input field sizes
        'digit_input_width': 40,
        'digit_input_height': 40,
        
        # Button sizes
        'keypad_button_width': 60,
        'keypad_button_height': 40,
        'action_button_width': 60,
        'action_button_height': 40,
        'signin_button_width': 120,
        'signin_button_height': 40,

        # Font sizes
        'keypad_font_size': 16,
        'label_font_size': 16,
        'digit_font_size': 14,

        # Padding
        'keypad_padding': 8,
        'label_padding': 8,
        'digit_padding': 5,
        
        # Spacing and margins
        'keypad_spacing': 10,
        'container_margin': 10,
        'section_spacing': 10
    }

    MEDIUM = {
        # Logo dimensions
        'logo_width': 300,
        'logo_height': 125,

        # Auth container sizes
        'auth_container_width': 400,
        'auth_container_height': 500,

        # Input field sizes
        'digit_input_width': 40,
        'digit_input_height': 40,

        # Button sizes
        'keypad_button_width': 50,
        'keypad_button_height': 50,
        'action_button_width': 80,
        'action_button_height': 50,
        'signin_button_width': 160,
        'signin_button_height': 50,
        'top_bar_btn_width': 100,
        'top_bar_btn_height': 40,

        # Font sizes
        'keypad_font_size': 18,
        'label_font_size': 18,
        'digit_font_size': 16,
        'top_bar_btn_font_size': 16,

        # Padding
        'keypad_padding': 10,
        'label_padding': 10,
        'digit_padding': 8,
        'top_bar_btn_padding': 8,

        # Spacing and margins
        'keypad_spacing': 15,
        'container_margin': 15,
        'section_spacing': 15
    }

    LARGE = {
        # Logo dimensions
        'logo_width': 300,
        'logo_height': 150,

        # Auth container sizes
        'auth_container_width': 500,
        'auth_container_height': 600,

        # Input field sizes
        'digit_input_width': 60,
        'digit_input_height': 60,

        # Button sizes
        'keypad_button_width': 100,
        'keypad_button_height': 60,
        'action_button_width': 150,
        'action_button_height': 60,
        'signin_button_width': 200,
        'signin_button_height': 60,

        # Font sizes
        'keypad_font_size': 24,
        'label_font_size': 18,
        'digit_font_size': 16,

        # Padding
        'keypad_padding': 5,
        'label_padding': 5,
        'digit_padding': 5,

        # Spacing and margins
        'keypad_spacing': 10,
        'container_margin': 15,
        'section_spacing': 10
    }

    def __init__(self):
        self.current_config = None
        
    def initialize(self):
        """Initialize screen configuration after QApplication is created"""
        if QApplication.instance():
            screen = QApplication.primaryScreen()
            if screen:
                geometry = screen.geometry()
                self.width = geometry.width()
                self.height = geometry.height()
                print(f"width: {self.width}")
                print(f"height: {self.height}")
                self._set_size_config()
            else:
                self.current_config = self.MEDIUM  # Fallback to medium if screen detection fails
        else:
            self.current_config = self.MEDIUM  # Fallback to medium if QApplication not created

    def _set_size_config(self):
        """Determine which size configuration to use based on screen resolution"""
        if self.width >= 1280 and self.height >= 1080:
            self.current_config = self.LARGE
            print(f"size: Large")
        elif self.width >= 1024 and self.height >= 768:
            self.current_config = self.MEDIUM
            print(f"size: Medium")
        else:
            self.current_config = self.SMALL
            print(f"size: Small")

    def get_size(self, element_name):
        """Get the size for a specific element based on current screen configuration"""
        if self.current_config is None:
            self.initialize()
        return self.current_config.get(element_name)
    
    def get_screen_dimensions(self):
        """Get the screen dimensions"""
        if self.width is None or self.height is None:
            self.initialize()
        return self.width, self.height

# Create a singleton instance
screen_config = ScreenConfig()