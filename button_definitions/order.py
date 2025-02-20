from .types import OrderButtonType

class OrderButtonConfig:
    """Configuration for order type buttons"""
    DEFAULTS = {
        # Normal state
        "text_color": "#333333",
        "background": "white",
        "border_color": "#DEDEDE",
        # Selected state
        "selected_text_color": "white",
        "selected_background": "#2196F3",
        "selected_border_color": "#2196F3",
        # Hover state
        "hover_background": "#F8F9FA",
        "hover_border_color": "#2196F3",
        # Selected hover state
        "selected_hover_background": "#1E88E5",
    }

    BUTTON_CONFIGS = {
        OrderButtonType.DINE_IN: {
            "text": "Dine In",
            "action": "set_dine_in",
            "default_selected": True
        },
        OrderButtonType.TAKE_AWAY: {
            "text": "Take-Away",
            "action": "set_take_away",
            "default_selected": False
        },
        OrderButtonType.DELIVERY: {
            "text": "Delivery",
            "action": "set_delivery",
            "default_selected": False
        }
    }

    @classmethod
    def get_config(cls, button_type: OrderButtonType) -> dict:
        """Get configuration for a specific order button type"""
        config = cls.BUTTON_CONFIGS.get(button_type, {}).copy()
        config['colors'] = cls.DEFAULTS
        return config