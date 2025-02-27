# styles/payment_widgets.py
"""Styles for payment-related widgets"""

class PaymentWidgetStyles:
    """Styles for payment widgets including base, preset, and specific payment types"""
    
    @staticmethod
    def get_container_style(style_override=None):
        """Get style for all payment widget containers with optional overrides
        
        Args:
            style_override: Optional dict with custom style properties
        """
        # Default style properties
        style_props = {
            'background': 'white',
            'border': '1px solid #dddddd',
            'border-radius': '5px'
        }
        
        # Apply any overrides
        if style_override:
            style_props.update(style_override)
        
        # Build style string
        style_str = "QFrame { "
        for prop, value in style_props.items():
            style_str += f"{prop}: {value}; "
        style_str += "}"
        
        return style_str
    
    @staticmethod
    def get_preset_button_style(currency_type, config, style_override=None):
        """Get style for preset amount buttons with optional overrides
        
        Args:
            currency_type: "USD" or "LBP" for appropriate hover colors
            config: Button configuration from layout_config
            style_override: Optional dict with custom style properties
        """
        hover_color = "#1890ff" if currency_type == "USD" else "#52c41a"
        
        # Default style properties
        style_props = {
            'background': 'white',
            'border': '1px solid #ddd',
            'border-radius': f"{config['radius']}px",
            'padding': f"{config['padding']}px",
            'font-size': f"{config['font_size']}px",
            'text-align': 'center'
        }
        
        hover_props = {
            'background': '#f0f0f0',
            'border-color': hover_color
        }
        
        disabled_props = {
            'background': '#f5f5f5',
            'border': '1px solid #ddd',
            'color': '#999'
        }
        
        # Apply any overrides
        if style_override:
            if 'normal' in style_override:
                style_props.update(style_override['normal'])
            if 'hover' in style_override:
                hover_props.update(style_override['hover'])
            if 'disabled' in style_override:
                disabled_props.update(style_override['disabled'])
        
        # Build style string
        style_str = "QPushButton { "
        for prop, value in style_props.items():
            style_str += f"{prop}: {value}; "
        style_str += "} "
        
        style_str += "QPushButton:hover { "
        for prop, value in hover_props.items():
            style_str += f"{prop}: {value}; "
        style_str += "} "
        
        style_str += "QPushButton:disabled { "
        for prop, value in disabled_props.items():
            style_str += f"{prop}: {value}; "
        style_str += "}"
        
        return style_str
    
    @staticmethod
    def get_payment_action_button_style(payment_type, button_color, hover_color, config, style_override=None):
        """Get style for payment action buttons with optional overrides
        
        Args:
            payment_type: Payment type identifier
            button_color: Base button color
            hover_color: Hover state color
            config: Button configuration from layout_config
            style_override: Optional dict with custom style properties
        """
        # Default style properties
        style_props = {
            'background': button_color,
            'color': 'white',
            'border': 'none',
            'border-radius': f"{config['radius']}px",
            'padding': f"{config['padding']}px",
            'font-size': f"{config['font_size']}px",
            'font-weight': 'bold',
            'min-width': f"{config['width']}px",
            'min-height': f"{config['height']}px"
        }
        
        hover_props = {
            'background': hover_color
        }
        
        # Apply any overrides
        if style_override:
            if 'normal' in style_override:
                style_props.update(style_override['normal'])
            if 'hover' in style_override:
                hover_props.update(style_override['hover'])
        
        # Build style string
        style_str = "QPushButton { "
        for prop, value in style_props.items():
            style_str += f"{prop}: {value}; "
        style_str += "} "
        
        style_str += "QPushButton:hover { "
        for prop, value in hover_props.items():
            style_str += f"{prop}: {value}; "
        style_str += "} "
        
        return style_str
    
    # Special styles for specific payment types
    
    @staticmethod
    def get_usd_action_button_style(config, style_override=None):
        """USD-specific action button style with optional overrides"""
        button_color = "#1890ff"
        hover_color = "#096dd9"
        
        return PaymentWidgetStyles.get_payment_action_button_style(
            "USD", button_color, hover_color, config, style_override
        )
    
    @staticmethod
    def get_lbp_action_button_style(config, style_override=None):
        """LBP-specific action button style with optional overrides"""
        button_color = "#52c41a"
        hover_color = "#389e0d"
        
        return PaymentWidgetStyles.get_payment_action_button_style(
            "LBP", button_color, hover_color, config, style_override
        )
    
    @staticmethod
    def get_card_payment_button_style(config, style_override=None):
        """Card payment-specific button style with optional overrides"""
        button_color = "#fa541c"
        hover_color = "#d4380d"
        
        return PaymentWidgetStyles.get_payment_action_button_style(
            "CARD", button_color, hover_color, config, style_override
        )
    
    @staticmethod
    def get_other_payment_button_style(config, style_override=None):
        """Other payment-specific button style with optional overrides"""
        button_color = "#722ed1"
        hover_color = "#531dab"
        
        return PaymentWidgetStyles.get_payment_action_button_style(
            "OTHER", button_color, hover_color, config, style_override
        )