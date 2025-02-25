from components.numpad.types import NumpadMode, NumpadValidation
from button_definitions.types import PaymentButtonType

class ValidationService:
    """Centralized service for validation rules across the application"""
    
    def __init__(self):
        self.validation_rules = NumpadValidation.RULES
    
    def validate_input(self, value: str, mode: NumpadMode):
        """Validate input based on mode and specific rules"""
        rules = self.validation_rules.get(mode, {})
        
        # Check for empty input
        if not value or value == '0':
            return False, "Value is required"
            
        # Check decimal point rule
        if '.' in value and not rules.get('allow_decimal', True):
            return False, f"Decimal values not allowed for this input"
            
        # Check numeric format
        try:
            if rules.get('allow_decimal', True):
                number = float(value)
            else:
                number = int(value)
        except ValueError:
            return False, "Invalid number format"
            
        # Check minimum value
        min_value = rules.get('min_value', None)
        if min_value is not None and number < min_value:
            return False, f"Value must be at least {min_value}"
            
        # Check maximum value
        max_value = rules.get('max_value', None)
        if max_value is not None and number > max_value:
            return False, f"Value cannot exceed {max_value}"
            
        return True, None
    
    def validate_payment_input(self, payment_type: str, value: str):
        """Validate payment input based on payment type"""
        # Map payment types to validation modes
        mode_map = {
            PaymentButtonType.CASH_USD.value: NumpadMode.USD,
            PaymentButtonType.CASH_LBP.value: NumpadMode.LBP,
            PaymentButtonType.OTHER.value: NumpadMode.USD  # Default to USD rules for other
        }
        
        mode = mode_map.get(payment_type, NumpadMode.DEFAULT)
        return self.validate_input(value, mode)
    
    def validate_product_quantity(self, value: str):
        """Validate product quantity input"""
        return self.validate_input(value, NumpadMode.QTY)