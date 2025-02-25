from typing import Dict, Any
from config.screen_config import screen_config

class KeyboardStyles:
    # Base styles for the keyboard container
    KEYBOARD_BASE = """
        VirtualKeyboard {
            background: darkgrey;
            border-radius: 10px;
            padding: 10px;
        }
    """

    # Handle bar styles
    HANDLE_BAR = """
        QFrame {
            background: #444444;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }
    """

    # Control button styles (minimize, restore)
    CONTROL_BUTTONS = """
        QPushButton {
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 20px;
            font-weight: bold;
            width: 40px;
        }
        QPushButton:hover {
            background: rgba(255, 255, 255, 0.1);
        }
    """

    # Regular key button styles
    KEY_BUTTONS = """
        QPushButton {
            background: white;
            border: 1px solid #DEDEDE;
            border-radius: 10px;
            padding: 8px;
            color: #333;
            font-size: 18px;
        }
        QPushButton:hover {
            background: #F8F9FA;
            border-color: #2196F3;
        }
    """

    # Special key styles (Enter, Space)
    SPACE_KEY = """
        QPushButton {
            background: white;
            border: 1px solid #DEDEDE;
            border-radius: 8px;
            color: #333;
            font-size: 14px;
            min-width: 300px;
            margin-left: 70px;
            margin-right: 50px;
            margin-bottom: 10px;
        }
        QPushButton:hover {
            background: #F8F9FA;
            border-color: #2196F3;
        }
    """

    ENTER_KEY = """
        QPushButton {
            background: #2196F3;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
            margin-right: 15px;
        }
        QPushButton:hover {
            background: #1E88E5;
        }
    """

class KeyboardConfig:
    """Configuration class for keyboard dimensions and layout"""
    
    _instance = None

    # Default dimensions
    DEFAULT_DIMENSIONS = {
        'key_width': 50,
        'key_height': 50,
        'space_width': 600,
        'space_height': 45,
        'enter_width': 175,
        'enter_height': 45,
        'handle_height': 40,
        'control_button_size': 40,
    }

    # Layout configuration
    LAYOUT = {
        'main_margins': (5, 5, 5, 5),
        'main_spacing': 5,
        'handle_margins': (10, 0, 10, 0),
        'handle_spacing': 8,
        'bottom_margins': (0, 0, 0, 10),
    }

    # Colors
    COLORS = {
        'background': 'darkgrey',
        'handle': '#444444',
        'key_border': '#DEDEDE',
        'key_hover_border': '#2196F3',
        'enter_background': '#2196F3',
        'enter_hover': '#1E88E5',
    }

    def __init__(self, screen_config_instance=None):
        """Initialize keyboard config, optionally with screen config"""
        self.screen_config = screen_config_instance
        if screen_config_instance:
            KeyboardConfig._instance = self

    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance"""
        if not cls._instance:
            cls._instance = KeyboardConfig(screen_config)
        return cls._instance
          
    def get_dimensions(self) -> Dict[str, int]:
        """Get keyboard dimensions based on screen config if available"""
        if self.screen_config:
            try:
                return {
                    'key_width': self.screen_config.get_size('keyboard_key_width'),
                    'key_height': self.screen_config.get_size('keyboard_key_height'),
                    'space_width': self.screen_config.get_size('keyboard_space_width'),
                    'space_height': self.screen_config.get_size('keyboard_space_height'),
                    'enter_width': self.screen_config.get_size('keyboard_enter_width'),
                    'enter_height': self.screen_config.get_size('keyboard_enter_height'),
                    'handle_height': self.screen_config.get_size('keyboard_handle_height'),
                    'control_button_size': self.screen_config.get_size('keyboard_control_button_size'),
                }
            except (AttributeError, KeyError):
                # Fallback to default if any value is missing
                print("Warning: Using default keyboard dimensions due to missing screen config values")
                return self.DEFAULT_DIMENSIONS.copy()
        return self.DEFAULT_DIMENSIONS.copy()

    def get_layout(self) -> Dict[str, Any]:
        """Get keyboard layout configuration"""
        if self.screen_config:
            try:
                spacing = self.screen_config.get_size('keyboard_spacing')
                return {
                    'main_margins': (spacing, spacing, spacing, spacing),
                    'main_spacing': spacing,
                    'handle_margins': (spacing + 5, 0, spacing + 5, 0),
                    'handle_spacing': spacing,
                    'bottom_margins': (0, 0, 0, spacing + 5),
                }
            except (AttributeError, KeyError):
                # Fallback to default if any value is missing
                print("Warning: Using default keyboard layout due to missing screen config values")
                return self.LAYOUT.copy()
        return self.LAYOUT.copy()

    def get_colors(self) -> Dict[str, str]:
        """Get keyboard color configuration"""
        return self.COLORS.copy()

class KeyboardEnabledInputStyles:
    """Styles for keyboard-enabled input fields"""
    
    BASE_INPUT = """
        QLineEdit {
            border: 1px solid #DEDEDE;
            border-radius: 20px;
            padding: 8px 12px;
            font-size: 14px;
            color: #333;
            background: white;
        }
        QLineEdit:focus {
            border-color: #2196F3;
            outline: none;
        }
    """

    SEARCH_INPUT = """
        QLineEdit {
            border: 1px solid #DEDEDE;
            border-radius: 20px;
            padding: 8px 40px 8px 40px;
            font-size: 14px;
            color: #333;
            min-width: 300px;
            max-width: 400px;
            background: white;
        }
        QLineEdit:focus {
            border-color: #2196F3;
            outline: none;
        }
    """

# Create a global instance
keyboard_config = KeyboardConfig()