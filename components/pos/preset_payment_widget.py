# preset_payment_widget.py - Updated initialization
from PyQt5.QtWidgets import QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from .payment_option_widget import PaymentOptionWidget

class PresetPaymentWidget(PaymentOptionWidget):
    """Widget for displaying preset denominations and payment option"""
    
    # Additional signal for preset selection
    preset_selected = pyqtSignal(float)  # Emits the selected preset amount
    
    def __init__(self, payment_type, button_text, button_color, hover_color, 
                 preset_values=None, preset_format=None, parent=None):
        # Store preset configuration 
        self.preset_values = preset_values or []
        self.preset_format = preset_format or (lambda x: f"{x}")
        
        # Call parent constructor - now safe because _setup_ui won't be called until _init_ui
        super().__init__(payment_type, button_text, button_color, hover_color, parent)
        
    def _setup_ui(self):
        """Initialize the widget UI with presets and payment button"""
        # Get configuration
        preset_config = self.layout_config.get_preset_button_config()
        action_config = self.layout_config.get_payment_action_button_config()

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Create preset buttons (one per row)
        for value in self.preset_values:
            # Format the value using the provided formatter
            display_value = self.preset_format(value)
            
            btn = QPushButton(display_value)
            btn.setFixedSize(preset_config['width'], preset_config['height'])
            btn.setStyleSheet("""
                QPushButton {
                    background: white;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: #f0f0f0;
                    border-color: #1890ff;
                }
            """)
            btn.clicked.connect(lambda checked, v=value: self._on_preset_clicked(v))
            main_layout.addWidget(btn)
            
        main_layout.addStretch(1)  # Add stretch to push payment button to bottom
        
        # Add payment button
        self.payment_btn = QPushButton(self.button_text)
        self.payment_btn.setFixedSize(action_config['width'], action_config['height'])
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
        
    def _on_preset_clicked(self, value):
        """Handle preset button click"""
        self.preset_selected.emit(value)