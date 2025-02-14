from .types import PaymentButtonType

class PaymentButtonConfig:
    """Configuration for payment buttons"""
    DEFAULTS = {
        "text_color": "#FFFFFF",
        "font_weight": 500,
        "border": "none",
    }

    BUTTON_CONFIGS = {
        PaymentButtonType.CASH: {
            "text": "PAY CASH",
            "colors": {
                "primary": "#006400",
                "hover": "#48A848",
                "text": DEFAULTS["text_color"]
            },
            "action": "process_cash_payment"
        },
        PaymentButtonType.OTHER: {
            "text": "PAY OTHER",
            "colors": {
                "primary": "#FFBF00",
                "hover": "#FFB300",
                "text": DEFAULTS["text_color"]
            },
            "action": "process_other_payment"
        }
    }

    @classmethod
    def get_config(cls, button_type: PaymentButtonType) -> dict:
        """Get configuration for a specific payment button type"""
        return cls.BUTTON_CONFIGS.get(button_type, {})