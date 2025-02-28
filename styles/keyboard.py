"""Keyboard styling and configuration"""
from config.screen_config import screen_config

class KeyboardConfig:
    """Configuration for keyboard dimensions and layout"""
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
        """Get keyboard dimensions from layout config"""
        return {
            'key_width': self.screen_config.get_size('keyboard_key_width'),
            'key_height': self.screen_config.get_size('keyboard_key_height'),
            'space_width': self.screen_config.get_size('keyboard_space_width'),
            'space_height': self.screen_config.get_size('keyboard_space_height'),
            'enter_width': self.screen_config.get_size('keyboard_enter_width'),
            'enter_height': self.screen_config.get_size('keyboard_enter_height'),
            'handle_height': self.screen_config.get_size('keyboard_handle_height'),
            'control_button_size': self.screen_config.get_size('keyboard_control_button_size')
        }
    
    def get_layout(self):
        """Get keyboard layout configuration"""
        return {
            'main_margins': [10, 5, 10, 10],  # Left, top, right, bottom
            'main_spacing': self.screen_config.get_size('keyboard_spacing'),
            'handle_margins': [5, 0, 5, 0],
            'handle_spacing': 8
        }

class KeyboardEnabledInputStyles:
    """Styles for input fields that work with virtual keyboard"""
    
    # Base input style
    BASE_INPUT = """
        QLineEdit {
            border: 1px solid #DEDEDE;
            border-radius: 4px;
            padding: 5px 10px;
            background: grey;
            color: #333;
        }
        QLineEdit:focus {
            border-color: #2196F3;
        }
    """
    
    # Search input style
    SEARCH_INPUT = """
        QLineEdit {
            border: 1px solid #DEDEDE;
            border-radius: 20px;
            padding: 5px 30px;
            background: white;
            color: #333;
        }
        QLineEdit:focus {
            border-color: #2196F3;
        }
    """

class KeyboardStyles:
    """Styles for keyboard and keyboard-enabled inputs"""
    
    # Base keyboard style
    KEYBOARD_BASE = """
        QWidget {
            background: darkgrey;
        }
    """
    
    # Handle bar style
    HANDLE_BAR = """
        QFrame {
            background: grey;
            border-bottom: 1px solid #DEDEDE;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }
    """
    
    @staticmethod
    def get_key_style(config):
        """Get key button style with configurable font size
        
        Args:
            config: Keyboard configuration
        """
        return f"""
            QPushButton {{
                background: white;
                border: 1px solid #DEDEDE;
                border-radius: 4px;
                color: #333;
                font-size: {config.screen_config.get_size('keyboard_font_size')}px;
                padding: {config.screen_config.get_size('keyboard_padding')}px;
            }}
            QPushButton:hover {{
                background: #F5F5F5;
                border-color: #2196F3;
            }}
        """
    
    @staticmethod
    def get_space_key_style(config):
        """Get space key style with configurable font size
        
        Args:
            config: Keyboard configuration
        """
        return f"""
            QPushButton {{
                background: white;
                border: 1px solid #DEDEDE;
                border-radius: 4px;
                color: #333;
                font-size: {config.screen_config.get_size('keyboard_font_size')}px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background: #F5F5F5;
                border-color: #2196F3;
            }}
        """
    
    @staticmethod
    def get_enter_key_style(config):
        """Get enter key style with configurable font size
        
        Args:
            config: Keyboard configuration
        """
        return f"""
            QPushButton {{
                background: #2196F3;
                border: none;
                border-radius: 4px;
                color: white;
                font-size: {config.screen_config.get_size('keyboard_font_size')}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: #1976D2;
            }}
        """
    
    @staticmethod
    def get_control_button_style(config):
        """Get control button style with configurable font size
        
        Args:
            config: Keyboard configuration
        """
        return f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 3px;
                color: #666;
                font-size: {config.screen_config.get_size('keyboard_font_size') - 2}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: #E0E0E0;
            }}
        """