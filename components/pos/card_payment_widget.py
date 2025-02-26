from .payment_option_widget import PaymentOptionWidget

class CardPaymentWidget(PaymentOptionWidget):
    """Widget for card payment option"""
    
    def __init__(self, parent=None):
        super().__init__(
            payment_type="CARD",  
            button_text="Card Payment",
            button_color="#fa541c",  # Orange base
            hover_color="#d4380d",  # Darker orange for hover
            parent=parent
        )