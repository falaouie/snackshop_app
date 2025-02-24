from enum import Enum, auto

class NumpadMode(Enum):
    """Available modes for the numpad component"""
    QTY = auto()   # For quantities and inventory
    USD = auto()   # For USD amounts
    LBP = auto()   # For LBP amounts
    DEFAULT = auto() # For standalone operation

class NumpadState(Enum):
    """Operating state of the numpad"""
    STANDALONE = auto()    # Independent operation (e.g., POS view)
    INPUT_BOUND = auto()   # Bound to input field

class NumpadValidation:
    """Validation rules for different numpad modes"""
    RULES = {
        NumpadMode.QTY: {
            'allow_decimal': False,
            'max_digits': 4,
            'min_value': 1,
            'max_value': 9999
        },
        # NumpadMode.WGT: {
        #     'allow_decimal': True,
        #     'max_digits': 6,
        #     'decimal_places': 3,
        #     'min_value': 0.001,
        #     'max_value': 999.999
        # },
        NumpadMode.USD: {
            'allow_decimal': True,
            'max_digits': 8,
            'decimal_places': 2,
            'min_value': 0.01,
            'max_value': 999999.99
        },
        NumpadMode.LBP: {
            'allow_decimal': False,
            'max_digits': 9,
            'min_value': 1,  # Changed from 1000 to allow building up the number
            'max_value': 999999999,
            'increment': 1000  # New field to indicate minimum increment
        }
    }