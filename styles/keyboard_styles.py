"""Styles for keyboard components and keyboard-enabled inputs"""
from config.layouts.keyboard_layout import keyboard_layout_config

class KeyboardStyles:
    # Base keyboard container styles
    KEYBOARD_BASE = """
        QWidget {
            background-color: #F5F5F5;
            border: 1px solid #CCCCCC;
            border-radius: 8px;
        }
    """
    
    HANDLE_BAR = """
        QFrame {
            background-color: #E0E0E0;
            border-bottom: 1px solid #CCCCCC;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }
    """
    
    # Standard input style that can be applied directly
    INPUT_BASE = """
        QLineEdit {
            background-color: white;
            border: 1px solid #DEDEDE;
            border-radius: 4px;
            padding: 8px;
            font-size: 14px;
            color: #333333;
        }
        QLineEdit:focus {
            border: 1px solid #2196F3;
        }
    """
    
    @staticmethod
    def get_key_style():
        """Get styling for standard keyboard keys"""
        config = keyboard_layout_config.get_styling()
        return f"""
            QPushButton {{
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                font-size: {config['font_size']}px;
                padding: {config['padding']}px;
            }}
            QPushButton:hover {{
                background-color: #F0F0F0;
                border-color: #2196F3;
            }}
            QPushButton:pressed {{
                background-color: #E0E0E0;
            }}
        """
    
    @staticmethod
    def get_space_key_style():
        """Get styling for space bar key"""
        config = keyboard_layout_config.get_styling()
        return f"""
            QPushButton {{
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                font-size: {config['font_size']}px;
                padding: {config['padding']}px;
            }}
            QPushButton:hover {{
                background-color: #F0F0F0;
                border-color: #2196F3;
            }}
            QPushButton:pressed {{
                background-color: #E0E0E0;
            }}
        """
    
    @staticmethod
    def get_enter_key_style():
        """Get styling for enter key"""
        config = keyboard_layout_config.get_styling()
        return f"""
            QPushButton {{
                background-color: #2196F3;
                color: white;
                border: 1px solid #1976D2;
                border-radius: 4px;
                font-size: {config['font_size']}px;
                padding: {config['padding']}px;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
            QPushButton:pressed {{
                background-color: #0D47A1;
            }}
        """
    
    @staticmethod
    def get_control_button_style():
        """Get styling for keyboard control buttons (min/max/close)"""
        return """
            QPushButton {
                background-color: transparent;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
            QPushButton#close_btn:hover {
                background-color: #FF5252;
                color: white;
            }
        """