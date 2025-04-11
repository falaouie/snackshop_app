# styles/auth_top_bar_styles.py
"""
Styles for the TopBar component

This module follows a clean separation of concerns where:
1. Stylesheets handle only visual appearance (colors, borders)
2. Widget methods handle sizing and font properties
3. Config values are used directly by the widget, not in the stylesheet

This approach follows Qt best practices:
- Stylesheets for colors and visual styling
- Qt methods (setFixedHeight, QFont) for dimensions and text properties
"""
class AuthStyles:
    """Styles for top bar and related components"""
    
    @staticmethod
    def get_auth_top_bar_container_style():
        """Get the main container style"""
        return """
            QFrame {
                background: white;
            }
        """
    
    @staticmethod
    def get_exit_button_style():
        """Get exit button style"""
        return """
            QPushButton {
                background: transparent;
                border: none;
            }
        """
    
    @staticmethod
    def get_logo_label_style():
        """Get logo label style"""
        return """
            QLabel {
                background: transparent;
                border: none;
            }
        """
    
    """Authentication view styles"""

    @staticmethod
    def get_auth_container_style():
        return f"""
            QFrame {{
                background: white;
                border: 1px solid #ddd;
            }}
        """
    
    # @staticmethod
    # def LABEL_TEXT(padding, font_size):
    #     return f"""
    #         QLabel {{
    #             color: #333;
    #             background: transparent;
    #             border-radius: 15px;
    #             padding: {padding}px;
    #             font-size: {font_size}px;
    #         }}
    #     """
    
    @staticmethod
    def get_auth_label_text_style():
        return f"""
            QLabel {{
                color: #333;
                background: transparent;
                border-radius: 15px;
            }}
        """

    # @staticmethod
    # def LABEL_TEXT_INVALID(padding, font_size):
    #     return f"""
    #         QLabel {{
    #             color: red;
    #             background: white;
    #             border-radius: 15px;
    #             padding: {padding}px;
    #             font-size: {font_size}px;
    #         }}
    #     """
    
    @staticmethod
    def get_auth_label_invalid_style():
        return f"""
            QLabel {{
                color: red;
                background: white;
                border-radius: 15px;
            }}
        """

    @staticmethod
    def DIGIT_BOX_EMPTY(padding, font_size):
        return f"""
            QLabel {{
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: {padding}px;
                font-size: {font_size}px;
            }}
        """

    @staticmethod
    def DIGIT_BOX_FILLED(padding, font_size):
        return f"""
            QLabel {{
                border: 2px solid #3498db;
                background-color: #f8f8f8;
                border-radius: 15px;
                padding: {padding}px;
                font-size: {font_size}px;
            }}
        """

    @staticmethod
    def KEYPAD_BUTTON(font_size, padding):
        return f"""
            QPushButton {{
                font-size: {font_size}px;
                border: 1px solid #ddd;
                border-radius: 15px;
                padding: {padding}px;
            }}
            QPushButton:hover {{
                background-color: #f8f8f8;
            }}
        """
    
    @staticmethod
    def get_keypad_button_style():
        return f"""
            QPushButton {{
                border: 1px solid #ddd;
            }}
            QPushButton:hover {{
                background-color: #f8f8f8;
            }}
        """
    
    @staticmethod
    def get_next_btn_active_style():
        return f"""
            QPushButton {{
                background-color: #3498db;
                color: white;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
        """