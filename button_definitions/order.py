from .types import OrderButtonType

class OrderButtonConfig:
    """Configuration for order type buttons"""
    DEFAULTS = {
        "text_color": "#333333",
        "text_color_selected": "#FFFFFF",
        "border_color": "#DEDEDE",
        "border_color_selected": "#2196F3",
        "background": "white",
        "background_selected": "#2196F3",
        "background_hover": "#F8F9FA"
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