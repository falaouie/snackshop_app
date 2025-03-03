def _select_item(self, widget):
    """Update selection status of items"""
    for i in range(self.order_list_layout.count()):
        item = self.order_list_layout.itemAt(i).widget()
        if item and isinstance(item, QFrame):
            item.setProperty('selected', False)
            item.setStyleSheet(OrderWidgetStyles.get_order_item_style())
            item.style().unpolish(item)
            item.style().polish(item)
    
    widget.setProperty('selected', True)
    # Use new method for selected item style
    widget.setStyleSheet(OrderWidgetStyles.get_order_item_selected_style())
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    self.selected_item = widget