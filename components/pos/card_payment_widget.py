# components/pos/card_payment_widget.py
from .payment_option_widget import PaymentOptionWidget
from styles.payment_widgets import PaymentWidgetStyles
from button_definitions.types import PaymentButtonType

class CardPaymentWidget(PaymentOptionWidget):
    """Widget for card payment option"""
    
    def __init__(self, parent=None):
        super().__init__(
            payment_type=PaymentButtonType.CARD.value if hasattr(PaymentButtonType, 'CARD') else "CARD",
            button_text="Card Payment",
            button_color="#fa541c",  # Orange base
            hover_color="#d4380d",  # Darker orange for hover
            parent=parent
        )
        
        # Set card-specific button style
        action_config = self.layout_config.get_payment_action_button_config()
        self.payment_btn.setStyleSheet(
            PaymentWidgetStyles.get_card_payment_button_style(action_config))