# components/pos/preset_payment_widget.py
from PyQt5.QtWidgets import QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from .payment_option_widget import PaymentOptionWidget
from styles.payment_widgets import PaymentWidgetStyles

class PresetPaymentWidget(PaymentOptionWidget):
    """Widget for displaying preset denominations and payment option"""
    
    # Additional signal for preset selection
    preset_selected = pyqtSignal(float)  # Emits the selected preset amount
    
    def __init__(self, payment_type, button_text, button_color, hover_color, 
                 currency_type="USD", preset_values=None, preset_format=None, parent=None):
        # Store preset configuration before calling super()
        self.preset_values = preset_values or []
        self.preset_format = preset_format or (lambda x: f"{x}")
        self.currency_type = currency_type  # "USD" or "LBP"
        
        # Call parent constructor
        super().__init__(payment_type, button_text, button_color, hover_color, parent)
        
    def _setup_ui(self):
        """Initialize the widget UI with presets and payment button"""
        # Get configuration from layout
        preset_config = self.layout_config.get_preset_button_config()
        action_config = self.layout_config.get_payment_action_button_config()

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(preset_config['spacing'])
        
        # Create preset buttons (one per row)
        for value in self.preset_values:
            # Format the value using the provided formatter
            display_value = self.preset_format(value)
            
            btn = QPushButton(display_value)
            # Use dimensions from layout config
            btn.setFixedSize(preset_config['width'], preset_config['height'])
            # Use centralized style with currency type
            btn.setStyleSheet(PaymentWidgetStyles.get_preset_button_style(
                self.currency_type, preset_config))
            btn.clicked.connect(lambda checked, v=value: self._on_preset_clicked(v))
            main_layout.addWidget(btn)
            
        main_layout.addStretch(1)  # Add stretch to push payment button to bottom
        
        # Add payment button
        self.payment_btn = QPushButton(self.button_text)
        # Use dimensions from layout config
        self.payment_btn.setFixedSize(action_config['width'], action_config['height'])
        # Use centralized style - the appropriate style will be set by derived classes
        self.payment_btn.clicked.connect(self._on_payment_requested)
        main_layout.addWidget(self.payment_btn)
        
    def _on_preset_clicked(self, value):
        """Handle preset button click"""
        self.preset_selected.emit(value)