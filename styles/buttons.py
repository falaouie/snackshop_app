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
    # screen_config = None  # Will be set during initialization
    layout_config = None

    # @classmethod
    # def init_screen_config(cls, config):
    #     """Initialize screen configuration"""
    #     cls.screen_config = config

    @classmethod
    def init_layout_config(cls, config):
        """Initialize layout configuration"""
        cls.layout_config = config
    
    @classmethod
    def get_payment_button_style(cls, button_type):
        """Generate payment button style based on configuration"""
        if not cls._check_config():
            return ""
                
        config = PaymentButtonConfig.get_config(PaymentButtonType(button_type))
        if not config:
            return ""
                
        button_config = cls.layout_config.get_button_config('payment')
        
        return f"""
            QPushButton {{
                background-color: {config['colors']['primary']};
                color: {config['colors']['text']};
                border: none;
                border-radius: {button_config['border_radius']}px;
                padding: {button_config['padding']}px;
                font-size: {button_config['font_size']}px;
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
        if not cls._check_config():
            return ""
                
        config = TransactionButtonConfig.get_config(TransactionButtonType(button_type))
        if not config:
            return ""
                
        button_config = cls.layout_config.get_button_config('transaction')
        
        return f"""
            QPushButton {{
                background-color: {config['colors']['primary']};
                color: {config['colors']['text']};
                border: none;
                border-radius: {button_config['border_radius']}px;
                padding: {button_config['padding']}px;
                font-size: {button_config['font_size']}px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {config['colors']['hover']};
            }}
        """

    @classmethod
    def get_horizontal_button_style(cls, button_type):
        """Generate horizontal button style based on configuration"""
        if not cls._check_config():
            return ""
                
        config = HorizontalButtonConfig.get_config(HorizontalButtonType(button_type))
        if not config:
            return ""
                
        button_config = cls.layout_config.get_button_config('horizontal')
        
        return f"""
            QPushButton {{
                background-color: {config['colors']['primary']};
                color: {config['colors']['text']};
                border: none;
                border-radius: {button_config['border_radius']}px;
                padding: {button_config['padding']}px;
                font-size: {button_config['font_size']}px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {config['colors']['hover']};
            }}
        """

    @classmethod
    def get_order_button_style(cls, is_selected=False):
        """Generate order type button style based on selection state"""
        if not cls._check_config():
            return ""
                
        button_config = cls.layout_config.get_button_config('order_type')
        config = OrderButtonConfig.DEFAULTS
        
        if is_selected:
            return f"""
                QPushButton {{
                    background: {config['selected_background']};
                    border: none;
                    border-radius: {button_config['border_radius']}px;
                    padding: {button_config['padding']}px;
                    color: {config['selected_text_color']};
                    font-size: {button_config['font_size']}px;
                    font-weight: 500;
                    min-width: {button_config['width']}px;
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
                    border-radius: {button_config['border_radius']}px;
                    padding: {button_config['padding']}px;
                    color: {config['text_color']};
                    font-size: {button_config['font_size']}px;
                    min-width: {button_config['width']}px;
                }}
                QPushButton:hover {{
                    background: {config['hover_background']};
                    border-color: {config['hover_border_color']};
                }}
            """

    @classmethod
    def get_category_button_style(cls, is_selected=False):
        """Generate category button style without size properties"""
        if not cls._check_config():
            return ""
        
        config = CategoryButtonConfig.DEFAULTS
        grid_config = cls.layout_config.get_product_grid_config()
        
        if is_selected:
            return f"""
                QPushButton {{
                    background: {config['selected_background']};
                    border: none;
                    border-radius: {grid_config['category_button']['radius']}px;
                    padding: {grid_config['category_button']['padding']}px;
                    color: {config['selected_text_color']};
                    font-size: {grid_config['category_button']['font_size']}px;
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
                    border-radius: {grid_config['category_button']['radius']}px;
                    padding: {grid_config['category_button']['padding']}px;
                    color: {config['text_color']};
                    font-size: {grid_config['category_button']['font_size']}px;
                }}
                QPushButton:hover {{
                    background: {config['hover_background']};
                    border-color: {config['hover_border_color']};
                }}
            """

    @classmethod
    def get_product_button_style(cls):
        """Generate product button style without size properties"""
        if not cls._check_config():
            return ""
        
        config = ProductButtonConfig.DEFAULTS
        grid_config = cls.layout_config.get_product_grid_config()
        
        return f"""
            QPushButton {{
                background: {config['background']};
                border: 1px solid {config['border_color']};
                border-radius: {grid_config['product_button']['radius']}px;
                padding: {grid_config['product_button']['padding']}px;
                color: {config['text_color']};
                font-weight: {config['font_weight']};
                font-size: {grid_config['product_button']['font_size']}px;
            }}
            QPushButton:hover {{
                background: {config['background_hover']};
                border-color: {config['border_color_hover']};
            }}
            QPushButton:pressed {{
                background: {config['background_pressed']};
            }}
        """
    
    @classmethod
    def _check_config(cls):
        """Common configuration check
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        if not cls.layout_config:
            return False
        return True