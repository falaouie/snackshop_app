# components/pos/lbp_preset_widget.py
from PyQt5.QtWidgets import QVBoxLayout, QPushButton
from .preset_payment_widget import PresetPaymentWidget
from styles.payment_widgets import PaymentWidgetStyles

class LBPPresetWidget(PresetPaymentWidget):
    """Widget for displaying LBP preset buttons with enhanced styling"""
    
    def __init__(self, parent=None):
        # LBP preset values
        preset_values = [1000, 5000, 10000, 20000, 50000, 100000]
        
        # Format function for LBP values (whole numbers with commas)
        def lbp_format(value):
            return f"{value:,}"
        
        # Custom LBP-specific style overrides
        self.style_override = {
            'normal': {
                'font-weight': 'bold',
                'color': '#52c41a'
            },
            'hover': {
                'background': '#f6ffed',
                'border-color': '#52c41a'
            }
        }
        
        super().__init__(
            currency_type="LBP",
            preset_values=preset_values,
            preset_format=lbp_format,
            parent=parent
        )
    
    def _setup_ui(self):
        """Override to apply LBP-specific styling"""
        # Get preset button config
        preset_config = self.layout_config.get_preset_button_config()
        
        # Main layout with LBP-specific margins
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
            
            # Apply button styling with LBP-specific overrides
            preset_btn.setStyleSheet(
                PaymentWidgetStyles.get_preset_button_style(
                    self.currency_type, preset_config, self.style_override))
            
            # Connect to emit the numerical value
            preset_btn.clicked.connect(lambda checked, v=preset_value: 
                                    self.preset_selected.emit(v))
            
            main_layout.addWidget(preset_btn)