from config.style_constants import Colors, FontSizes, Spacing, BorderRadius

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
            border-radius: 15px;
            padding: {}px;
        }}
    """
    
    LABEL_TEXT = """
        QLabel {{
            color: #333;
            background: transparent;
            border-radius: 15px;
            padding: {}px;
            font-size: {}px;
        }}
    """

    LABEL_TEXT_INVALID = """
        QLabel {{
            color: red;
            background: white;
            border-radius: 15px;
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
            border-radius: 15px;
            padding: {}px;
            font-size: {}px;
        }}
    """

    KEYPAD_BUTTON = """
        QPushButton {{
            font-size: {}px;
            border: 1px solid #ddd;
            border-radius: 15px;
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
            border-radius: 15px;
            font-size: {}px;
            padding: {}px;
        }}
        QPushButton:hover {{
            background-color: #2980b9;
        }}
    """

class POSStyles:
    """POS view specific styles"""
    
    TOP_BAR = """
        QFrame {
            background: #F0F0F0;
            border-bottom: 1px solid #DEDEDE;
        }
    """
    
    SEARCH_INPUT = """
        QLineEdit {
            border: 1px solid #DEDEDE;
            border-radius: 20px;
            padding: 8px 40px;
            font-size: 14px;
            color: #333;
            background: white;
        }
        QLineEdit:focus {
            border-color: #2196F3;
            outline: none;
        }
    """
    
    HORIZONTAL_CATEGORY_BUTTON = """
        QPushButton {
            background: white;
            border: 1px solid #DEDEDE;
            border-radius: 4px;
            padding: 4px;
            color: #333;
            text-align: center;
            font-size: 13px;
        }
        QPushButton:hover {
            background: #F8F9FA;
            border-color: #2196F3;
        }
    """
    
    HORIZONTAL_CATEGORY_BUTTON_SELECTED = """
        QPushButton {
            background: #2196F3;
            border: none;
            border-radius: 4px;
            padding: 4px;
            color: white;
            text-align: center;
            font-size: 13px;
            font-weight: 500;
        }
        QPushButton:hover {
            background: #1E88E5;
        }
    """
    
    ORDER_PANEL = """
        QFrame {
            background: white;
            border-right: 1px solid #DEDEDE;
        }
    """
    
    ORDER_HEADER = """
        QFrame {
            background: #F8F9FA;
            border: none;
        }
        QLabel {
            color: #2196F3;
            font-size: 16px;
            font-weight: 500;
        }
    """
    
    ORDER_ITEM = """
        QFrame {
            background: white;
            border-bottom: 1px solid #EEEEEE;
            padding: 2px;
        }
    """
    
    ORDER_ITEM_SELECTED = """
        QFrame {
            background: #E3F2FD;
            border: 1px solid #2196F3;
            border-radius: 4px;
        }
    """
    
    QUANTITY_SUMMARY = """
        QFrame {
            background: white;
            border-top: 1px solid #DEDEDE;
        }
        QLabel {
            color: #666;
            font-size: 13px;
        }
    """
    
    PRODUCT_BUTTON = """
        QPushButton {
            background: white;
            border: 1px solid #DEDEDE;
            border-radius: 16px;
            padding: 8px;
            color: #333;
            font-size: 14px;
        }
        QPushButton:hover {
            background: #F8F9FA;
            border-color: #2196F3;
        }
        QPushButton:pressed {
            background: #F1F1F1;
        }
    """
    
    ACTION_BUTTON = """
        QPushButton {
            background-color: {bg_color};
            color: {text_color};
            border: none;
            border-radius: 10px;
            padding: 5px;
            margin: 3px;
            font-size: 13px;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: {hover_color};
        }
    """
    
    BOTTOM_BAR = """
        QFrame {{
            background: #F8F9FA;
            border-top: 1px solid #DEDEDE;
            min-height: {height}px;
            max-height: {height}px;
            margin-bottom: 10px;
        }}
    """
    
    PAY_BUTTON = """
        QPushButton {{
            background-color: {bg_color};
            color: {text_color};
            border: none;
            border-radius: {border_radius}px;
            padding: {padding}px;
            font-size: {font_size}px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
    """

    ORDER_TYPE_BUTTON = """
        QPushButton {
            background: white;
            border: 1px solid #DEDEDE;
            border-radius: 4px;
            padding: 8px 16px;
            color: #333;
            font-size: 13px;
            height: 36px;
            min-width: 100px;
        }
        QPushButton:hover {
            background: #F8F9FA;
            border-color: #2196F3;
        }
        QPushButton:checked {
            background: #2196F3;
            border-color: #2196F3;
            color: white;
        }
    """
    
    TOTALS_FRAME = """
        QFrame {
            background: #F8F9FA;
            border-top: 1px solid #DEDEDE;
        }
        QLabel {
            color: #333;
        }
        .currency-usd {
            font-size: 24px;
            font-weight: bold;
            color: #03991f;
        }
        .currency-lbp {
            font-size: 20px;
            color: #666;
        }
    """

    # Scroll Area Styles
    SCROLL_AREA = """
        QScrollArea {
            border: none;
            background: transparent;
        }
        QScrollBar:vertical {
            border: none;
            background: #F8F9FA;
            width: 8px;
            margin: 0;
        }
        QScrollBar::handle:vertical {
            background: #DEDEDE;
            border-radius: 4px;
            min-height: 20px;
        }
        QScrollBar::add-line:vertical, 
        QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
    """
    
    # Menu Styles
    MENU = """
        QMenu {
            background-color: white;
            border: 1px solid #DEDEDE;
            border-radius: 4px;
            padding: 5px;
        }
        QMenu::item {
            padding: 8px 20px;
            border-radius: 4px;
            color: #333;
        }
        QMenu::item:selected {
            background-color: #F0F0F0;
            color: #2196F3;
        }
        QMenu::separator {
            height: 1px;
            background: #DEDEDE;
            margin: 5px 0px;
        }
    """
    
    # Lock Button Style
    LOCK_BUTTON = """
        QPushButton {
            background: transparent;
            border: none;
            padding: 0px;
        }
    """
    
    # Order List Item Styles
    ORDER_LIST_WIDGET = """
        QWidget {
            background: white;
        }
        QLabel {
            padding: 5px;
        }
    """
    
    # Splitter Style
    SPLITTER = """
        QSplitter::handle {
            background: #DEDEDE;
            width: 1px;
        }
    """
    
    # Employee Zone Styles
    EMPLOYEE_ZONE = """
        QFrame {
            background: transparent;
            border: none;
        }
    """
    
    EMPLOYEE_ID = """
        QLabel {
            color: #333;
            font-weight: 500;
        }
    """
    
    DATE_TIME_ZONE = """
        QFrame {
            background: transparent;
            border: none;
        }
    """
    
    DATE_LABEL = """
        QLabel {
            color: #666;
        }
    """
    
    TIME_LABEL = """
        QLabel {
            color: #333;
            font-weight: 500;
            padding-left: 4px;
        }
    """
    
    # Already existing styles...
    SEARCH_INPUT = """
        QLineEdit {
            border: 1px solid #DEDEDE;
            border-radius: 20px;
            padding: 8px 40px;
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

    @staticmethod
    def get_pay_button_style(button_type="default"):
        """Get the appropriate style for a payment button"""
        if button_type == "cash":
            return POSStyles.PAY_BUTTON.format(
                bg_color=Colors.SUCCESS,
                hover_color=Colors.SUCCESS_HOVER,
                text_color=Colors.TEXT_LIGHT,
                border_radius=BorderRadius.MEDIUM,
                padding=Spacing.MEDIUM,
                font_size=FontSizes.XXLARGE
            )
        elif button_type == "other":
            return POSStyles.PAY_BUTTON.format(
                bg_color=Colors.WARNING,
                hover_color=Colors.WARNING_HOVER,
                text_color=Colors.TEXT_LIGHT,
                border_radius=BorderRadius.MEDIUM,
                padding=Spacing.MEDIUM,
                font_size=FontSizes.XLARGE
            )
        
    def get_action_button_style(button_type, colors):
        """Get style for action buttons with dynamic colors"""
        return f"""
            QPushButton {{
                background-color: {colors['bg']};
                color: {colors['text']};
                border: none;
                border-radius: 10px;
                padding: 5px;
                margin: 3px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {colors['hover']};
            }}
        """