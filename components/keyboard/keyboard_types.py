from enum import Enum

class KeyboardType(Enum):
    """Enum defining different types of virtual keyboards"""
    FULL = "full"          # Standard QWERTY keyboard with numbers
    NUMERIC = "numeric"    # Numbers only (0-9)
    DECIMAL = "decimal"    # Numbers with decimal point
    EMAIL = "email"        # Standard keyboard with @ and common email domains
    PHONE = "phone"        # Phone number format keyboard
    SEARCH = "search"      # Standard keyboard with search-specific features