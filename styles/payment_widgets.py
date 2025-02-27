# styles/payment_widgets.py
"""Styles for payment-related widgets"""

# styles/payment_widgets.py
"""Styles for payment-related widgets"""

class PaymentWidgetStyles:
    """Styles for payment widgets including base, preset, and specific payment types"""
    
    @staticmethod
    def get_container_style():
        """Get style for all payment widget containers"""
        return """
            QFrame { 
                background: white; 
                border: 1px solid #dddddd; 
                border-radius: 5px; 
            }
        """
    
    @staticmethod
    def get_preset_button_style(currency_type, config):
        """Get style for preset amount buttons
        
        Args:
            currency_type: "USD" or "LBP" for appropriate hover colors
            config: Button configuration from layout_config
        """
        hover_color = "#1890ff" if currency_type == "USD" else "#52c41a"
        
        return f"""
            QPushButton {{
                background: white;
                border: 1px solid #ddd;
                border-radius: {config['radius']}px;
                padding: {config['padding']}px;
                font-size: {config['font_size']}px;
            }}
            QPushButton:hover {{
                background: #f0f0f0;
                border-color: {hover_color};
            }}
            QPushButton:disabled {{
                background: #f5f5f5;
                border: 1px solid #ddd;
                color: #999;
            }}
        """
    
    @staticmethod
    def get_payment_action_button_style(payment_type, button_color, hover_color, config):
        """Get style for payment action buttons
        
        Args:
            payment_type: Payment type identifier
            button_color: Base button color
            hover_color: Hover state color
            config: Button configuration from layout_config
        """
        return f"""
            QPushButton {{
                background: {button_color};
                color: white;
                border: none;
                border-radius: {config['radius']}px;
                padding: {config['padding']}px;
                font-size: {config['font_size']}px;
                font-weight: bold;
                min-width: {config['width']}px;
                min-height: {config['height']}px;
            }}
            QPushButton:hover {{
                background: {hover_color};
            }}
        """
    
    # Special styles for specific payment types
    
    @staticmethod
    def get_usd_action_button_style(config):
        """USD-specific action button style"""
        return f"""
            QPushButton {{
                background: #1890ff;
                color: white;
                border: none;
                border-radius: {config['radius']}px;
                padding: {config['padding']}px;
                font-size: {config['font_size']}px;
                font-weight: bold;
                min-width: {config['width']}px;
                min-height: {config['height']}px;
            }}
            QPushButton:hover {{
                background: #096dd9;
            }}
        """
    
    @staticmethod
    def get_lbp_action_button_style(config):
        """LBP-specific action button style"""
        return f"""
            QPushButton {{
                background: #52c41a;
                color: white;
                border: none;
                border-radius: {config['radius']}px;
                padding: {config['padding']}px;
                font-size: {config['font_size']}px;
                font-weight: bold;
                min-width: {config['width']}px;
                min-height: {config['height']}px;
            }}
            QPushButton:hover {{
                background: #389e0d;
            }}
        """
    
    @staticmethod
    def get_card_payment_button_style(config):
        """Card payment-specific button style"""
        return f"""
            QPushButton {{
                background: #fa541c;
                color: white;
                border: none;
                border-radius: {config['radius']}px;
                padding: {config['padding']}px;
                font-size: {config['font_size']}px;
                font-weight: bold;
                min-width: {config['width']}px;
                min-height: {config['height']}px;
            }}
            QPushButton:hover {{
                background: #d4380d;
            }}
    """

    @staticmethod
    def get_other_payment_button_style(config):
        """Other payment-specific button style"""
        return f"""
            QPushButton {{
                background: #722ed1;
                color: white;
                border: none;
                border-radius: {config['radius']}px;
                padding: {config['padding']}px;
                font-size: {config['font_size']}px;
                font-weight: bold;
                min-width: {config['width']}px;
                min-height: {config['height']}px;
            }}
            QPushButton:hover {{
                background: #531dab;
            }}
        """