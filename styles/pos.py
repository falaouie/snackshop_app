from .buttons import ButtonStyles

class POSStyles:
    """POS view specific styles"""
    screen_config = None
    
    @classmethod
    def init_screen_config(cls, config):
        cls.screen_config = config
    
    # Delegate button styles to ButtonStyles class
    get_payment_button_style = ButtonStyles.get_payment_button_style
    get_transaction_button_style = ButtonStyles.get_transaction_button_style
    get_horizontal_button_style = ButtonStyles.get_horizontal_button_style
    get_order_button_style = ButtonStyles.get_order_button_style
    
    # Top bar styles
    @classmethod
    def TOP_BAR(cls, height):
        return f"""
            QFrame {{
                background: #F0F0F0;
                border-bottom: 1px solid #DEDEDE;
                height: {height}px;
            }}
        """
    
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
    
    # Search input styles
    @classmethod
    def SEARCH_INPUT(cls, width, height):
        return f"""
            QLineEdit {{
                border: 1px solid #DEDEDE;
                border-radius: 20px;
                padding: 8px 40px;
                font-size: 14px;
                color: #333;
                background: white;
                width: {width}px;
                height: {height}px;
            }}
            QLineEdit:focus {{
                border-color: #2196F3;
                outline: none;
            }}
        """
    
    # center panel and intermediate container styles
    @classmethod
    def CENTER_PANEL(cls):
        return """
            QFrame {
                background: white;
                border-left: 1px solid #DEDEDE;
                border-right: 1px solid #DEDEDE;
            }
        """

    @classmethod
    def INTERMEDIATE_CONTAINER(cls):
        return """
            QFrame {
                background: white;
                border-top: 1px solid #DEDEDE;
            }
    """
    # Order panel styles
    @classmethod
    def ORDER_PANEL(cls, width):
        return f"""
            QFrame {{
                background: white;
                border-right: 1px solid #DEDEDE;
                width: {width}px;
            }}
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

    ORDER_LIST_WIDGET = """
        QWidget {
            background: white;
        }
        QFrame {
            background: white;
            border: none;
        }
    """

    SPLITTER = """
        QSplitter {
            background: transparent;
        }
        QSplitter::handle {
            background: #DEDEDE;
            width: 1px;
        }
        QSplitter::handle:hover {
            background: #2196F3;
        }
    """

    # Product button styles
    @classmethod
    def get_product_button_style(cls):
        if not cls.screen_config:
            return ""
            
        return f"""
            QPushButton {{
                background: white;
                border: 1px solid #DEDEDE;
                border-radius: {cls.screen_config.get_size('button_border_radius')}px;
                padding: {cls.screen_config.get_size('button_padding')}px;
                color: #333;
                font-size: 14px;
                width: {cls.screen_config.get_size('pos_product_button_width')}px;
                height: {cls.screen_config.get_size('pos_product_button_height')}px;
            }}
            QPushButton:hover {{
                background: #F8F9FA;
                border-color: #2196F3;
            }}
            QPushButton:pressed {{
                background: #F1F1F1;
            }}
        """
    
    # Bottom bar styles
    @classmethod
    def BOTTOM_BAR(cls, height):
        return f"""
            QFrame {{
                background: #F8F9FA;
                border-top: 1px solid #DEDEDE;
                height: {height}px;
                margin-bottom: 10px;
            }}
        """
    
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
    
    LOCK_BUTTON = """
        QPushButton {
            background: transparent;
            border: none;
            padding: 0px;
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