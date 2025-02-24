from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from styles import ButtonStyles
from styles.layouts import layout_config
from button_definitions.types import PaymentButtonType
from button_definitions.payment import PaymentButtonConfig

class PaymentButtonsWidget(QFrame):
    """Widget for managing payment buttons"""
    
    # Signals
    action_triggered = pyqtSignal(str)  # Emits the triggered action type
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_config = layout_config.get_instance()
        self.payment_buttons = {}  # Store buttons for reference
        self._setup_ui()

    def _setup_ui(self):
        """Initialize the payment buttons UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(6)
        
        self._create_buttons(main_layout)

    def _create_buttons(self, layout):
        """Create payment buttons"""
        button_config = self.layout_config.get_button_config('payment')
        
        for button_type in PaymentButtonType:
            config = PaymentButtonConfig.get_config(button_type)
            if config:  # Only create button if config exists
                btn = QPushButton(config['text'])
                btn.setStyleSheet(ButtonStyles.get_payment_button_style(button_type))
                btn.setFixedSize(
                    button_config['width'],
                    button_config['height']
                )
                
                # Connect button handler - simplified for Phase 1
                btn.clicked.connect(
                    lambda checked, type=button_type.value: self._handle_action_triggered(type)
                )
                
                # Store button reference
                self.payment_buttons[button_type.value] = btn
                layout.addWidget(btn)

    def _handle_action_triggered(self, action_type):
        """Handle button action trigger"""
        self.action_triggered.emit(action_type)

    # Payment processing methods will be implemented in future phases
    def process_cash_usd_payment(self):
        """Handle USD cash payment - placeholder"""
        pass

    def process_cash_lbp_payment(self):
        """Handle LBP cash payment - placeholder"""
        pass

    def process_other_payment(self):
        """Handle other payment types - placeholder"""
        pass