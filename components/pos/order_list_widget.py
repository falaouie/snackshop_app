# components/pos/order_list_widget.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QScrollArea, QToolButton, QMenu, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from models.order_item import OrderItem
from styles.order_widgets import OrderWidgetStyles
from config.layouts.order_list_layout import order_layout_config

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

        # Apply styling
        self.setStyleSheet(OrderWidgetStyles.get_order_container_style())
        
        # Set panel dimensions from config
        panel_dimensions = order_layout_config.get_panel_dimensions() 
        self.setFixedWidth(panel_dimensions['width'])

        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize the order list UI"""
        list_config = order_layout_config.get_list_layout()
        layout = QVBoxLayout(self)
        margins = order_layout_config.get_header_margins()
        layout.setContentsMargins(
            margins[0],  # left margin
            margins[1],  # top margin
            margins[2],  # right margin
            margins[3]   # bottom margin
        )
        spacing = list_config['spacing']
        layout.setSpacing(spacing)
        
        # Order Header
        layout.addWidget(self._create_header())
        
        # Order Items Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        # Set scroll area dimensions from config
        scroll_config = order_layout_config.get_scrollbar_config()
        scroll_style = OrderWidgetStyles.get_scroll_area_style()
        self.scroll_area.setStyleSheet(scroll_style)
        
        self.order_list_widget = QWidget()
        list_style = OrderWidgetStyles.get_order_list_widget_style()
        self.order_list_widget.setStyleSheet(list_style)
        
        self.order_list_layout = QVBoxLayout(self.order_list_widget)
        
        content_margin = list_config['content_margin']
        spacing = list_config['spacing']
        self.order_list_layout.setContentsMargins(
            content_margin, content_margin, content_margin, content_margin
        )
        self.order_list_layout.setSpacing(spacing)
        self.order_list_layout.addStretch()
        
        self.scroll_area.setWidget(self.order_list_widget)
        layout.addWidget(self.scroll_area)
        
        # Quantity Summary
        self.qty_summary = self._create_quantity_summary()
        layout.addWidget(self.qty_summary)

    def _create_header(self):
        """Create order header with menu button"""
        header_frame = QFrame()
        header_frame.setStyleSheet(OrderWidgetStyles.get_order_header_style())

        header_layout = QHBoxLayout(header_frame)
        
        # Get margins from order_layout_config
        margins = order_layout_config.get_header_margins()
        header_layout.setContentsMargins(
            margins[0],  # left margin
            margins[1],  # top margin
            margins[2],  # right margin
            margins[3]   # bottom margin
        )
        
        order_label = QLabel("ORDER # 1234")
        # Apply font size from config
        font = QFont()
        font_size = order_layout_config.get_styling()['font_size']
        font.setPointSize(font_size)
        order_label.setFont(font)
        
        menu_btn = QToolButton()
        menu_btn.setText("⋮")
        
        # Apply font size from config
        menu_font = QFont()
        menu_font_size = font_size + 4  # Slightly larger
        menu_font.setPointSize(menu_font_size)
        menu_btn.setFont(menu_font)
        
        # Get padding from config
        menu_padding = order_layout_config.get_header_menu_button_padding()
        menu_btn.setContentsMargins(
            menu_padding['padding_left'],
            0,
            menu_padding['padding_right'],
            0
        )
        
        # Apply style
        menu_btn.setStyleSheet(OrderWidgetStyles.get_header_menu_button_style())
        menu_btn.clicked.connect(self._show_menu)
        
        header_layout.addWidget(order_label)
        header_layout.addStretch()
        header_layout.addWidget(menu_btn)
        
        return header_frame

    def _create_quantity_summary(self):
        """Create frame showing total quantity and unique items"""
        summary_frame = QFrame()
        summary_frame.setStyleSheet(OrderWidgetStyles.get_quantity_summary_style())
        
        summary_layout = QHBoxLayout(summary_frame)
        
        # Get margins from order_layout_config
        margins = order_layout_config.get_summary_margins()
        summary_layout.setContentsMargins(
            margins[0],  # left margin
            margins[1],  # top margin
            margins[2],  # right margin
            margins[3]   # bottom margin
        )
        
        self.qty_summary_label = QLabel("Qty: 0 | Items: 0")
        
        # Apply font size from config
        font = QFont()
        font_size = order_layout_config.get_styling()['font_size'] - 1  # Slightly smaller
        font.setPointSize(font_size)
        self.qty_summary_label.setFont(font)
        
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
        item_widget.setStyleSheet(OrderWidgetStyles.get_order_item_style())
        
        item_layout = QHBoxLayout(item_widget)
        # Get margins from order_layout_config
        margins = order_layout_config.get_item_margins()
        item_layout.setContentsMargins(
            margins[0],  # left margin
            margins[1],  # top margin
            margins[2],  # right margin
            margins[3]   # bottom margin
        )
        
        # Get item padding from config and apply it
        item_padding = order_layout_config.get_item_padding()
        item_widget.setContentsMargins(item_padding, item_padding, item_padding, item_padding)
        
        # Quantity
        label_widths = order_layout_config.get_label_widths()
        qty_label = QLabel(str(item.quantity))
        
        # Apply font from config
        font_size = order_layout_config.get_styling()['font_size']
        font = QFont()
        font.setPointSize(font_size)
        qty_label.setFont(font)
        
        # Use width from config
        qty_label.setFixedWidth(label_widths['quantity'])
        qty_label.setAlignment(Qt.AlignCenter)
        
        # Name
        name_label = QLabel(item.name)
        name_label.setFont(font)  # Use same font
        
        # Total
        total_label = QLabel(f"{item.get_total():.2f}")
        total_label.setFont(font)  # Use same font
        total_label.setAlignment(Qt.AlignRight)
        # Use width from config
        total_label.setFixedWidth(label_widths['total'])
        
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
        
        # Get menu configuration
        menu_config = order_layout_config.get_menu_config()
        
        # Apply font size from config
        font = QFont()
        font.setPointSize(menu_config['font_size'])
        menu.setFont(font)
        
        # Apply visual styling
        menu.setStyleSheet(OrderWidgetStyles.get_menu_style())
        
        # Create menu actions
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
                item.setStyleSheet(OrderWidgetStyles.get_order_item_style())
                item.style().unpolish(item)
                item.style().polish(item)
        
        widget.setProperty('selected', True)
        # Use new method for selected item style
        widget.setStyleSheet(OrderWidgetStyles.get_order_item_selected_style())
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
        
        # Get message box config
        msgbox_config = order_layout_config.get_message_box_config()
        
        # Apply font size from config
        font = QFont()
        font.setPointSize(msgbox_config['font_size'])
        msg_box.setFont(font)
        
        # Apply visual styling
        msg_box.setStyleSheet(OrderWidgetStyles.get_message_box_style())
        
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