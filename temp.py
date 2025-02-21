# In POSView class

def __init__(self, user_id, parent=None):
    super().__init__(parent)
    self.user_id = user_id
    self.layout_config = layout_config.get_instance()
    self.exchange_rate = 90000
    self.prices = PRODUCT_PRICES 
    self.keyboard = VirtualKeyboard(self)
    self.pending_quantity = None  # Track pending quantity from numpad
    
    self.timer = QTimer(self)
    self.timer.timeout.connect(self._update_time)
    self.timer.start(1000)
    
    self.transaction_buttons = None
    
    self._setup_ui()
    self._update_time()

def _create_products_widget(self):
    """Create products panel with numpad integration"""
    # ... existing code until numpad creation ...

    # Create numpad widget
    self.numpad_widget = NumpadWidget(self)
    # Connect to track value changes
    self.numpad_widget.display.textChanged.connect(self._handle_numpad_value_change)
    intermediate_layout.addWidget(self.numpad_widget)

    # ... rest of existing code ...

def _handle_numpad_value_change(self, value: str):
    """Handle numpad value changes"""
    try:
        # Clean the value (remove formatting)
        clean_value = value.replace(',', '')
        # Only update pending quantity if it's a valid number and in QTY mode
        if self.numpad_widget.current_mode == NumpadMode.QTY:
            self.pending_quantity = int(clean_value) if clean_value != '0' else None
        else:
            self.pending_quantity = None
    except ValueError:
        self.pending_quantity = None

def _handle_product_click(self, item_name):
    """Handle product button click with quantity support"""
    quantity = 1  # Default quantity
    
    # Use pending quantity if available
    if self.pending_quantity is not None:
        quantity = self.pending_quantity
        # Reset numpad and pending quantity
        self.numpad_widget._on_clear()
        self.pending_quantity = None
    
    # Add item with quantity
    self.order_list.add_item(item_name, self.prices.get(item_name, 0))
    
    # If quantity > 1, add additional quantities
    for _ in range(quantity - 1):
        self.order_list.add_item(item_name, self.prices.get(item_name, 0))
    
    self._update_totals()
    self.search_input.clear_search()