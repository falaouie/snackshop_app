from config.screen_config import screen_config
from models.button_definitions import (
    PAYMENT_BUTTONS,
    TRANSACTION_BUTTONS,
    HORIZONTAL_BUTTONS,
    ORDER_TYPES
)

class ButtonStyles:
    """Centralized button style generators"""
    
    @staticmethod
    def get_payment_button_style(button_type):
        """Generate payment button style based on configuration"""
        if button_type.upper() not in PAYMENT_BUTTONS:
            return ""
            
        button_config = PAYMENT_BUTTONS[button_type.upper()]
        sizes = screen_config.get_size('payment_button')
        
        return f"""
            QPushButton {{
                background-color: {button_config['colors']['primary']};
                color: {button_config['colors']['text']};
                border: none;
                border-radius: {sizes['border_radius']}px;
                padding: {sizes['padding']}px;
                font-size: {sizes['font_size']}px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {button_config['colors']['hover']};
            }}
            QPushButton:pressed {{
                background-color: {button_config['colors']['primary']};
            }}
        """

    @staticmethod
    def get_transaction_button_style(button_type):
        """Generate transaction button style based on configuration"""
        if button_type.upper() not in TRANSACTION_BUTTONS:
            return ""
            
        button_config = TRANSACTION_BUTTONS[button_type.upper()]
        sizes = screen_config.get_size('transaction_button')
        
        return f"""
            QPushButton {{
                background-color: {button_config['colors']['primary']};
                color: {button_config['colors']['text']};
                border: none;
                border-radius: {sizes['border_radius']}px;
                padding: {sizes['padding']}px;
                font-size: {sizes['font_size']}px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {button_config['colors']['hover']};
            }}
        """

    @staticmethod
    def get_horizontal_button_style(button_type):
        """Generate horizontal button style based on configuration"""
        if button_type.upper() not in HORIZONTAL_BUTTONS:
            return ""
            
        button_config = HORIZONTAL_BUTTONS[button_type.upper()]
        sizes = screen_config.get_size('horizontal_button')
        
        return f"""
            QPushButton {{
                background-color: {button_config['colors']['primary']};
                color: {button_config['colors']['text']};
                border: none;
                border-radius: {sizes['border_radius']}px;
                padding: {sizes['padding']}px;
                font-size: {sizes['font_size']}px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {button_config['colors']['hover']};
            }}
        """

    @staticmethod
    def get_order_type_button_style():
        """Generate order type button style"""
        sizes = screen_config.get_size('order_type_button')
        
        return f"""
            QPushButton {{
                background: white;
                border: 1px solid #DEDEDE;
                border-radius: {sizes['border_radius']}px;
                padding: {sizes['padding']}px;
                color: #333;
                font-size: {sizes['font_size']}px;
                height: {sizes['height']}px;
                min-width: {sizes['min_width']}px;
            }}
            QPushButton:hover {{
                background: #F8F9FA;
                border-color: #2196F3;
            }}
            QPushButton:checked {{
                background: #2196F3;
                border-color: #2196F3;
                color: white;
            }}
        """

class POSStyles:
    """POS view specific styles"""
    
    # Delegate button styles to ButtonStyles class
    get_payment_button_style = ButtonStyles.get_payment_button_style
    get_transaction_button_style = ButtonStyles.get_transaction_button_style
    get_horizontal_button_style = ButtonStyles.get_horizontal_button_style
    get_order_type_button_style = ButtonStyles.get_order_type_button_style
    
    # Top bar styles
    @staticmethod
    def TOP_BAR(height):
        return """
            QFrame {
                background: #F0F0F0;
                border-bottom: 1px solid #DEDEDE;
                height: %dpx;
            }
        """ % height
    
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
    @staticmethod
    def SEARCH_INPUT(width, height):
        return """
            QLineEdit {
                border: 1px solid #DEDEDE;
                border-radius: 20px;
                padding: 8px 40px;
                font-size: 14px;
                color: #333;
                background: white;
                width: %dpx;
                height: %dpx;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                outline: none;
            }
        """ % (width, height)
    
    # Category button styles
    @staticmethod
    def HORIZONTAL_CATEGORY_BUTTON(border_radius, padding, width, height):
        return """
            QPushButton {
                background: white;
                border: 1px solid #DEDEDE;
                border-radius: %dpx;
                padding: %dpx;
                color: #333;
                font-size: 13px;
                width: %dpx;
                height: %dpx;
            }
            QPushButton:hover {
                background: #F8F9FA;
                border-color: #2196F3;
            }
        """ % (border_radius, padding, width, height)
    
    def HORIZONTAL_CATEGORY_BUTTON_SELECTED(border_radius, padding, width, height):
        return """
            QPushButton {
                background: #2196F3;
                border: none;
                border-radius: %dpx;
                padding: %dpx;
                color: white;
                font-size: 13px;
                font-weight: 500;
                width: %dpx;
                height: %dpx;
            }
            QPushButton:hover {
                background: #1E88E5;
            }
        """ % (border_radius, padding, width, height)
    
    # Order panel styles
    def ORDER_PANEL(width):
        return """
            QFrame {
                background: white;
                border-right: 1px solid #DEDEDE;
                width: %dpx;
            }
        """ % width
    
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

    # Order list widget styles
    ORDER_LIST_WIDGET = """
        QWidget {
            background: white;
        }
        QFrame {
            background: white;
            border: none;
        }
    """

    # Splitter styles
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
    PRODUCT_BUTTON = f"""
        QPushButton {{
            background: white;
            border: 1px solid #DEDEDE;
            border-radius: {screen_config.get_size('button_border_radius')}px;
            padding: {screen_config.get_size('button_padding')}px;
            color: #333;
            font-size: 14px;
            width: {screen_config.get_size('pos_product_button_width')}px;
            height: {screen_config.get_size('pos_product_button_height')}px;
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
    @staticmethod
    def BOTTOM_BAR(height):
        return """
            QFrame {
                background: #F8F9FA;
                border-top: 1px solid #DEDEDE;
                height: %dpx;
                margin-bottom: 10px;
            }
        """ % height
    
    # Scroll area styles
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
    
    # Menu styles
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
    
    # Lock button styles
    LOCK_BUTTON = """
        QPushButton {
            background: transparent;
            border: none;
            padding: 0px;
        }
    """
    
    # Totals frame styles
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

class AppStyles:
    """Application-wide styles"""
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
    """Authentication view styles"""
    
    @staticmethod
    def CONTAINER(margin):
        return """
            QFrame {
                background: white;
                border: 1px solid #ddd;
                border-radius: 15px;
                padding: %dpx;
            }
        """ % margin
    
    @staticmethod
    def LABEL_TEXT(padding, font_size):
        return """
            QLabel {
                color: #333;
                background: transparent;
                border-radius: 15px;
                padding: %dpx;
                font-size: %dpx;
            }
        """ % (padding, font_size)

    @staticmethod
    def LABEL_TEXT_INVALID(padding, font_size):
        return """
            QLabel {
                color: red;
                background: white;
                border-radius: 15px;
                padding: %dpx;
                font-size: %dpx;
            }
        """ % (padding, font_size)

    @staticmethod
    def DIGIT_BOX_EMPTY(padding, font_size):
        return """
            QLabel {
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: %dpx;
                font-size: %dpx;
            }
        """ % (padding, font_size)

    @staticmethod
    def DIGIT_BOX_FILLED(padding, font_size):
        return """
            QLabel {
                border: 2px solid #3498db;
                background-color: #f8f8f8;
                border-radius: 15px;
                padding: %dpx;
                font-size: %dpx;
            }
        """ % (padding, font_size)

    @staticmethod
    def KEYPAD_BUTTON(font_size, padding):
        return """
            QPushButton {
                font-size: %dpx;
                border: 1px solid #ddd;
                border-radius: 15px;
                padding: %dpx;
            }
            QPushButton:hover {
                background-color: #f8f8f8;
            }
        """ % (font_size, padding)

    @staticmethod
    def NEXT_BUTTON_ACTIVE(font_size, padding):
        return """
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 15px;
                font-size: %dpx;
                padding: %dpx;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """ % (font_size, padding)