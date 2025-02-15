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
    HorizontalButtonType
)

class ButtonStyles:
    """Centralized button style generators"""
    screen_config = None  # Will be set during initialization
    
    @classmethod
    def init_screen_config(cls, config):
        """Initialize screen configuration"""
        cls.screen_config = config
    
    @classmethod
    def get_payment_button_style(cls, button_type):
        """Generate payment button style based on configuration"""
        if not cls.screen_config:
            return ""
            
        config = PaymentButtonConfig.get_config(PaymentButtonType(button_type))
        if not config:
            return ""
            
        sizes = cls.screen_config.get_size('payment_button')
        
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

    @classmethod
    def get_transaction_button_style(cls, button_type):
        """Generate transaction button style based on configuration"""
        if not cls.screen_config:
            return ""
            
        config = TransactionButtonConfig.get_config(TransactionButtonType(button_type))
        if not config:
            return ""
            
        sizes = cls.screen_config.get_size('transaction_button')
        
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

    @classmethod
    def get_horizontal_button_style(cls, button_type):
        """Generate horizontal button style based on configuration"""
        if not cls.screen_config:
            return ""
            
        config = HorizontalButtonConfig.get_config(HorizontalButtonType(button_type))
        if not config:
            return ""
            
        sizes = cls.screen_config.get_size('horizontal_button')
        
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

    @classmethod
    def get_order_button_style(cls):
        """Generate order type button style"""
        if not cls.screen_config:
            return ""
            
        sizes = cls.screen_config.get_size('order_type_button')
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

    @classmethod
    def get_category_button_style(cls, is_selected=False):
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

    @classmethod
    def get_product_button_style(cls):
        """Generate product button style"""
        if not cls.screen_config:
            return ""
            
        config = ProductButtonConfig.DEFAULTS
        return f"""
            QPushButton {{
                background: {config['background']};
                border: 1px solid {config['border_color']};
                border-radius: {cls.screen_config.get_size('button_border_radius')}px;
                padding: {cls.screen_config.get_size('button_padding')}px;
                color: {config['text_color']};
                font-weight: {config['font_weight']};
                font-size: 14px;
                width: {cls.screen_config.get_size('pos_product_button_width')}px;
                height: {cls.screen_config.get_size('pos_product_button_height')}px;
            }}
            QPushButton:hover {{
                background: {config['background_hover']};
                border-color: {config['border_color_hover']};
            }}
            QPushButton:pressed {{
                background: {config['background_pressed']};
            }}
        """