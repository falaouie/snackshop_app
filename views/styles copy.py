class AppStyles:
    """Centralized style configurations"""
    WINDOW_MAIN = """
        QMainWindow {
            background-color: #f0f0f0;
        }
    """
    
    LABEL_HEADING = """
        QLabel {
            font-size: 24px;
            color: #2c3e50;
            padding: 5px;
        }
    """
    
    CONTAINER = """
        QWidget {
            background: white;
            border-radius: 8px;
            padding: 5px;
        }
    """
class AuthStyles:
    CONTAINER = """
        QFrame {
            background: white;
            border-radius: 10px;
            border: 1px solid #ddd;
            padding: 5px;
        }
    """
    
    LOGO_CONTAINER = """
        QLabel {
            qproperty-alignment: AlignCenter;
            padding: 5px;
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