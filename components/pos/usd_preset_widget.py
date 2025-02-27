# components/pos/usd_preset_widget.py
from PyQt5.QtWidgets import QVBoxLayout, QPushButton
from .preset_payment_widget import PresetPaymentWidget
from styles.payment_widgets import PaymentWidgetStyles

class USDPresetWidget(PresetPaymentWidget):
    """Widget for displaying USD preset buttons with enhanced styling"""
    
    def __init__(self, parent=None):
        # USD preset values
        preset_values = [1, 5, 10, 20, 50, 100]
        
        # Format function for USD values
        def usd_format(value):
            return f"${value:.2f}"
        
        # Custom USD-specific style overrides could be added here
        self.style_override = {
            'normal': {
                'font-weight': 'bold',
                'color': '#1890ff'
            },
            'hover': {
                'background': '#e6f7ff',
                'border-color': '#1890ff'
            }
        }
        
        super().__init__(
            currency_type="USD",
            preset_values=preset_values,
            preset_format=usd_format,
            parent=parent
        )
    
    def _setup_ui(self):
        """Override to apply USD-specific styling"""
        # Get preset button config
        preset_config = self.layout_config.get_preset_button_config()
        
        # Main layout with USD-specific margins
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            preset_config.get('margin_left', 5),
            preset_config.get('margin_top', 5),
            preset_config.get('margin_right', 5),
            preset_config.get('margin_bottom', 5)
        )
        main_layout.setSpacing(preset_config['spacing'])
        
        # Add one preset value per row
        for preset_value in self.preset_values:
            preset_btn = QPushButton(self.preset_format(preset_value))
            
            # Apply button sizing
            preset_btn.setFixedHeight(preset_config['height'])
            if 'width' in preset_config:
                preset_btn.setFixedWidth(preset_config['width'])
            
            # Apply button styling with USD-specific overrides
            preset_btn.setStyleSheet(
                PaymentWidgetStyles.get_preset_button_style(
                    self.currency_type, preset_config, self.style_override))
            
            # Connect to emit the numerical value
            preset_btn.clicked.connect(lambda checked, v=preset_value: 
                                    self.preset_selected.emit(v))
            
            main_layout.addWidget(preset_btn)