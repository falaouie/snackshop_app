from .types import TransactionButtonType

class TransactionButtonConfig:
    """Configuration for transaction buttons"""
    DEFAULTS = {
        "text_color": "#FFFFFF",
        "font_weight": 500,
        "border": "none",
    }

    BUTTON_CONFIGS = {
        TransactionButtonType.HOLD: {
            "text": "Hold",
            "colors": {
                "primary": "#FFC107",
                "hover": "#FFB300",
                "text": "#000000"
            },
            "action": "hold_transaction"
        },
        TransactionButtonType.VOID: {
            "text": "VOID",
            "colors": {
                "primary": "#F44336",
                "hover": "#E53935",
                "text": DEFAULTS["text_color"]
            },
            "action": "void_transaction"
        },
        TransactionButtonType.PAID_IN: {
            "text": "PAID IN",
            "colors": {
                "primary": "#9E9E9E",
                "hover": "#757575",
                "text": DEFAULTS["text_color"]
            },
            "action": "paid_in"
        },
        TransactionButtonType.PAID_OUT: {
            "text": "PAID OUT",
            "colors": {
                "primary": "#9E9E9E",
                "hover": "#757575",
                "text": DEFAULTS["text_color"]
            },
            "action": "paid_out"
        },
        TransactionButtonType.NO_SALE: {
            "text": "NO SALE",
            "colors": {
                "primary": "#9E9E9E",
                "hover": "#757575",
                "text": DEFAULTS["text_color"]
            },
            "action": "no_sale"
        },
        TransactionButtonType.DISCOUNT: {
            "text": "DISCOUNT",
            "colors": {
                "primary": "#4CAF50",
                "hover": "#43A047",
                "text": DEFAULTS["text_color"]
            },
            "action": "apply_discount"
        },
        TransactionButtonType.BLANK: {
            "text": "Blank",
            "colors": {
                "primary": "#9E9E9E",
                "hover": "#757575",
                "text": DEFAULTS["text_color"]
            },
            "action": None
        },
        TransactionButtonType.NUM_PAD: {
            "text": "NUM PAD",
            "colors": {
                "primary": "#9E9E9E",
                "hover": "#757575",
                "text": DEFAULTS["text_color"]
            },
            "action": "show_numpad"
        }
    }

    @classmethod
    def get_config(cls, button_type: TransactionButtonType) -> dict:
        """Get configuration for a specific transaction button type"""
        return cls.BUTTON_CONFIGS.get(button_type, {})