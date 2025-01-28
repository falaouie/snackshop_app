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

class POSStyles:
    TOP_BAR = """
        QFrame {
            background-color: white;
        }
    """
    
    TOP_BAR_TEXT = """
        QLabel {
            color: black;
            font-size: 14px;
            padding: 5px;
        }
    """
    
    TOP_BAR_BUTTON = """
        QPushButton {
            background-color: #34495e;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #435c78;
        }
    """
    
    ORDER_PANEL = """
        QFrame {
            background-color: #f5f6fa;
            border-right: 1px solid #dcdde1;
        }
    """
    
    PRODUCTS_PANEL = """
        QFrame {
            background-color: white;
        }
    """
    
    SECTION_HEADER = """
        QLabel {
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            padding: 5px 0;
        }
    """
    
    CATEGORY_BUTTON = """
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:checked {
            background-color: #2980b9;
        }
    """
    
    SCROLL_AREA = """
        QScrollArea {
            border: none;
            background: white;
        }
    """
    
    BOTTOM_BAR = """
        QFrame {
            background-color: #2c3e50;
            border-top: 1px solid #34495e;
        }
    """
    
    BOTTOM_BAR_BUTTON = """
        QPushButton {
            background-color: #34495e;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #435c78;
        }
    """
    
    PAYMENT_BUTTON = """
        QPushButton {
            background-color: #27ae60;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #219a52;
        }
    """

    SUMMARY_PANEL = """
        QFrame {
            background-color: white;
            border-top: 1px solid #dcdde1;
            margin-top: 10px;
        }
        QLabel {
            font-size: 16px;
            color: #2c3e50;
        }
    """
    
    PRODUCT_BUTTON = """
        QPushButton {
            background-color: white;
            border: 1px solid #dcdde1;
            border-radius: 4px;
            padding: 10px;
            font-size: 14px;
            text-align: center;
        }
        QPushButton:hover {
            background-color: #f8f9fa;
            border-color: #3498db;
        }
    """

    NUMBERS_PANEL = """
        QFrame {
            background-color: #f5f6fa;
            border-right: 1px solid #dcdde1;
            border-left: 1px solid #dcdde1;
        }
    """
    
    NUMBER_BUTTON = """
        QPushButton {
            background-color: white;
            border: 1px solid #dcdde1;
            border-radius: 4px;
            font-size: 14px;
            color: #2c3e50;
        }
        QPushButton:hover {
            background-color: #f8f9fa;
            border-color: #3498db;
        }
        QPushButton:pressed {
            background-color: #e9ecef;
        }
    """

    PRODUCT_BUTTON_DISABLED = """
        QPushButton {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
        }
    """
    
    BACK_BUTTON = """
        QPushButton {
            background-color: #34495e;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2c3e50;
        }
    """

    HEADER_FRAME = """
        QFrame {
            background-color: #f5f6fa;
            border-bottom: 1px solid #dcdde1;
        }
    """