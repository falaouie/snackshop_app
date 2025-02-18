"""
OrderItem model for managing individual items in a POS order.
"""
from decimal import Decimal
from typing import Optional
from dataclasses import dataclass

@dataclass
class OrderItem:
    """
    Represents an item in a POS order with quantity and price tracking.
    
    Attributes:
        name (str): Name of the product
        price (Decimal): Unit price of the product
        quantity (int): Quantity of items ordered
        discount (Decimal): Discount amount per unit (default 0)
        notes (str): Optional notes for the item
    """
    name: str
    price: Decimal
    quantity: int = 1
    discount: Decimal = Decimal('0')
    notes: Optional[str] = None

    def __post_init__(self):
        """Convert price and discount to Decimal if they aren't already"""
        self.price = Decimal(str(self.price))
        self.discount = Decimal(str(self.discount))

    def get_total(self) -> Decimal:
        """Calculate total price for this item including quantity and discounts"""
        return (self.price - self.discount) * self.quantity

    def increment_quantity(self, amount: int = 1) -> None:
        """Increment the quantity by the specified amount"""
        self.quantity += amount

    def decrement_quantity(self, amount: int = 1) -> None:
        """Decrement the quantity by the specified amount"""
        self.quantity = max(0, self.quantity - amount)

    def set_quantity(self, quantity: int) -> None:
        """Set the quantity directly, ensuring it's not negative"""
        self.quantity = max(0, quantity)

    def apply_discount(self, amount: Decimal) -> None:
        """Apply a per-unit discount"""
        self.discount = Decimal(str(amount))

    def clear_discount(self) -> None:
        """Remove any applied discount"""
        self.discount = Decimal('0')

    def get_subtotal(self) -> Decimal:
        """Calculate subtotal before discounts"""
        return self.price * self.quantity

    def get_discount_total(self) -> Decimal:
        """Calculate total discount amount"""
        return self.discount * self.quantity

    def to_dict(self) -> dict:
        """Convert the order item to a dictionary representation"""
        return {
            'name': self.name,
            'price': float(self.price),
            'quantity': self.quantity,
            'discount': float(self.discount),
            'notes': self.notes,
            'total': float(self.get_total())
        }