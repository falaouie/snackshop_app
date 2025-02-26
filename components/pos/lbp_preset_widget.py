# lbp_preset_widget.py - Updated Version
from .preset_payment_widget import PresetPaymentWidget
from button_definitions.types import PaymentButtonType

class LBPPresetWidget(PresetPaymentWidget):
    """Widget for displaying LBP preset buttons and payment option"""
    
    def __init__(self, parent=None):
        # LBP preset values
        preset_values = [1000, 5000, 10000, 20000, 50000, 100000]
        
        # Format function for LBP values
        def lbp_format(value):
            return f"{value:,}"
        
        super().__init__(
            payment_type=PaymentButtonType.CASH_LBP.value,
            button_text="LBP Cash",
            button_color="#52c41a",  # Green
            hover_color="#389e0d",   # Darker green
            preset_values=preset_values,
            preset_format=lbp_format,
            parent=parent
        )
        
        # Customize button styles if needed
        self.payment_btn.setStyleSheet("""
            QPushButton {
                background: #f6ffed;
                color: #52c41a;
                border: 2px solid #52c41a;
                border-radius: 5px;
                padding: 8px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #d9f7be;
            }
        """)