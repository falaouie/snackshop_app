from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal
from styles import POSStyles, ButtonStyles
from styles.layouts import layout_config
from button_definitions.types import OrderButtonType
from button_definitions.order_type import OrderTypeButtonConfig

class TotalsWidget(QFrame):
    order_type_changed = pyqtSignal(str)
    
    def __init__(self, exchange_rate, parent=None):
        super().__init__(parent)
        self.layout_config = layout_config.get_instance()
        self.exchange_rate = exchange_rate
        self.selected_order_type = None  # Track selected order type
        self.order_buttons = {}  # Store buttons for reference
        self.setStyleSheet(POSStyles.TOTALS_FRAME)
        self._setup_ui()

    def _create_order_buttons(self):
        """Create order type buttons section"""
        order_buttons_container = QFrame()
        order_buttons_layout = QHBoxLayout(order_buttons_container)
        order_buttons_layout.setContentsMargins(0, 0, 0, 0)
        order_buttons_layout.setSpacing(10)

        button_config = self.layout_config.get_button_config('order_type')

        # Create buttons for each order type
        for button_type in OrderButtonType:
            config = OrderTypeButtonConfig.get_config(button_type)
            btn = QPushButton(config['text'])
            btn.setFixedSize(
                button_config['width'],
                button_config['height']
            )
            # Remove setCheckable - we'll handle selection manually
            btn.clicked.connect(
                lambda checked, type=button_type.value: self._handle_order_type_selection(type)
            )
            
            # Store button reference
            self.order_buttons[button_type.value] = btn
            order_buttons_layout.addWidget(btn)

            # Set initial selection for default button
            if config.get('default_selected', False):
                self._handle_order_type_selection(button_type.value)
        
        return order_buttons_container

    def _handle_order_type_selection(self, order_type):
        """Handle order type button selection"""
        # Reset previous selection
        if self.selected_order_type:
            prev_btn = self.order_buttons[self.selected_order_type]
            prev_btn.setStyleSheet(ButtonStyles.get_order_button_style(is_selected=False))

        # Update new selection
        curr_btn = self.order_buttons[order_type]
        curr_btn.setStyleSheet(ButtonStyles.get_order_button_style(is_selected=True))
        
        self.selected_order_type = order_type
        self.order_type_changed.emit(order_type)