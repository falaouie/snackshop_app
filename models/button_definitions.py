"""
Core button definitions and configurations
Defines what buttons exist and their basic properties,
excluding size and style-specific details
"""

# Order type configurations
ORDER_TYPES = {
    "DINE_IN": {
        "text": "Dine In",
        "action": "set_dine_in"
    },
    "TAKE_AWAY": {
        "text": "Take-Away",
        "action": "set_take_away"
    },
    "DELIVERY": {
        "text": "Delivery",
        "action": "set_delivery"
    }
}

# Action button configurations
HORIZONTAL_BUTTONS = {
    "HOLD": {
        "text": "Hold",
        "colors": {
            "primary": "#FFC107",
            "hover": "#FFB300",
            "text": "#000000"
        },
        "action": "hold_order"
    },
    "VOID": {
        "text": "VOID",
        "colors": {
            "primary": "#F44336",
            "hover": "#E53935",
            "text": "#FFFFFF"
        },
        "action": "void_order"
    },
    "NO_SALE": {
        "text": "NO SALE",
        "colors": {
            "primary": "#9E9E9E",
            "hover": "#757575",
            "text": "#FFFFFF"
        },
        "action": "no_sale"
    }
}

# Transaction button configurations
TRANSACTION_BUTTONS = {
    "HOLD": {
        "text": "Hold",
        "colors": {
            "primary": "#FFC107",
            "hover": "#FFB300",
            "text": "#000000"
        },
        "action": "hold_transaction"
    },
    "VOID": {
        "text": "VOID",
        "colors": {
            "primary": "#F44336",
            "hover": "#E53935",
            "text": "#FFFFFF"
        },
        "action": "void_transaction"
    },
    "PAID_IN": {
        "text": "PAID IN",
        "colors": {
            "primary": "#9E9E9E",
            "hover": "#757575",
            "text": "#FFFFFF"
        },
        "action": "paid_in"
    },
    "PAID_OUT": {
        "text": "PAID OUT",
        "colors": {
            "primary": "#9E9E9E",
            "hover": "#757575",
            "text": "#FFFFFF"
        },
        "action": "paid_out"
    },
    "NO_SALE": {
        "text": "NO SALE",
        "colors": {
            "primary": "#9E9E9E",
            "hover": "#757575",
            "text": "#FFFFFF"
        },
        "action": "no_sale"
    },
    "DISCOUNT": {
        "text": "DISCOUNT",
        "colors": {
            "primary": "#4CAF50",
            "hover": "#43A047",
            "text": "#FFFFFF"
        },
        "action": "apply_discount"
    },
    "BLANK": {
        "text": "Blank",
        "colors": {
            "primary": "#9E9E9E",
            "hover": "#757575",
            "text": "#FFFFFF"
        },
        "action": None
    },
    "NUM_PAD": {
        "text": "NUM PAD",
        "colors": {
            "primary": "#9E9E9E",
            "hover": "#757575",
            "text": "#FFFFFF"
        },
        "action": "show_numpad"
    }
}

# Payment button configurations
PAYMENT_BUTTONS = {
    "CASH": {
        "text": "PAY CASH",
        "colors": {
            "primary": "#006400",  # darkgreen
            "hover": "#48A848",
            "text": "#FFFFFF"
        },
        "action": "process_cash_payment"
    },
    "OTHER": {
        "text": "PAY OTHER",
        "colors": {
            "primary": "#FFBF00",
            "hover": "#FFB300",
            "text": "#FFFFFF"
        },
        "action": "process_other_payment"
    }
}