# components/pos/cash_lbp_payment_widget.py
from .payment_option_widget import PaymentOptionWidget
from styles.payment_widgets import PaymentWidgetStyles
from button_definitions.types import PaymentButtonType

class CashLBPPaymentWidget(PaymentOptionWidget):
    """Widget for LBP cash payment option"""
    
    def __init__(self, parent=None):
        super().__init__(
            payment_type=PaymentButtonType.CASH_LBP.value,
            button_text="LBP Cash",
            button_color="#52c41a",  # Green base
            hover_color="#389e0d",  # Darker green for hover
            parent=parent
        )
        
        # Set LBP-specific button style
        action_config = self.layout_config.get_payment_action_button_config()
        self.payment_btn.setStyleSheet(
            PaymentWidgetStyles.get_lbp_action_button_style(action_config))