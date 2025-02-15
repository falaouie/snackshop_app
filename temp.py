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
    
    # Rest of the ButtonStyles methods, but change all @staticmethod to @classmethod
    # and use cls.screen_config instead of directly importing screen_config