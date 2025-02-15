from config.screen_config import screen_config
from button_definitions.types import (
    PaymentButtonType, 
    TransactionButtonType, 
    OrderButtonType,
    HorizontalButtonType
)
from button_definitions.horizontal import HorizontalButtonConfig
from button_definitions.payment import PaymentButtonConfig
from button_definitions.order import OrderButtonConfig
from button_definitions.transaction import TransactionButtonConfig
from button_definitions.product import ProductButtonConfig
from button_definitions.category import CategoryButtonConfig
from .base import BaseStyles

class ButtonStyles:
    """Button-specific styles"""
    
    @staticmethod
    def get_payment_button_style(button_type: PaymentButtonType) -> str:
        """Generate payment button style based on new configuration"""
        # Get button configuration
        config = PaymentButtonConfig.get_config(button_type)
        if not config:
            return ""
            
        # Get size configuration
        sizes = screen_config.get_size('payment_button')
        
        # Generate style using base style generator
        return BaseStyles.create_button_style(
            background_color=config['colors']['primary'],
            text_color=config['colors']['text'],
            hover_color=config['colors']['hover'],
            border_radius=sizes['border_radius'],
            padding=sizes['padding'],
            font_size=sizes['font_size']
        )
    
    @staticmethod
    def get_transaction_button_style(button_type: TransactionButtonType) -> str:
        """Generate transaction button style based on configuration"""
        config = TransactionButtonConfig.get_config(button_type)
        if not config:
            return ""
            
        sizes = screen_config.get_size('transaction_button')
        
        return BaseStyles.create_button_style(
            background_color=config['colors']['primary'],
            text_color=config['colors']['text'],
            hover_color=config['colors']['hover'],
            border_radius=sizes['border_radius'],
            padding=sizes['padding'],
            font_size=sizes['font_size']
        )
    
    @staticmethod
    def get_order_button_style() -> str:
        """Generate order type button style"""
        config = OrderButtonConfig.DEFAULTS
        sizes = screen_config.get_size('order_type_button')
        
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
    def get_horizontal_button_style(button_type: HorizontalButtonType) -> str:
        """Generate horizontal button style based on configuration"""
        config = HorizontalButtonConfig.get_config(button_type)
        if not config:
            return ""
            
        sizes = screen_config.get_size('horizontal_button')
        
        return BaseStyles.create_button_style(
            background_color=config['colors']['primary'],
            text_color=config['colors']['text'],
            hover_color=config['colors']['hover'],
            border_radius=sizes['border_radius'],
            padding=sizes['padding'],
            font_size=sizes['font_size']
        )
    
    @staticmethod
    def get_product_button_style(custom_colors: dict = None) -> str:
        """
        Generate product button style based on configuration
        
        Args:
            custom_colors: Optional custom colors for admin customization
        """
        # Start with default config
        config = ProductButtonConfig.DEFAULTS.copy()
        
        # Apply any custom colors
        if custom_colors:
            config.update(custom_colors)
            
        sizes = screen_config.get_size('pos_product_button')
        
        return f"""
            QPushButton {{
                background: {config['background']};
                color: {config['text_color']};
                border: 1px solid {config['border_color']};
                border-radius: {screen_config.get_size('button_border_radius')}px;
                padding: {screen_config.get_size('button_padding')}px;
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
    
    @staticmethod
    def get_category_button_style(is_selected: bool = False, custom_colors: dict = None) -> str:
        """Generate category button style based on state"""
        config = CategoryButtonConfig.DEFAULTS.copy()
        if custom_colors:
            config.update(custom_colors)

        # Use correct screen config keys
        border_radius = screen_config.get_size('button_border_radius')
        padding = screen_config.get_size('button_padding')
        width = screen_config.get_size('pos_category_button_width')
        height = screen_config.get_size('pos_category_button_height')
        
        if is_selected:
            return f"""
                QPushButton {{
                    background: {config['selected_background']};
                    color: {config['selected_text_color']};
                    border: none;
                    border-radius: {border_radius}px;
                    padding: {padding}px;
                    font-size: 13px;
                    font-weight: 500;
                    width: {width}px;
                    height: {height}px;
                }}
                QPushButton:hover {{
                    background: {config['selected_hover_background']};
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background: {config['background']};
                    color: {config['text_color']};
                    border: 1px solid {config['border_color']};
                    border-radius: {border_radius}px;
                    padding: {padding}px;
                    font-size: 13px;
                    width: {width}px;
                    height: {height}px;
                }}
                QPushButton:hover {{
                    background: {config['hover_background']};
                    border-color: {config['hover_border_color']};
                }}
            """