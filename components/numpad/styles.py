from config.screen_config import screen_config

class NumpadStyles:
    """Styles for the numpad component"""
    
    # Base container style
    CONTAINER = """
        QFrame {
            background: white;
            border: 1px solid #DEDEDE;
            border-radius: 4px;
        }
    """

    # Display style
    DISPLAY = """
        QLineEdit {
            border: 1px solid #DEDEDE;
            border-radius: 4px;
            padding: 8px;
            font-size: 24px;
            background: #F9F9F9;
        }
        QLineEdit:disabled {
            background: #F9F9F9;
            color: #333;
        }
    """

    # QTY mode button style
    QTY_BUTTON = """
        QPushButton {
            background: white;
            border: 1px solid #DEDEDE;
            border-radius: 4px;
            padding: 8px;
            font-size: 16px;
        }
        QPushButton:hover {
            background: #F5F5F5;
        }
        QPushButton:checked {
            background: #007AFF;
            color: white;
            border: none;
        }
        QPushButton:pressed {
            background: #EBEBEB;
        }
    """

    # Number button style
    NUMBER_BUTTON = """
        QPushButton {
            background: white;
            border: 1px solid #DEDEDE;
            border-radius: 4px;
            padding: 2px;
        }
        QPushButton:hover {
            background: #F5F5F5;
        }
        QPushButton:pressed {
            background: #EBEBEB;
        }
        QPushButton:disabled {
            background: #F5F5F5;
            color: #999;
        }
    """

class NumpadConfig:
    """Configuration for numpad dimensions and layout"""
    
    _instance = None

    # Default dimensions
    DIMENSIONS = {
        'width': 350,           # Total numpad width
        'display_height': 45,   # Height of display area
        'button_size': 45,      # Size of number buttons
        'qty_button_size': 70,  # Size of QTY button
        'spacing': 8,           # Spacing between elements
    }

    # Layout configuration
    LAYOUT = {
        'main_margins': (2, 2, 2, 2),
        'grid_margins': (0, 0, 0, 0),
        'grid_spacing': 5,
        'display_row_spacing': 5,  # Spacing between QTY button and display
    }

    def __init__(self, screen_config_instance=None):
        """Initialize numpad config, optionally with screen config"""
        self.screen_config = screen_config_instance
        if screen_config_instance:
            NumpadConfig._instance = self

    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance"""
        if not cls._instance:
            cls._instance = NumpadConfig(screen_config)
        return cls._instance

    def get_dimensions(self):
        """Get numpad dimensions based on screen config if available"""
        if self.screen_config:
            try:
                return {
                    'width': self.screen_config.get_size('numpad_width'),
                    'display_height': self.screen_config.get_size('numpad_display_height'),
                    'button_size': self.screen_config.get_size('numpad_button_size'),
                    'qty_button_size': self.screen_config.get_size('numpad_button_size'),
                    'spacing': self.screen_config.get_size('numpad_spacing'),
                }
            except (AttributeError, KeyError):
                # Fallback to default if any value is missing
                print("Warning: Using default numpad dimensions due to missing screen config values")
                return self.DEFAULT_DIMENSIONS.copy()
        return self.DEFAULT_DIMENSIONS.copy()

    def get_layout(self):
        """Get numpad layout configuration based on screen config if available"""
        if self.screen_config:
            try:
                spacing = self.screen_config.get_size('numpad_spacing')
                return {
                    'main_margins': (spacing, spacing, spacing, spacing),
                    'grid_margins': (2, 2, 2, 2),
                    'grid_spacing': spacing,
                    'display_row_spacing': spacing,
                }
            except (AttributeError, KeyError):
                # Fallback to default if any value is missing
                print("Warning: Using default numpad layout due to missing screen config values")
                return self.DEFAULT_LAYOUT.copy()
        return self.DEFAULT_LAYOUT.copy()
    
# Create a global instance
numpad_config = NumpadConfig()