# In POSView class, add this new method:
def _create_quantity_summary(self):
    """Create frame showing total quantity and unique items"""
    summary_frame = QFrame()
    summary_frame.setStyleSheet("""
        QFrame {
            background: white;
            border-top: 1px solid #DEDEDE;
        }
        QLabel {
            color: #666;
            font-size: 13px;
        }
    """)
    
    summary_layout = QHBoxLayout(summary_frame)
    summary_layout.setContentsMargins(15, 8, 15, 8)
    
    self.qty_summary_label = QLabel("Qty: 0 | Items: 0")
    summary_layout.addWidget(self.qty_summary_label)
    summary_layout.addStretch()
    
    return summary_frame

def _update_quantity_summary(self):
    """Update the quantity summary label"""
    total_qty = sum(item.quantity for item in self.order_items)
    unique_items = len(self.order_items)
    self.qty_summary_label.setText(f"Qty: {total_qty} | Items: {unique_items}")

# Modify _create_order_widget to add the summary frame
# After the scroll_area.setWidget(self.order_list_widget) line, add:
        layout.addWidget(scroll_area)
        
        # Add quantity summary
        self.quantity_summary = self._create_quantity_summary()
        layout.addWidget(self.quantity_summary)
        
        # Add horizontal buttons section
        horizontal_buttons_frame = QFrame()

# Modify _update_order_display to update the summary
def _update_order_display(self):
    """Update the entire order display"""
    # Clear current display
    for i in reversed(range(self.order_list_layout.count())):
        widget = self.order_list_layout.itemAt(i).widget()
        if widget:
            widget.deleteLater()
    
    # Add all items
    for item in self.order_items:
        self._add_item_to_display(item)
    
    # Update quantity summary
    self._update_quantity_summary()

# Modify _clear_order to update the summary when clearing
def _clear_order(self):
    """Clear all items from the current order"""
    reply = QMessageBox.question(
        self,
        'Clear Order',
        'Are you sure you want to clear the current order?',
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    
    if reply == QMessageBox.Yes:
        # Clear order items
        self.order_items = []
        
        # Update displays
        self._update_order_display()
        self._update_totals()
        self._update_quantity_summary()  # Add this line