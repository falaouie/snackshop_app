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
                width: {sizes['width']}px;
                height: {sizes['height']}px;
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
                width: {sizes['width']}px;
                height: {sizes['height']}px;
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
                width: {sizes['width']}px;
                height: {sizes['height']}px;
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
    
    # Other POS styles remain the same but use screen_config for sizes
    TOP_BAR = """
        QFrame {
            background: #F0F0F0;
            border-bottom: 1px solid #DEDEDE;
        }
    """
    
    SEARCH_INPUT = f"""
        QLineEdit {{
            border: 1px solid #DEDEDE;
            border-radius: 20px;
            padding: 8px 40px;
            font-size: 14px;
            color: #333;
            background: white;
            width: {screen_config.get_size('pos_search_input_width')}px;
            height: {screen_config.get_size('pos_search_input_height')}px;
        }}
        QLineEdit:focus {{
            border-color: #2196F3;
            outline: none;
        }}
    """
    
    ORDER_PANEL = f"""
        QFrame {{
            background: white;
            border-right: 1px solid #DEDEDE;
            width: {screen_config.get_size('pos_order_panel_width')}px;
        }}
    """
    
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
    
    BOTTOM_BAR = f"""
        QFrame {{
            background: #F8F9FA;
            border-top: 1px solid #DEDEDE;
            height: {screen_config.get_size('pos_bottom_bar_height')}px;
            margin-bottom: 10px;
        }}
    """

    # Keep other existing styles...
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
    # Auth styles remain unchanged...
    pass