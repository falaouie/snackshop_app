from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from styles import ButtonStyles
from styles.layouts import layout_config
from button_definitions.types import PaymentButtonType
from button_definitions.payment import PaymentButtonConfig
from components.numpad.types import NumpadMode 

class PaymentButtonsWidget(QFrame):
    """Widget for managing payment buttons"""
    
    # Signals
    action_triggered = pyqtSignal(str)  # Emits the triggered action type
    currency_mode_changed = pyqtSignal(object)  # Emits the NumpadMode
    
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
                
                # Connect button handlers
                btn.clicked.connect(
                    lambda checked, type=button_type.value: self._handle_action_triggered(type)
                )
                
                # Connect mode change handlers
                if button_type == PaymentButtonType.CASH_USD:
                    btn.clicked.connect(lambda: self.currency_mode_changed.emit(NumpadMode.USD))
                    btn.clicked.connect(self.process_cash_usd_payment)
                elif button_type == PaymentButtonType.CASH_LBP:
                    btn.clicked.connect(lambda: self.currency_mode_changed.emit(NumpadMode.LBP))
                    btn.clicked.connect(self.process_cash_lbp_payment)
                elif button_type == PaymentButtonType.OTHER:
                    btn.clicked.connect(self.process_other_payment)
                
                # Store button reference
                self.payment_buttons[button_type.value] = btn
                layout.addWidget(btn)

    def _handle_action_triggered(self, action_type):
        """Handle button action trigger"""
        self.action_triggered.emit(action_type)

    # Temporary test methods
    def process_cash_usd_payment(self):
        """Handle USD cash payment"""
        print("CASH USD button clicked")

    def process_cash_lbp_payment(self):
        """Handle LBP cash payment"""
        print("CASH LBP button clicked")

    def process_other_payment(self):
        """Handle other payment types"""
        print("Other Payment button clicked")
        # Reset to QTY mode
        self.currency_mode_changed.emit(NumpadMode.QTY) # remove later