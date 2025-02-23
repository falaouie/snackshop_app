from enum import Enum, auto

class ButtonType(Enum):
    """Enum for different types of buttons"""
    PAYMENT = auto()
    TRANSACTION = auto()
    ORDER = auto()
    # HORIZONTAL = auto()

class PaymentButtonType(Enum):
    """Specific payment button types"""
    CASH = "CASH"
    OTHER = "OTHER"

class TransactionButtonType(Enum):
    """Specific transaction button types"""
    HOLD = "HOLD"
    VOID = "VOID"
    PAID_IN = "PAID_IN"
    PAID_OUT = "PAID_OUT"
    NO_SALE = "NO_SALE"
    DISCOUNT = "DISCOUNT"
    BLANK = "BLANK"
    NUM_PAD = "NUM_PAD"

class OrderButtonType(Enum):
    """Order type button types"""
    DINE_IN = "DINE_IN"
    TAKE_AWAY = "TAKE_AWAY"
    DELIVERY = "DELIVERY"

# class HorizontalButtonType(Enum):
#     """Horizontal button types in order panel"""
#     HOLD = "HOLD"
#     VOID = "VOID"
#     NO_SALE = "NO_SALE"

class ProductButtonType(Enum):
    """Product button type"""
    PRODUCT = "PRODUCT"

class CategoryButtonType(Enum):
    """Category button types"""
    CATEGORY = "CATEGORY" 