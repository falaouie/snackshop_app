from typing import Optional, Set
from .types import NumpadMode, NumpadState, NumpadValidation

class NumpadManager:
    """Manager for numpad state and interactions"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NumpadManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the numpad manager"""
        self.current_numpad = None
        self.current_input = None
        self.current_mode = NumpadMode.QTY
        self.current_state = NumpadState.STANDALONE
        self.registered_inputs: Set = set()

    def register_numpad(self, numpad) -> None:
        """Register a numpad instance"""
        self.current_numpad = numpad

    def register_input(self, input_widget) -> None:
        """
        Register an input field for future input-bound mode
        Future: Will handle input field registration for bound mode
        """
        self.registered_inputs.add(input_widget)

    def unregister_input(self, input_widget) -> None:
        """
        Unregister an input field
        Future: Will handle input field cleanup for bound mode
        """
        if input_widget in self.registered_inputs:
            self.registered_inputs.remove(input_widget)

    def validate_input(self, value: str, mode: NumpadMode) -> bool:
        """
        Validate input based on current mode
        
        Args:
            value: The value to validate
            mode: The mode to validate against
            
        Returns:
            bool: True if valid, False otherwise
        """
        rules = NumpadValidation.RULES.get(mode, {})
        
        try:
            # Handle empty input
            if not value or value == '.':
                return True

            # Convert to proper type
            num_value = float(value) if '.' in value else int(value)
            
            # Check decimal allowance
            if not rules.get('allow_decimal', True) and '.' in value:
                return False
                
            # Check min/max values
            if num_value < rules.get('min_value', float('-inf')):
                return False
            if num_value > rules.get('max_value', float('inf')):
                return False
                
            # Check decimal places
            if '.' in value and rules.get('decimal_places'):
                decimal_places = len(value.split('.')[1])
                if decimal_places > rules['decimal_places']:
                    return False
                    
            return True
            
        except ValueError:
            return False

    def format_value(self, value: str, mode: NumpadMode) -> str:
        """
        Format value based on mode
        
        Args:
            value: The value to format
            mode: The mode to format for
            
        Returns:
            str: Formatted value
        """
        if not value:
            return "0"
            
        rules = NumpadValidation.RULES.get(mode, {})
        
        try:
            num_value = float(value) if '.' in value else int(value)
            
            if mode == NumpadMode.USD:
                return f"{num_value:.2f}"
            elif mode == NumpadMode.WGT:
                return f"{num_value:.3f}"
            elif mode in (NumpadMode.QTY, NumpadMode.LBP):
                return str(int(num_value))
            
            return value
            
        except ValueError:
            return "0"