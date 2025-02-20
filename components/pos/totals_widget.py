from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal
from styles import POSStyles, ButtonStyles
from styles.layouts import layout_config
from button_definitions.types import OrderButtonType
from button_definitions.order_type import OrderTypeButtonConfig

class TotalsWidget(QFrame):
    """Widget for displaying order totals and order type buttons"""
    
    # Signals
    order_type_changed = pyqtSignal(str)  # Emits the selected order type
    
    def __init__(self, exchange_rate, parent=None):
        super().__init__(parent)
        self.layout_config = layout_config.get_instance()
        self.exchange_rate = exchange_rate
        self.selected_order_type = None  # Track selected order type
        self.order_buttons = {}  # Store buttons for reference
        self.setStyleSheet(POSStyles.TOTALS_FRAME)
        self._setup_ui()

    def _setup_ui(self):
        """Initialize the totals widget UI"""
        # Main horizontal layout
        totals_layout = QHBoxLayout(self)
        totals_layout.setContentsMargins(15, 10, 15, 10)
        totals_layout.setSpacing(20)

        # Order Type Buttons Section (Left)
        totals_layout.addWidget(self._create_order_buttons())
        totals_layout.addStretch(1)
        
        # Amounts Section (Right)
        totals_layout.addWidget(self._create_amounts_section())

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
            order_buttons_layout.addWidget(btn)

            # Set initial selection for default button
            if config.get('default_selected', False):
                self._handle_order_type_selection(button_type.value)
        
        return order_buttons_container
    
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

    def _create_amounts_section(self):
        """Create amounts display section"""
        amounts_container = QFrame()
        amounts_layout = QVBoxLayout(amounts_container)
        amounts_layout.setContentsMargins(0, 0, 0, 0)
        amounts_layout.setSpacing(4)
        
        # USD Total
        usd_layout = QHBoxLayout()
        self.usd_amount = QLabel("$0.00")
        self.usd_amount.setProperty("class", "currency-usd")
        usd_layout.addStretch()
        usd_layout.addWidget(self.usd_amount)
        
        # LBP Total
        lbp_layout = QHBoxLayout()
        self.lbp_amount = QLabel("LBP 000")
        self.lbp_amount.setProperty("class", "currency-lbp")
        lbp_layout.addStretch()
        lbp_layout.addWidget(self.lbp_amount)
        
        amounts_layout.addLayout(usd_layout)
        amounts_layout.addLayout(lbp_layout)
        
        return amounts_container

    def update_totals(self, amount_usd):
        """Update total amounts in both currencies"""
        total_lbp = amount_usd * self.exchange_rate
        
        self.usd_amount.setText(f"${amount_usd:.2f}")
        self.lbp_amount.setText(f"LBP {total_lbp:,.0f}")

    def set_exchange_rate(self, rate):
        """Update the exchange rate and recalculate totals"""
        self.exchange_rate = rate
        # Force update with current USD amount
        current_usd = float(self.usd_amount.text().replace('$', ''))
        self.update_totals(current_usd)

    def set_dine_in(self):
        """Handle dine in button click"""
        print("Dine In Button Clicked")

    def set_take_away(self):
        """Handle take away button click"""
        print("Take-Away Button Clicked")

    def set_delivery(self):
        """Handle delivery button click"""
        print("Delivery Button Clicked")