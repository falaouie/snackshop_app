@classmethod
def get_payment_button_style(cls, button_type):
    """Generate payment button style based on configuration"""
    if not cls.layout_config:
        return ""
            
    config = PaymentButtonConfig.get_config(PaymentButtonType(button_type))
    if not config:
        return ""
            
    # Pass 'payment' string instead of button_type enum
    button_config = cls.layout_config.get_button_config('payment')
    
    return f"""
        QPushButton {{
            background-color: {config['colors']['primary']};
            color: {config['colors']['text']};
            border: none;
            border-radius: {button_config['padding']}px;
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