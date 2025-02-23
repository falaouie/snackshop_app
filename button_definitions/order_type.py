from .types import OrderButtonType

class OrderTypeButtonConfig:
    """Configuration for order type buttons"""
    DEFAULTS = {
        # Normal state
        "text_color": "#333333",
        "background": "white",
        "border_color": "#DEDEDE",
        # Selected state
        "selected_text_color": "white",
        "selected_background": "black",
        "selected_border_color": "#2196F3",
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