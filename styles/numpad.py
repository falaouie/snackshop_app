"""Numpad styling and configuration"""
from config.screen_config import screen_config

class NumpadConfig:
    """Configuration for numpad dimensions and layout"""
    _instance = None
    
    def __init__(self, screen_config=None):
        self.screen_config = screen_config
    
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            from config.screen_config import screen_config
            cls._instance = cls(screen_config)
        return cls._instance
        
    def get_dimensions(self):
        """Get button dimensions directly from layouts.py values"""
        return {
            'button_size': self.screen_config.get_size('numpad_button_size'),
            'display_height': self.screen_config.get_size('numpad_display_height'),
            'width': self.screen_config.get_size('numpad_width')
        }
    
    def get_layout(self):
        """Get layout configuration with detailed margin control"""
        return {
            'main_margins': [
                self.screen_config.get_size('numpad_main_margin_left'),
                self.screen_config.get_size('numpad_main_margin_top'),
                self.screen_config.get_size('numpad_main_margin_right'),
                self.screen_config.get_size('numpad_main_margin_bottom')
            ],
            'grid_margins': [
                self.screen_config.get_size('numpad_grid_margin_left'),
                self.screen_config.get_size('numpad_grid_margin_top'),
                self.screen_config.get_size('numpad_grid_margin_right'),
                self.screen_config.get_size('numpad_grid_margin_bottom')
            ],
            'grid_spacing': self.screen_config.get_size('numpad_spacing')
        }


class NumpadStyles:
    """Styles for numpad components"""
    
    # Container style
    CONTAINER = """
        QFrame {
            background: white;
            border: 1px solid #DEDEDE;
            border-radius: 5px;
        }
    """
    
    # Grid container style
    GRID_CONTAINER = """
        QFrame {
            background: transparent;
            border: none;
        }
    """
    
    @staticmethod
    def get_display_style(config):
        """Get display style with font size from config"""
        font_size = config.screen_config.get_size('numpad_font_size')
        return f"""
            QLineEdit {{
                background: white;
                border: 1px solid #DEDEDE;
                border-radius: 4px;
                font-size: {font_size}px;
                font-weight: 500;
                color: #333;
                padding: 5px 10px;
            }}
        """
    
    @staticmethod
    def get_number_button_style(config):
        """Get number button style with font size from config"""
        font_size = config.screen_config.get_size('numpad_font_size')
        return f"""
            QPushButton {{
                background: white;
                border: 1px solid #DEDEDE;
                border-radius: 4px;
                padding: 0px;
                font-size: {font_size}px;
                color: #333;
            }}
            QPushButton:hover {{
                background: #F5F5F5;
                border-color: #2196F3;
            }}
        """