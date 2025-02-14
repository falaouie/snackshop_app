from .types import HorizontalButtonType

class HorizontalButtonConfig:
    """Configuration for horizontal buttons in order panel"""
    DEFAULTS = {
        "text_color": "#FFFFFF",
        "font_weight": 500,
        "border": "none",
    }

    BUTTON_CONFIGS = {
        HorizontalButtonType.HOLD: {
            "text": "Hold",
            "colors": {
                "primary": "#FFC107",
                "hover": "#FFB300",
                "text": "#000000"  # Special case: black text for hold button
            },
            "action": "hold_order"
        },
        HorizontalButtonType.VOID: {
            "text": "VOID",
            "colors": {
                "primary": "#F44336",
                "hover": "#E53935",
                "text": DEFAULTS["text_color"]
            },
            "action": "void_order"
        },
        HorizontalButtonType.NO_SALE: {
            "text": "NO SALE",
            "colors": {
                "primary": "#9E9E9E",
                "hover": "#757575",
                "text": DEFAULTS["text_color"]
            },
            "action": "no_sale"
        }
    }

    @classmethod
    def get_config(cls, button_type: HorizontalButtonType) -> dict:
        """Get configuration for a specific horizontal button type"""
        return cls.BUTTON_CONFIGS.get(button_type, {})