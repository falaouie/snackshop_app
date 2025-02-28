"""Numpad styling and configuration"""
from config.layouts.numpad_layout import numpad_layout_config

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
        font_size = config.get_size('font_size')
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
        font_size = config.get_size('font_size')
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