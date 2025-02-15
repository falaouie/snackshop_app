from config.screen_config import screen_config
from button_definitions import (
    PaymentButtonConfig,
    TransactionButtonConfig,
    HorizontalButtonConfig,
    OrderButtonConfig,
    CategoryButtonConfig,
    ProductButtonConfig
)
from button_definitions.types import (
    PaymentButtonType,
    TransactionButtonType,
    HorizontalButtonType,
    OrderButtonType,
    CategoryButtonType,
    ProductButtonType
)

class ButtonStyles:
    """Centralized button style generators"""
    
    @staticmethod
    def get_payment_button_style(button_type):
        """Generate payment button style based on configuration"""
        config = PaymentButtonConfig.get_config(PaymentButtonType(button_type))
        if not config:
            return ""
            
        sizes = screen_config.get_size('payment_button')
        
        return f"""
            QPushButton {{
                background-color: {config['colors']['primary']};
                color: {config['colors']['text']};
                border: none;
                border-radius: {sizes['border_radius']}px;
                padding: {sizes['padding']}px;
                font-size: {sizes['font_size']}px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {config['colors']['hover']};
            }}
            QPushButton:pressed {{
                background-color: {config['colors']['primary']};
            }}
        """

    @staticmethod
    def get_transaction_button_style(button_type):
        """Generate transaction button style based on configuration"""
        config = TransactionButtonConfig.get_config(TransactionButtonType(button_type))
        if not config:
            return ""
            
        sizes = screen_config.get_size('transaction_button')
        
        return f"""
            QPushButton {{
                background-color: {config['colors']['primary']};
                color: {config['colors']['text']};
                border: none;
                border-radius: {sizes['border_radius']}px;
                padding: {sizes['padding']}px;
                font-size: {sizes['font_size']}px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {config['colors']['hover']};
            }}
        """

    @staticmethod
    def get_horizontal_button_style(button_type):
        """Generate horizontal button style based on configuration"""
        config = HorizontalButtonConfig.get_config(HorizontalButtonType(button_type))
        if not config:
            return ""
            
        sizes = screen_config.get_size('horizontal_button')
        
        return f"""
            QPushButton {{
                background-color: {config['colors']['primary']};
                color: {config['colors']['text']};
                border: none;
                border-radius: {sizes['border_radius']}px;
                padding: {sizes['padding']}px;
                font-size: {sizes['font_size']}px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {config['colors']['hover']};
            }}
        """

    @staticmethod
    def get_order_button_style():
        """Generate order type button style"""
        sizes = screen_config.get_size('order_type_button')
        config = OrderButtonConfig.DEFAULTS
        
        return f"""
            QPushButton {{
                background: {config['background']};
                border: 1px solid {config['border_color']};
                border-radius: {sizes['border_radius']}px;
                padding: {sizes['padding']}px;
                color: {config['text_color']};
                font-size: {sizes['font_size']}px;
                height: {sizes['height']}px;
                min-width: {sizes['min_width']}px;
            }}
            QPushButton:hover {{
                background: {config['background_hover']};
                border-color: {config['border_color_selected']};
            }}
            QPushButton:checked {{
                background: {config['background_selected']};
                border-color: {config['border_color_selected']};
                color: {config['text_color_selected']};
            }}
        """

    @staticmethod
    def get_category_button_style(is_selected=False):
        """Generate category button style"""
        config = CategoryButtonConfig.DEFAULTS
        
        if is_selected:
            return f"""
                QPushButton {{
                    background: {config['selected_background']};
                    border: none;
                    border-radius: 4px;
                    padding: 5px;
                    color: {config['selected_text_color']};
                    font-size: 13px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background: {config['selected_hover_background']};
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background: {config['background']};
                    border: 1px solid {config['border_color']};
                    border-radius: 4px;
                    padding: 5px;
                    color: {config['text_color']};
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    background: {config['hover_background']};
                    border-color: {config['hover_border_color']};
                }}
            """

    @staticmethod
    def get_product_button_style():
        """Generate product button style"""
        config = ProductButtonConfig.DEFAULTS
        return f"""
            QPushButton {{
                background: {config['background']};
                border: 1px solid {config['border_color']};
                border-radius: {screen_config.get_size('button_border_radius')}px;
                padding: {screen_config.get_size('button_padding')}px;
                color: {config['text_color']};
                font-weight: {config['font_weight']};
                font-size: 14px;
                width: {screen_config.get_size('pos_product_button_width')}px;
                height: {screen_config.get_size('pos_product_button_height')}px;
            }}
            QPushButton:hover {{
                background: {config['background_hover']};
                border-color: {config['border_color_hover']};
            }}
            QPushButton:pressed {{
                background: {config['background_pressed']};
            }}
        """

# Rest of the styles.py file (POSStyles, AppStyles, AuthStyles) remains unchanged