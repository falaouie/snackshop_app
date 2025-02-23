from .types import PaymentButtonType

class PaymentButtonConfig:
    """Configuration for payment buttons"""
    DEFAULTS = {
        "text_color": "#FFFFFF",
        "font_weight": 500,
        "border": "none",
    }

    BUTTON_CONFIGS = {
        PaymentButtonType.CASH_USD: {
            "text": "CASH USD",
            "colors": {
                "primary": "#006400",  # Dark green
                "hover": "#48A848",    # Lighter green
                "text": DEFAULTS["text_color"]
            },
            "action": "process_cash_usd_payment"
        },
        PaymentButtonType.CASH_LBP: {
            "text": "CASH LBP",
            "colors": {
                "primary": "#004D40",  # Dark teal
                "hover": "#00897B",    # Lighter teal
                "text": DEFAULTS["text_color"]
            },
            "action": "process_cash_lbp_payment"
        },
        PaymentButtonType.OTHER: {
            "text": "PAY OTHER",
            "colors": {
                "primary": "#FFBF00",  # Amber
                "hover": "#FFB300",    # Lighter amber
                "text": DEFAULTS["text_color"]
            },
            "action": "process_other_payment"
        }
    }

    @classmethod
    def get_config(cls, button_type: PaymentButtonType) -> dict:
        """Get configuration for a specific payment button type"""
        return cls.BUTTON_CONFIGS.get(button_type, {})