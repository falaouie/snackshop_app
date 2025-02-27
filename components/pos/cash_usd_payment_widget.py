# components/pos/cash_usd_payment_widget.py
from .payment_option_widget import PaymentOptionWidget
from styles.payment_widgets import PaymentWidgetStyles
from button_definitions.types import PaymentButtonType

class CashUSDPaymentWidget(PaymentOptionWidget):
    """Widget for USD cash payment option"""
    
    def __init__(self, parent=None):
        super().__init__(
            payment_type=PaymentButtonType.CASH_USD.value,
            button_text="USD Cash",
            button_color="#1890ff",  # Blue base
            hover_color="#096dd9",  # Darker blue for hover
            parent=parent
        )
        
        # Set USD-specific button style
        action_config = self.layout_config.get_payment_action_button_config()
        self.payment_btn.setStyleSheet(
            PaymentWidgetStyles.get_usd_action_button_style(action_config))