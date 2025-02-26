# components/pos/order_list_widget.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QScrollArea, QToolButton, QMenu, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from models.order_item import OrderItem
from styles.layouts import layout_config
from styles.order_widgets import OrderWidgetStyles

class OrderListWidget(QFrame):
    """Widget for displaying and managing order items"""
    
    # Signals
    item_selected = pyqtSignal(OrderItem)
    item_removed = pyqtSignal(OrderItem)
    order_cleared = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.order_items = []
        self.selected_item = None
        self.layout_config = layout_config.get_instance()
        
        # Use the centralized style with width from layout config
        order_panel_width = self.layout_config.get_pos_layout()['order_panel_width']
        self.setStyleSheet(OrderWidgetStyles.get_container_style(order_panel_width))
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize the order list UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Order Header
        layout.addWidget(self._create_header())
        
        # Order Items Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        # Use centralized scroll area style
        self.scroll_area.setStyleSheet(OrderWidgetStyles.SCROLL_AREA)
        
        self.order_list_widget = QWidget()
        # Use centralized order list widget style
        self.order_list_widget.setStyleSheet(OrderWidgetStyles.ORDER_LIST_WIDGET)
        
        self.order_list_layout = QVBoxLayout(self.order_list_widget)
        self.order_list_layout.setContentsMargins(5, 5, 5, 5)
        self.order_list_layout.setSpacing(5)
        self.order_list_layout.addStretch()
        
        self.scroll_area.setWidget(self.order_list_widget)
        layout.addWidget(self.scroll_area)
        
        # Quantity Summary
        self.qty_summary = self._create_quantity_summary()
        layout.addWidget(self.qty_summary)

    def _create_header(self):
        """Create order header with menu button"""
        header_frame = QFrame()
        # Use centralized order header style
        header_frame.setStyleSheet(OrderWidgetStyles.ORDER_HEADER)
        
        header_layout = QHBoxLayout(header_frame)
        # Get margins from layout config
        header_layout.setContentsMargins(
            self.layout_config.screen_config.get_size('order_header_margin_left'),
            self.layout_config.screen_config.get_size('order_header_margin_top'),
            self.layout_config.screen_config.get_size('order_header_margin_right'),
            self.layout_config.screen_config.get_size('order_header_margin_bottom')
        )
        
        order_label = QLabel("ORDER # 1234")
        menu_btn = QToolButton()
        menu_btn.setText("⋮")
        # Use centralized menu button style
        menu_btn.setStyleSheet(OrderWidgetStyles.HEADER_MENU_BUTTON)
        menu_btn.clicked.connect(self._show_menu)
        
        header_layout.addWidget(order_label)
        header_layout.addStretch()
        header_layout.addWidget(menu_btn)
        
        return header_frame

    def _create_quantity_summary(self):
        """Create frame showing total quantity and unique items"""
        summary_frame = QFrame()
        # Use centralized quantity summary style
        summary_frame.setStyleSheet(OrderWidgetStyles.QUANTITY_SUMMARY)
        
        summary_layout = QHBoxLayout(summary_frame)
        # Get margins from layout config
        summary_layout.setContentsMargins(
            self.layout_config.screen_config.get_size('order_summary_margin_left'),
            self.layout_config.screen_config.get_size('order_summary_margin_top'),
            self.layout_config.screen_config.get_size('order_summary_margin_right'),
            self.layout_config.screen_config.get_size('order_summary_margin_bottom')
        )
        
        self.qty_summary_label = QLabel("Qty: 0 | Items: 0")
        summary_layout.addWidget(self.qty_summary_label)
        summary_layout.addStretch()
        
        return summary_frame

    def _add_item_to_display(self, item: OrderItem) -> None:
        """Add a new item row to the order display"""
        # Remove stretch if exists
        self._remove_stretch()
        
        # Create item row
        item_widget = QFrame()
        item_widget.setProperty('selected', False)
        # Use centralized order item style
        item_widget.setStyleSheet(OrderWidgetStyles.ORDER_ITEM)
        
        item_layout = QHBoxLayout(item_widget)
        # Get margins from layout config
        item_layout.setContentsMargins(
            self.layout_config.screen_config.get_size('order_item_margin_left'),
            self.layout_config.screen_config.get_size('order_item_margin_top'),
            self.layout_config.screen_config.get_size('order_item_margin_right'),
            self.layout_config.screen_config.get_size('order_item_margin_bottom')
        )
        
        # Quantity
        qty_label = QLabel(str(item.quantity))
        # Use width from layout config
        qty_label.setFixedWidth(
            self.layout_config.screen_config.get_size('order_quantity_label_width')
        )
        qty_label.setAlignment(Qt.AlignCenter)
        
        # Name
        name_label = QLabel(item.name)
        
        # Total
        total_label = QLabel(f"{item.get_total():.2f}")
        total_label.setAlignment(Qt.AlignRight)
        # Use width from layout config
        total_label.setFixedWidth(
            self.layout_config.screen_config.get_size('order_total_label_width')
        )
        
        item_layout.addWidget(qty_label)
        item_layout.addWidget(name_label)
        item_layout.addWidget(total_label)
        
        # Store reference to the order item
        item_widget.order_item = item
        
        # Add click handling
        item_widget.mousePressEvent = lambda event, widget=item_widget: self._on_item_clicked(widget, event)
        
        self.order_list_layout.addWidget(item_widget)
        self.order_list_layout.addStretch()

    def _show_menu(self):
        """Show the order actions menu"""
        menu = QMenu(self)
        # Use centralized menu style
        menu.setStyleSheet(OrderWidgetStyles.MENU)

        clear_action = menu.addAction("Cancel Order")
        clear_item = menu.addAction("Remove Selected Item")
        
        action = menu.exec_(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))
        
        if action == clear_action:
            self.clear_order()
        elif action == clear_item:
            self.remove_selected_item()

    def _on_item_clicked(self, widget, event):
        """Handle item selection"""
        if event.button() == Qt.LeftButton:
            self._select_item(widget)
            self.item_selected.emit(widget.order_item)

    def _select_item(self, widget):
        """Update selection status of items"""
        for i in range(self.order_list_layout.count()):
            item = self.order_list_layout.itemAt(i).widget()
            if item and isinstance(item, QFrame):
                item.setProperty('selected', False)
                item.setStyleSheet(OrderWidgetStyles.ORDER_ITEM)
                item.style().unpolish(item)
                item.style().polish(item)
        
        widget.setProperty('selected', True)
        # Use centralized selected item style
        widget.setStyleSheet(OrderWidgetStyles.ORDER_ITEM_SELECTED)
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        self.selected_item = widget

    def clear_order(self):
        """Clear all items from the order after confirmation"""
        # Create message box
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Clear Order')
        msg_box.setText('Are you sure you want to clear the current order?')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        # Apply centralized message box style
        msg_box.setStyleSheet(OrderWidgetStyles.MESSAGE_BOX)
        
        reply = msg_box.exec_()
        
        if reply == QMessageBox.Yes:
            self.order_items = []
            self._update_display()
            self.order_cleared.emit()

    def remove_selected_item(self):
        """Remove the currently selected item"""
        if self.selected_item and hasattr(self.selected_item, 'order_item'):
            item = self.selected_item.order_item
            self.order_items.remove(item)
            self.item_removed.emit(item)
            self.selected_item = None
            self._update_display()

    def remove_item(self, item):
        """Remove a specific item from the order list
        
        Args:
            item: The OrderItem object to remove
        """
        if item in self.order_items:
            self.order_items.remove(item)
            self._update_display()
            self._update_quantity_summary()
            self.item_removed.emit(item)

    def _update_display(self):
        """Update the entire order display"""
        self._clear_display()
        for item in self.order_items:
            self._add_item_to_display(item)
        self._update_quantity_summary()

    def _clear_display(self):
        """Clear all items from display"""
        for i in reversed(range(self.order_list_layout.count())):
            widget = self.order_list_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def _remove_stretch(self):
        """Remove stretch from layout if it exists"""
        for i in reversed(range(self.order_list_layout.count())):
            if self.order_list_layout.itemAt(i).widget() is None:
                self.order_list_layout.takeAt(i)

    def _update_quantity_summary(self):
        """Update the quantity summary label"""
        total_qty = sum(item.quantity for item in self.order_items)
        unique_items = len(self.order_items)
        self.qty_summary_label.setText(f"Qty: {total_qty} | Items: {unique_items}")

    def clear_items(self):
        """Clear all items from the order list"""
        self.order_items = []
        # Clear the UI display
        self._clear_display()
        # Update the quantity summary
        self._update_quantity_summary()
        # Emit order cleared signal
        self.order_cleared.emit()

    @property
    def total_amount(self):
        """Calculate total amount for all items"""
        return sum(item.get_total() for item in self.order_items)

    @property
    def items_count(self):
        """Get total number of items"""
        return len(self.order_items)