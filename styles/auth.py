class AuthStyles:
    """Authentication view styles"""
    
    @staticmethod
    def CONTAINER(margin):
        return f"""
            QFrame {{
                background: white;
                border: 1px solid #ddd;
                border-radius: 15px;
                padding: {margin}px;
            }}
        """
    
    @staticmethod
    def LABEL_TEXT(padding, font_size):
        return f"""
            QLabel {{
                color: #333;
                background: transparent;
                border-radius: 15px;
                padding: {padding}px;
                font-size: {font_size}px;
            }}
        """

    @staticmethod
    def LABEL_TEXT_INVALID(padding, font_size):
        return f"""
            QLabel {{
                color: red;
                background: white;
                border-radius: 15px;
                padding: {padding}px;
                font-size: {font_size}px;
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
    def NEXT_BUTTON_ACTIVE(font_size, padding):
        return f"""
            QPushButton {{
                background-color: #3498db;
                color: white;
                border-radius: 15px;
                font-size: {font_size}px;
                padding: {padding}px;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
        """