from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect

class ScreenConfig:
    """Handles screen detection and provides appropriate sizes for UI elements"""
    
    # Size configurations for different screen sizes
    SMALL = {
        # Logo dimensions
        'logo_width': 150,
        'logo_height': 56,

        # Auth container sizes
        'auth_container_width': 350,
        'auth_container_height': 400,
        
        # Input field sizes
        'input_field_height': 30,
        'input_digit_width': 30,
        
        # Button sizes
        'keypad_button_width': 60,
        'keypad_button_height': 40,
        'action_button_width': 60,
        'action_button_height': 40,
        
        # Spacing and margins
        'keypad_spacing': 10,
        'container_margin': 10,
        'section_spacing': 10
    }

    MEDIUM = {
        # Logo dimensions
        'logo_width': 200,
        'logo_height': 75,

        # Auth container sizes
        'auth_container_width': 400,
        'auth_container_height': 500,

        # Input field sizes
        'input_field_height': 40,
        'input_digit_width': 30,

        # Button sizes
        'keypad_button_width': 60,
        'keypad_button_height': 50,
        'action_button_width': 80,
        'action_button_height': 50,

        # Spacing and margins
        'keypad_spacing': 15,
        'container_margin': 15,
        'section_spacing': 15
    }

    LARGE = {
        # Logo dimensions
        'logo_width': 200,
        'logo_height': 100,

        # Auth container sizes
        'auth_container_width': 600,
        'auth_container_height': 700,
        'input_field_height': 60,
        'input_digit_width': 40,
        'keypad_button_width': 100,
        'keypad_button_height': 100,
        'action_button_width': 150,
        'action_button_height': 60,
        'keypad_spacing': 20,
        'container_margin': 30,
        'section_spacing': 25
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
        if self.width >= 1280 and self.height >= 1024:
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

# Create a singleton instance
screen_config = ScreenConfig()