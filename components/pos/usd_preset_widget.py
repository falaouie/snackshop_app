# components/pos/usd_preset_widget.py
from .preset_payment_widget import PresetPaymentWidget
from button_definitions.types import PaymentButtonType
from styles.payment_widgets import PaymentWidgetStyles

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
            currency_type="USD",
            preset_values=preset_values,
            preset_format=usd_format,
            parent=parent
        )
        
        # Set USD-specific button style
        action_config = self.layout_config.get_payment_action_button_config()
        self.payment_btn.setStyleSheet(
            PaymentWidgetStyles.get_usd_action_button_style(action_config))