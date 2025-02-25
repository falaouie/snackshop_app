from button_definitions.types import PaymentButtonType
from decimal import Decimal
from services.validation_service import ValidationService

class PaymentService:
    def __init__(self, exchange_rate=None):
        self.exchange_rate = exchange_rate or 90000  # Default value
        self.validation_service = ValidationService()
        
    def get_exchange_rate(self):
        """Return the current exchange rate"""
        return self.exchange_rate
    
    def validate_payment(self, payment_type, value_str):
        """Validate payment input based on payment type"""
        if not value_str:
            return False, "No payment amount entered"

        # Handle validation without using validation_service for now
        # Basic validation
        try:
            if payment_type == PaymentButtonType.CASH_LBP.value:
                if '.' in value_str:
                    return False, "Only whole numbers accepted for LBP"
                amount = int(value_str)
            else:
                amount = float(value_str)
                
            if amount <= 0:
                return False, "Amount must be greater than zero"
                
            return True, amount
        except ValueError:
            return False, "Invalid amount format"
            
    def process_payment(self, payment_type, value_str, order_total=None):
        """Process payment after validation"""
        is_valid, result = self.validate_payment(payment_type, value_str)
        
        if not is_valid:
            return False, result, None  # Error message in result
            
        # At this point, result contains the validated amount
        payment_amount = result
        
        # Basic payment processing logic (to be expanded)
        payment_info = {
            'type': payment_type,
            'amount': payment_amount,
            'timestamp': None  # You can add timestamp later
        }
        
        return True, None, payment_info  # Success, no error message, payment info