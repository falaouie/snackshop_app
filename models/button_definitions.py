"""
Constants for button definitions and related UI elements
"""

# Order type buttons
ORDER_TYPES = ["Dine In", "Take-Away", "Delivery"]

# Action button configurations
HORIZONTAL_BUTTONS = {
    "Hold": {"bg": "#FFC107", "hover": "#FFB300", "text": "#000000"},
    "VOID": {"bg": "#F44336", "hover": "#E53935", "text": "#FFFFFF"},
    "NO SALE": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"}
}

# Transaction button configurations
TRANSACTION_BUTTONS = {
    "Hold": {"bg": "#FFC107", "hover": "#FFB300", "text": "#000000"},
    "VOID": {"bg": "#F44336", "hover": "#E53935", "text": "#FFFFFF"},
    "PAID IN": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
    "PAID OUT": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
    "NO SALE": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
    "DISCOUNT": {"bg": "#4CAF50", "hover": "#43A047", "text": "#FFFFFF"},
    "Blank": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
    "NUM PAD": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"}
}

# Payment button configurations
PAYMENT_BUTTONS = {
    "cash": {
        "text": "PAY CASH",
        "bg": "darkgreen",
        "hover": "#48A848",
        "text_color": "#FFFFFF",
        "font_size": 20
    },
    "other": {
        "text": "PAY OTHER",
        "bg": "#FFBF00",
        "hover": "#FFB300",
        "text_color": "#FFFFFF",
        "font_size": 18
    }
}