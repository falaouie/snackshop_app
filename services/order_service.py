from decimal import Decimal
from models.order_item import OrderItem
from typing import List, Optional, Dict, Any
from button_definitions.types import OrderButtonType

class OrderService:
    def __init__(self):
        self.current_order_items: List[OrderItem] = []
        self.order_id: Optional[str] = None
        self.order_type: str = "TAKE_AWAY"  # Default order type
        self.order_status: str = "NEW"  # Initial status
        
    def create_new_order(self) -> None:
        """Start a fresh order"""
        self.current_order_items = []
        # In the future, generate a real order ID
        self.order_id = None
        self.order_status = "NEW"
        
    def add_item(self, item_name: str, price: float, quantity: int = 1) -> OrderItem:
        """Add item to the current order"""
        # Check if item already exists
        existing_item = self.find_item_by_name(item_name)
        
        if existing_item:
            existing_item.increment_quantity(quantity)
            return existing_item
        
        # Create new item
        new_item = OrderItem(
            name=item_name,
            price=Decimal(str(price)),
            quantity=quantity
        )
        self.current_order_items.append(new_item)
        return new_item
        
    def remove_item(self, item: OrderItem) -> None:
        """Remove an item from the current order"""
        if item in self.current_order_items:
            self.current_order_items.remove(item)
            
    def clear_order(self) -> None:
        """Clear all items from the current order"""
        self.current_order_items = []
        
    def find_item_by_name(self, item_name: str) -> Optional[OrderItem]:
        """Find an item in the order by name"""
        for item in self.current_order_items:
            if item.name == item_name:
                return item
        return None
        
    def set_order_type(self, order_type: str) -> None:
      """Set the type of the current order"""
      # Validate that it's a valid order type
      valid_types = [t.value for t in OrderButtonType]
      if order_type in valid_types:
          self.order_type = order_type
      else:
          # Default to TAKE_AWAY if invalid
          self.order_type = OrderButtonType.TAKE_AWAY.value
        
    def get_total(self) -> Decimal:
        """Calculate the total for the current order"""
        return sum(item.get_total() for item in self.current_order_items)
        
    def update_item_quantity(self, item_name: str, final_quantity: int) -> None:
        """Update an item's quantity or remove if zero"""
        item = self.find_item_by_name(item_name)
        if not item:
            return
            
        if final_quantity <= 0:
            self.remove_item(item)
        else:
            item.set_quantity(final_quantity)
            
    def get_order_summary(self) -> Dict[str, Any]:
        """Return a summary of the current order"""
        return {
            'order_id': self.order_id,
            'order_type': self.order_type,
            'order_status': self.order_status,
            'total': float(self.get_total()),
            'item_count': sum(item.quantity for item in self.current_order_items),
            'items': [item.to_dict() for item in self.current_order_items]
        }