# usd_preset_widget.py - Updated Version
from .preset_payment_widget import PresetPaymentWidget
from button_definitions.types import PaymentButtonType

class USDPresetWidget(PresetPaymentWidget):
    """Widget for displaying USD preset buttons and payment option"""
    
    def __init__(self, parent=None):
        # USD preset values
        preset_values = [1, 5, 10, 20, 50, 100]
        
        # Format function for USD values
        def usd_format(value):
            return f"${value:.2f}"
        
        super().__init__(
            payment_type=PaymentButtonType.CASH_USD.value,
            button_text="USD Cash",
            button_color="#1890ff",  # Blue
            hover_color="#096dd9",   # Darker blue
            preset_values=preset_values,
            preset_format=usd_format,
            parent=parent
        )
        
        # Customize button styles if needed
        self.payment_btn.setStyleSheet("""
            QPushButton {
                background: #e6f7ff;
                color: #1890ff;
                border: 2px solid #1890ff;
                border-radius: 5px;
                padding: 8px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #bae7ff;
            }
        """)