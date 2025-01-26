class AppStyles:
    """Centralized style configurations"""
    WINDOW_MAIN = """
        QMainWindow {
            background-color: white;
        }
    """
    
    LABEL_HEADING = """
        QLabel {
            font-size: 24px;
            color: #2c3e50;
            padding: 5px;
        }
    """

    LOGO_CONTAINER = """
        QLabel {
            qproperty-alignment: AlignCenter;
            padding: 5px;
        }
    """
class AuthStyles:
    CONTAINER = """
        QFrame {
            background: white;
            border: 1px solid #ddd;
            border-radius: 10px;
        }
    """
    
    LOGO_CONTAINER = """
        QLabel {
            qproperty-alignment: AlignCenter;
            padding: 5px;
        }
    """
    
    LABEL_TEXT = """
        QLabel {
            font-size: 18px;
            color: #333;
            padding: 10px;
            background: transparent;
        }
    """

    LABEL_TEXT_INVALID = """
        QLabel {
            font-size: 18px;
            color: red;
            font-weight: bold;
            background: white;
        }
    """

    DIGIT_BOX_EMPTY = """
        QLabel {
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
    """

    DIGIT_BOX_FILLED = """
        QLabel {
            border: 2px solid #3498db;
            background-color: #f8f8f8;
            font-size: 16px;
        }
    """

    KEYPAD_BUTTON = """
        QPushButton {
            font-size: 18px;
            min-width: 50px;
            min-height: 40px;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #f8f8f8;
        }
    """

    NEXT_BUTTON_ACTIVE = """
        QPushButton {
            background-color: #3498db;  /* Blue */
            color: white;
            font-size: 18px;
            min-width: 50px;
            min-height: 40px;
            border-radius: 5px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #2980b9;  /* Darker blue on hover */
        }
    """