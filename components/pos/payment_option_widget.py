# components/pos/payment_option_widget.py
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from styles.layouts import layout_config
from styles.payment_widgets import PaymentWidgetStyles

class PaymentOptionWidget(QFrame):
    """Base widget for payment option buttons"""
    
    # Signal
    payment_requested = pyqtSignal(str)  # Emits the payment type
    
    def __init__(self, payment_type, button_text, button_color, hover_color, parent=None):
        super().__init__(parent)
        self.layout_config = layout_config.get_instance()
        self.payment_type = payment_type
        self.button_text = button_text
        self.button_color = button_color
        self.hover_color = hover_color
        # Use the centralized container style
        self.setStyleSheet(PaymentWidgetStyles.get_container_style())
        # Initialize UI at the end to ensure derived classes have set their attributes
        self._init_ui()

    def _init_ui(self):
        """Initialize UI after constructor chain is complete"""
        self._setup_ui()
        
    def _setup_ui(self):
        """Initialize the widget UI"""
        # Get configuration
        action_config = self.layout_config.get_payment_action_button_config()

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Add payment button that fills the widget
        self.payment_btn = QPushButton(self.button_text)
        # Use dimensions from layout config
        self.payment_btn.setFixedSize(action_config['width'], action_config['height'])
        # Use centralized style system
        self.payment_btn.setStyleSheet(PaymentWidgetStyles.get_payment_action_button_style(
            self.payment_type, self.button_color, self.hover_color, action_config))
        self.payment_btn.clicked.connect(self._on_payment_requested)
        main_layout.addWidget(self.payment_btn)
        
    def _on_payment_requested(self):
        """Handle payment button click"""
        self.payment_requested.emit(self.payment_type)