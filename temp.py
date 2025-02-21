def _handle_product_click(self, item_name):
    """Handle product button click with quantity support"""
    # Check if item exists in order list
    existing_item = self._find_existing_item(item_name)
    
    # Get quantity from numpad if available, else default to 1
    new_quantity = self.pending_quantity if self.pending_quantity is not None else 1
    
    if existing_item and new_quantity > 0:
        # Show quantity decision dialog
        self._show_quantity_dialog(item_name, existing_item.quantity, new_quantity)
    else:
        # Process new item normally
        self._add_product_with_quantity(item_name, new_quantity)

def _find_existing_item(self, item_name):
    """Find an existing item in the order list"""
    for item in self.order_list.order_items:
        if item.name == item_name:
            return item
    return None

def _show_quantity_dialog(self, item_name, current_qty, new_qty):
    """Show dialog for quantity decision"""
    msg_box = QMessageBox(self)
    msg_box.setWindowTitle('Update Quantity')
    msg_box.setText(f"{item_name} exists with quantity {current_qty}")
    
    # Create custom buttons with clear labels
    add_button = msg_box.addButton(f"Add {new_qty} → Total: {current_qty + new_qty}", QMessageBox.ActionRole)
    replace_button = msg_box.addButton(f"Set to {new_qty}", QMessageBox.ActionRole)
    cancel_button = msg_box.addButton("Cancel", QMessageBox.RejectRole)
    
    # Style the message box
    msg_box.setStyleSheet("""
        QMessageBox {
            background-color: white;
        }
        QLabel {
            font-size: 14px;
            padding: 10px;
            min-width: 300px;
        }
        QPushButton {
            padding: 8px 15px;
            font-size: 13px;
            min-width: 150px;
            margin: 5px;
            border: 1px solid #DEDEDE;
            border-radius: 4px;
            background: white;
        }
        QPushButton:hover {
            background: #F5F5F5;
            border-color: #2196F3;
        }
    """)
    
    # Show dialog and handle response
    msg_box.exec_()
    clicked_button = msg_box.clickedButton()
    
    if clicked_button == add_button:
        # Add new quantity to existing
        self._update_item_quantity(item_name, current_qty + new_qty)
    elif clicked_button == replace_button:
        # Replace with new quantity
        self._update_item_quantity(item_name, new_qty)
    
    # Reset numpad regardless of choice (including cancel)
    self._reset_numpad()

def _update_item_quantity(self, item_name, final_quantity):
    """Update item quantity in order list"""
    # First remove existing item
    existing_item = self._find_existing_item(item_name)
    if existing_item:
        self.order_list.remove_item(existing_item)
    
    # Add item with new quantity
    price = self.prices.get(item_name, 0)
    for _ in range(final_quantity):
        self.order_list.add_item(item_name, price)
    
    self._update_totals()
    self.search_input.clear_search()

def _add_product_with_quantity(self, item_name, quantity):
    """Add new product with specified quantity"""
    price = self.prices.get(item_name, 0)
    for _ in range(quantity):
        self.order_list.add_item(item_name, price)
    
    self._update_totals()
    self.search_input.clear_search()
    self._reset_numpad()

def _reset_numpad(self):
    """Reset numpad state"""
    self.numpad_widget._current_value = "0"
    self.numpad_widget._update_display()
    self.pending_quantity = None