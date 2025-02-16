from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
from styles.layouts import layout_config
from .digit_box import DigitBox

class UserInput(QWidget):
    """A widget containing multiple digit boxes for PIN/ID input"""
    
    # Signal to emit when input changes - this remains unchanged
    input_changed = pyqtSignal(list)
    
    def __init__(self, is_pin=False):
        """Initialize the UserInput widget
        
        Args:
            is_pin (bool): Whether this input is for a PIN (masks input) or ID
        """
        super().__init__()
        self.is_pin = is_pin
        self.digits = ["", "", "", ""]  # Track input digits
        self.current_position = 0       # Current digit being edited
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the user interface with digit boxes in a horizontal layout"""
        # Create horizontal layout
        layout = QHBoxLayout()
        
        # Get the layout configuration instance
        config = layout_config.get_instance()
        
        # Get spacing configuration from layout_config
        spacing_config = config.get_spacing_config()
        
        # Set margins and spacing using values from layout config
        # Note: We're using container_margin and section_spacing from the config
        margin = spacing_config['container_margin']
        spacing = spacing_config['section_spacing']
        
        # Set the layout margins - only top and bottom margins are set
        layout.setContentsMargins(0, margin//2, 0, margin//2)
        
        # Set the spacing between digit boxes
        layout.setSpacing(spacing)
        
        # Create and add digit boxes
        self.digit_boxes = []
        for _ in range(4):  # Create 4 digit boxes
            box = DigitBox(is_pin=self.is_pin)
            self.digit_boxes.append(box)
            layout.addWidget(box)
            
        # Set the layout for this widget
        self.setLayout(layout)
        
    def add_digit(self, digit):
        """Add a digit to the input at the current position
        
        Args:
            digit (str): The digit to add
        """
        if self.current_position < 4:
            self.digits[self.current_position] = digit
            self.digit_boxes[self.current_position].update_digit(digit)
            self.current_position += 1
            self.input_changed.emit(self.digits)
            
    def remove_digit(self):
        """Remove the last entered digit"""
        if self.current_position > 0:
            self.current_position -= 1
            self.digits[self.current_position] = ""
            self.digit_boxes[self.current_position].update_digit("")
            self.input_changed.emit(self.digits)
            
    def clear_all(self):
        """Clear all entered digits"""
        self.digits = ["", "", "", ""]
        self.current_position = 0
        for box in self.digit_boxes:
            box.update_digit("")
        self.input_changed.emit(self.digits)
        
    def has_digits(self):
        """Check if any digits are entered
        
        Returns:
            bool: True if any digits are entered, False otherwise
        """
        return any(self.digits)
        
    def is_complete(self):
        """Check if all 4 digits are entered
        
        Returns:
            bool: True if all digits are entered, False otherwise
        """
        return all(self.digits)