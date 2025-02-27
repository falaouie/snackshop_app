# components/pos/lbp_preset_widget.py
from .preset_payment_widget import PresetPaymentWidget

class LBPPresetWidget(PresetPaymentWidget):
    """Widget for displaying LBP preset buttons"""
    
    def __init__(self, parent=None):
        # LBP preset values
        preset_values = [1000, 5000, 10000, 20000, 50000, 100000]
        
        # Format function for LBP values (whole numbers with commas)
        def lbp_format(value):
            return f"{value:,}"
        
        super().__init__(
            currency_type="LBP",
            preset_values=preset_values,
            preset_format=lbp_format,
            parent=parent
        )