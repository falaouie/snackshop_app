# components/pos/other_payment_widget.py
from .payment_option_widget import PaymentOptionWidget
from styles.payment_widgets import PaymentWidgetStyles
from button_definitions.types import PaymentButtonType

class OtherPaymentWidget(PaymentOptionWidget):
    """Widget for other payment options"""
    
    def __init__(self, parent=None):
        super().__init__(
            payment_type=PaymentButtonType.OTHER.value,
            button_text="Pay Other",
            button_color="#722ed1",  # Purple base
            hover_color="#531dab",  # Darker purple for hover
            parent=parent
        )
        
        # Set other payment-specific button style
        action_config = self.layout_config.get_payment_action_button_config()
        self.payment_btn.setStyleSheet(
            PaymentWidgetStyles.get_other_payment_button_style(action_config))