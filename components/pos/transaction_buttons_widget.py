from PyQt5.QtWidgets import QFrame, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from styles import ButtonStyles
from styles.layouts import layout_config
from styles.transaction_widgets import TransactionWidgetStyles
from button_definitions.types import TransactionButtonType
from button_definitions.transaction import TransactionButtonConfig

class TransactionButtonsWidget(QFrame):
    """Widget for managing transaction buttons in the vertical section"""
    
    # Signals
    action_triggered = pyqtSignal(str)  # Emits the triggered action type
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_config = layout_config.get_instance()
        self.transaction_buttons = {}  # Store buttons for reference
        
        # Use centralized container style
        self.setStyleSheet(TransactionWidgetStyles.CONTAINER)
        
        self._setup_ui()

    def _setup_ui(self):
        """Initialize the transaction buttons UI"""
        # Get layout configuration from styles
        layout_values = TransactionWidgetStyles.get_layout_config(self.layout_config)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(*layout_values['margins'])
        main_layout.setSpacing(layout_values['spacing'])
        
        self._create_buttons(main_layout)
        main_layout.addStretch()  # Add stretch at the end

    def _create_buttons(self, layout):
        """Create transaction buttons"""
        button_config = self.layout_config.get_button_config('transaction')
        
        for button_type in TransactionButtonType:
            config = TransactionButtonConfig.get_config(button_type)
            if config:  # Only create button if config exists
                btn = QPushButton(config['text'])
                
                # Use centralized button style
                btn.setStyleSheet(ButtonStyles.get_transaction_button_style(button_type))
                
                # Use dimensions from layout config
                btn.setFixedSize(
                    button_config['width'],
                    button_config['height']
                )
                
                # Connect button handlers
                btn.clicked.connect(
                    lambda checked, type=button_type.value: self._handle_action_triggered(type)
                )
                
                # Connect specific action if defined
                if config.get('action'):
                    btn.clicked.connect(getattr(self, config['action']))
                
                # Store button reference
                self.transaction_buttons[button_type.value] = btn
                layout.addWidget(btn)

    def _handle_action_triggered(self, action_type):
        """Handle button action trigger"""
        self.action_triggered.emit(action_type)

    # Action handlers
    def hold_transaction(self):
        """Handle hold transaction"""
        print("Hold transaction button clicked")

    def void_transaction(self):
        """Handle void transaction"""
        print("Void transaction button clicked")

    def paid_in(self):
        """Handle paid in"""
        print("Paid in button clicked")

    def paid_out(self):
        """Handle paid out"""
        print("Paid out button clicked")

    def no_sale(self):
        """Handle no sale"""
        print("Vertical No Sale button clicked")

    def apply_discount(self):
        """Handle discount"""
        print("Discount button clicked")

    def show_numpad(self):
        """Show numpad"""
        print("Num pad button clicked")