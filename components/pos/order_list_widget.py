from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QScrollArea, QToolButton, QMenu, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from models.order_item import OrderItem
from styles import POSStyles
from styles.layouts import layout_config 

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
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize the order list UI"""
        self.setStyleSheet(POSStyles.ORDER_PANEL(
            self.layout_config.get_pos_layout()['order_panel_width']
        ))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Order Header
        layout.addWidget(self._create_header())
        
        # Order Items Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)   
        self.scroll_area.setStyleSheet(POSStyles.SCROLL_AREA)
        
        self.order_list_widget = QWidget()
        self.order_list_widget.setStyleSheet(POSStyles.ORDER_LIST_WIDGET)
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
        header_frame.setStyleSheet("""
            QFrame {
                background: #F8F9FA;
                border: none;
            }
            QLabel {
                color: #2196F3;
                font-size: 16px;
                font-weight: 500;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 5, 0, 5)
        
        order_label = QLabel("ORDER # 1234")
        menu_btn = QToolButton()
        menu_btn.setText("⋮")
        menu_btn.setStyleSheet("""
            QToolButton {
                border: none;
                color: #2196F3;
                font-size: 20px;
                font-weight: bold;
                padding-left: 5px;
                padding-right: 5px;
            }
            QToolButton:hover {
                background: #EEEEEE;
                border-radius: 4px;
            }
        """)
        menu_btn.clicked.connect(self._show_menu)
        
        header_layout.addWidget(order_label)
        header_layout.addStretch()
        header_layout.addWidget(menu_btn)
        
        return header_frame

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

    def add_item(self, item_name: str, price: float) -> None:
        """Add an item to the order or increment its quantity if it exists"""
        existing_item = None
        for item in self.order_items:
            if item.name == item_name:
                existing_item = item
                break
        
        if existing_item:
            existing_item.quantity += 1
            self._update_display()
        else:
            new_item = OrderItem(item_name, price)
            self.order_items.append(new_item)
            self._add_item_to_display(new_item)
            self._update_quantity_summary()

    def _add_item_to_display(self, item: OrderItem) -> None:
        """Add a new item row to the order display"""
        # Remove stretch if exists
        self._remove_stretch()
        
        # Create item row
        item_widget = QFrame()
        item_widget.setProperty('selected', False)
        item_widget.setStyleSheet("""
            QFrame {
                background: white;
                border-bottom: 1px solid #EEEEEE;
                padding: 2px;
            }
            QFrame[selected="true"] {
                background: #E3F2FD;
                border: 1px solid #2196F3;
                border-radius: 4px;
            }
            QLabel {
                color: #333;
            }
        """)
        
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(5, 2, 5, 2)
        
        # Quantity
        qty_label = QLabel(str(item.quantity))
        qty_label.setFixedWidth(30)
        qty_label.setAlignment(Qt.AlignCenter)
        
        # Name
        name_label = QLabel(item.name)
        
        # Total
        total_label = QLabel(f"{item.get_total():.2f}")
        total_label.setAlignment(Qt.AlignRight)
        total_label.setFixedWidth(60)
        
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
        menu.setStyleSheet(POSStyles.MENU)

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
                item.style().unpolish(item)
                item.style().polish(item)
        
        widget.setProperty('selected', True)
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
      
      # Apply styling to the message box
      msg_box.setStyleSheet("""
          QMessageBox {
              background-color: white;
              border: 1px solid #DEDEDE;
              border-radius: 4px;
          }
          QMessageBox QLabel {
              color: #333;
              font-size: 14px;
              padding: 10px;
          }
          QPushButton {
              background-color: white;
              border: 1px solid #DEDEDE;
              border-radius: 4px;
              min-width: 80px;
              padding: 6px 12px;
              margin: 4px;
              color: #333;
          }
          QPushButton:hover {
              background-color: #F0F0F0;
              border-color: #2196F3;
              color: #2196F3;
          }
          QPushButton:default {
              border-color: #2196F3;
              color: #2196F3;
          }
      """)
      
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

    @property
    def total_amount(self):
        """Calculate total amount for all items"""
        return sum(item.get_total() for item in self.order_items)

    @property
    def items_count(self):
        """Get total number of items"""
        return len(self.order_items)