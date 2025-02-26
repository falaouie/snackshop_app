# payment_option_widget.py - Updated version
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from styles.layouts import layout_config

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
        self.setStyleSheet("QFrame { background: white; border: 1px solid #dddddd; border-radius: 5px; }")
        # IMPORTANT: We've moved this to the end to ensure derived classes have initialized their attributes
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
        
        self.payment_btn.setStyleSheet(f"""
            QPushButton {{
                background: {self.button_color};
                color: white;
                border: none;
                border-radius: {action_config['radius']}px;
                padding: {action_config['padding']}px;
                font-size: {action_config['font_size']}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {self.hover_color};
            }}
        """)
        self.payment_btn.clicked.connect(self._on_payment_requested)
        main_layout.addWidget(self.payment_btn)
        
    def _on_payment_requested(self):
        """Handle payment button click"""
        self.payment_requested.emit(self.payment_type)