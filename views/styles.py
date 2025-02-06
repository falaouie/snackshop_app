class AppStyles:
    """Centralized style configurations"""
    WINDOW_MAIN = """
        QMainWindow {
            background-color: #F8F9FA;
        }
    """

    LOGO_CONTAINER = """
        QLabel {
            qproperty-alignment: AlignCenter;
        }
    """
class AuthStyles:
    CONTAINER = """
        QFrame {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: {}px;
        }}
    """
    
    LABEL_TEXT = """
        QLabel {{
            color: #333;
            background: transparent;
            padding: {}px;
            font-size: {}px;
        }}
    """

    LABEL_TEXT_INVALID = """
        QLabel {{
            color: red;
            background: white;
            padding: {}px;
            font-size: {}px;
        }}
    """

    DIGIT_BOX_EMPTY = """
        QLabel {{
            border: 2px solid #ddd;
            border-radius: 5px;
            padding: {}px;
            font-size: {}px;
        }}
    """

    DIGIT_BOX_FILLED = """
        QLabel {{
            border: 2px solid #3498db;
            background-color: #f8f8f8;
            padding: {}px;
            font-size: {}px;
        }}
    """

    KEYPAD_BUTTON = """
        QPushButton {{
            font-size: {}px;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: {}px;
        }}
        QPushButton:hover {{
            background-color: #f8f8f8;
        }}
    """

    NEXT_BUTTON_ACTIVE = """
        QPushButton {{
            background-color: #3498db;
            color: white;
            border-radius: 5px;
            font-size: {}px;
            padding: {}px;
        }}
        QPushButton:hover {{
            background-color: #2980b9;
        }}
    """

class POSStyles:
    TOP_BAR = """
        QFrame {
            background-color: #BCBBBA;
        }
    """
    
    TOP_BAR_TEXT = """
        QLabel {
            color: black;
        }
    """
    
    TOP_BAR_BUTTON = """
        QPushButton {{
            background-color: #34495e;
            color: white;
            font-size: {}px;
            border: none;
            border-radius: 4px;
            padding: {}px;
        }}
        QPushButton:hover {{
            background-color: #435c78;
        }}
    """

    SIGN_OUT_BUTTON = """
        QPushButton {{
            background-color: red;
            color: white;
            font-size: {}px;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: {}px;
        }}
        QPushButton:hover {{
            background-color: #f8f8f8;
        }}
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
            color: #2c3e50;
            padding: 2px;
            font-weight: bold;
            font-size: 16px;
        }
    """
    
    CATEGORY_BUTTON = """
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
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
            background-color: #F8F9FA;
            border-top: 1px solid #34495e;
        }
    """
    
    BOTTOM_BAR_BUTTON = """
        QPushButton {
            border: none;
            border-radius: 16px;
            padding: 2px;
            font-weight: bold;
            font-size: 14px;
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
        }
        QPushButton:hover {
            background-color: #219a52;
        }
    """

    SUMMARY_PANEL = """
        QFrame {
            background-color: white;
            border-top: 1px solid #dcdde1;
        }
        QLabel {
            color: #2c3e50;
        }
    """
    
    PRODUCT_BUTTON = """
        QPushButton {
            background-color: white;
            border: 1px solid #dcdde1;
            border-radius: 10px;
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
            border-radius: 10px;
        }
    """
    
    BACK_BUTTON = """
        QPushButton {
            background-color: black;
            color: white;
            border: 1px solid #dcdde1;
            border-radius: 10px;
            text-align: center;
        }
    """

    HEADER_FRAME = """
        QFrame {
            background-color: #f5f6fa;
            border-bottom: 1px solid #dcdde1;
        }
    """

    CATEGORY_BUTTON_SELECTED = """
    QPushButton {
        background-color: #2980b9;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #3498db;
    }
"""