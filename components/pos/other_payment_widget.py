from .payment_option_widget import PaymentOptionWidget

class OtherPaymentWidget(PaymentOptionWidget):
    """Widget for other payment options"""
    
    def __init__(self, parent=None):
        super().__init__(
            payment_type="OTHER",
            button_text="Pay Other",
            button_color="#722ed1",  # Purple base
            hover_color="#531dab",  # Darker purple for hover
            parent=parent
        )