from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from styles import ButtonStyles
from styles.layouts import layout_config
from button_definitions.types import OrderButtonType
from button_definitions.order_type import OrderTypeButtonConfig

class OrderTypeWidget(QFrame):
    """Widget for managing order type selection buttons"""
    
    # Signals
    order_type_changed = pyqtSignal(str)  # Emits the selected order type
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_config = layout_config.get_instance()
        self.selected_order_type = None  # Track selected order type
        self.order_buttons = {}  # Store buttons for reference
        self._setup_ui()

    def _setup_ui(self):
        """Initialize the order type buttons UI"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        
        self._create_order_buttons(main_layout)

    def _create_order_buttons(self, layout):
        """Create order type buttons"""
        button_config = self.layout_config.get_button_config('order_type')

        for button_type in OrderButtonType:
          
            config = OrderTypeButtonConfig.get_config(button_type)
            btn = QPushButton(config['text'])
            btn.setFixedSize(
                button_config['width'],
                button_config['height']
            )
            
            # Set initial style
            btn.setStyleSheet(ButtonStyles.get_order_button_style(is_selected=False))
            
            # Connect selection handler
            btn.clicked.connect(
                lambda checked, type=button_type.value: self._handle_order_type_selection(type)
            )
            
            # Connect action handler using config
            if config.get('action'):
                btn.clicked.connect(getattr(self, config['action']))
            
            # Store button reference
            self.order_buttons[button_type.value] = btn
            layout.addWidget(btn)

            # Set initial selection for default button
            if config.get('default_selected', False):
                self._handle_order_type_selection(button_type.value)

    def _handle_order_type_selection(self, order_type):
        """Handle order type button selection"""
        # Reset previous selection if exists
        if self.selected_order_type:
            prev_btn = self.order_buttons[self.selected_order_type]
            prev_btn.setStyleSheet(ButtonStyles.get_order_button_style(is_selected=False))

        # Update new selection
        curr_btn = self.order_buttons[order_type]
        curr_btn.setStyleSheet(ButtonStyles.get_order_button_style(is_selected=True))
        
        self.selected_order_type = order_type
        self.order_type_changed.emit(order_type)

    # Button click handlers
    def set_dine_in(self):
        """Handle dine in button click"""
        print("Dine In Button Clicked")

    def set_take_away(self):
        """Handle take away button click"""
        print("Take-Away Button Clicked")

    def set_delivery(self):
        """Handle delivery button click"""
        print("Delivery Button Clicked")