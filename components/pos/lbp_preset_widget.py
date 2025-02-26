# components/pos/lbp_preset_widget.py
from .preset_payment_widget import PresetPaymentWidget
from button_definitions.types import PaymentButtonType
from styles.payment_widgets import PaymentWidgetStyles

class LBPPresetWidget(PresetPaymentWidget):
    """Widget for displaying LBP preset buttons and payment option"""
    
    def __init__(self, parent=None):
        # LBP preset values
        preset_values = [1000, 5000, 10000, 20000, 50000, 100000]
        
        # Format function for LBP values (whole numbers with commas)
        def lbp_format(value):
            return f"{value:,}"
        
        super().__init__(
            payment_type=PaymentButtonType.CASH_LBP.value,
            button_text="LBP Cash",
            button_color="#52c41a",  # Green
            hover_color="#389e0d",   # Darker green
            currency_type="LBP",     # Use LBP currency type for styling
            preset_values=preset_values,
            preset_format=lbp_format,
            parent=parent
        )
        
        # Set LBP-specific button style
        action_config = self.layout_config.get_payment_action_button_config()
        self.payment_btn.setStyleSheet(
            PaymentWidgetStyles.get_lbp_action_button_style(action_config))