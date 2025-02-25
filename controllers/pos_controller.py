from services.payment_service import PaymentService
from services.order_service import OrderService
from services.product_service import ProductService
from services.validation_service import ValidationService
from button_definitions.types import PaymentButtonType
from typing import Tuple, Dict, List, Any, Optional

class POSController:
    def __init__(self):
        # Initialize services
        self.payment_service = PaymentService()
        self.order_service = OrderService()
        self.product_service = ProductService()
        self.validation_service = ValidationService()
        
    def get_exchange_rate(self) -> float:
        """Get current exchange rate from payment service"""
        return self.payment_service.get_exchange_rate()
        
    # Payment-related methods
    def process_payment(self, payment_type: str, value_str: str) -> Tuple[bool, str]:
        """Process payment through the payment service"""
        order_total = self.order_service.get_total()
        success, message, payment_info = self.payment_service.process_payment(
            payment_type, value_str, float(order_total)
        )
        
        if not success:
            return False, message
            
        # In a real implementation, you would:
        # 1. Finalize the order
        # 2. Generate a receipt
        # 3. Reset for a new order
        
        return True, f"Payment of {payment_info['amount']} processed successfully"
    
    # Order-related methods
    def add_product_to_order(self, product_name: str, quantity: int = 1) -> bool:
        """Add a product to the current order"""
        price = self.product_service.get_product_price(product_name)
        if price <= 0:
            print(f"Product {product_name} price not found or invalid")
            return False
            
        print(f"Adding {quantity} x {product_name} at price {price}")
        self.order_service.add_item(product_name, price, quantity)
        return True

        
    def remove_item_from_order(self, item):
        """Remove an item from the current order"""
        print(f"Removing item: {item.name}")  # Debug print
        self.order_service.remove_item(item)
        return True
        
    def clear_order(self) -> None:
        """Clear the current order"""
        print("Clearing order")  # Debug print
        self.order_service.clear_order()
        
    def update_item_quantity(self, item_name: str, quantity: int) -> None:
        """Update an item's quantity"""
        self.order_service.update_item_quantity(item_name, quantity)
        
    def get_order_total(self) -> float:
        """Get the total for the current order"""
        return float(self.order_service.get_total())
        
    def set_order_type(self, order_type: str) -> None:
        """Set the order type"""
        self.order_service.set_order_type(order_type)
        
    def get_order_summary(self) -> Dict[str, Any]:
        """Get a summary of the current order"""
        return self.order_service.get_order_summary()
    
    # Product-related methods
    def get_filtered_products(self, search_text: str) -> List[str]:
        """Get products filtered by search text"""
        return self.product_service.filter_products(search_text)
        
    def get_product_price(self, product_name: str) -> float:
        """Get price for a product"""
        return self.product_service.get_product_price(product_name)
        
    def find_existing_item(self, item_name: str) -> Optional[Any]:
        """Find an existing item in the order"""
        return self.order_service.find_item_by_name(item_name)
    
    # validation methods
    def validate_product_quantity(self, value_str):
        """Validate quantity input for products"""
        return self.validation_service.validate_product_quantity(value_str)
        
    def validate_payment_input(self, payment_type, value_str):
      """Validate payment input"""
      # Temporary direct implementation until validation_service is fully integrated
      try:
          if payment_type == PaymentButtonType.CASH_LBP.value and '.' in value_str:
              return False, "Only whole numbers accepted for LBP"
              
          if payment_type == PaymentButtonType.CASH_LBP.value:
              amount = int(value_str)
          else:
              amount = float(value_str)
              
          if amount <= 0:
              return False, "Amount must be greater than zero"
              
          return True, None
      except ValueError:
          return False, "Invalid amount format"