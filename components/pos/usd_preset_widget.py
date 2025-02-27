# components/pos/usd_preset_widget.py
from .preset_payment_widget import PresetPaymentWidget

class USDPresetWidget(PresetPaymentWidget):
    """Widget for displaying USD preset buttons"""
    
    def __init__(self, parent=None):
        # USD preset values
        preset_values = [1, 5, 10, 20, 50, 100]
        
        # Format function for USD values
        def usd_format(value):
            return f"${value:.2f}"
        
        super().__init__(
            currency_type="USD",
            preset_values=preset_values,
            preset_format=usd_format,
            parent=parent
        )