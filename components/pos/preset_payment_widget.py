# Modified preset_payment_widget.py
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import pyqtSignal
from styles.layouts import layout_config
from styles.payment_widgets import PaymentWidgetStyles

class PresetPaymentWidget(QFrame):
    """Base widget for preset payment options with enhanced styling control"""
    
    # Signal
    preset_selected = pyqtSignal(float)  # Emits the selected preset amount
    
    def __init__(self, currency_type=None, preset_values=None, 
                 preset_format=None, parent=None):
        super().__init__(parent)
        self.layout_config = layout_config.get_instance()
        self.currency_type = currency_type
        self.preset_values = preset_values or []
        self.preset_format = preset_format or (lambda x: str(x))
        
        # Use the centralized container style
        self.setStyleSheet(PaymentWidgetStyles.get_payment_container_style())
        
        # Apply widget level sizing constraints
        preset_config = self.layout_config.get_preset_button_config()
        if 'widget_width' in preset_config:
            self.setFixedWidth(preset_config['widget_width'])
        
        # Set size policy to respect fixed size but expand as needed
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        # Initialize UI
        self._setup_ui()
        
    def _setup_ui(self):
        """Initialize the widget UI"""
        # Get preset button config
        preset_config = self.layout_config.get_preset_button_config()
        
        # Main layout
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
            
            # Apply button styling
            preset_btn.setStyleSheet(
                PaymentWidgetStyles.get_preset_button_style(
                    self.currency_type, preset_config))
            
            # Connect to emit the numerical value
            preset_btn.clicked.connect(lambda checked, v=preset_value: 
                                    self.preset_selected.emit(v))
            
            main_layout.addWidget(preset_btn)