from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                                QPushButton, QFrame, QSplitter, QGridLayout, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtSvg import QSvgRenderer

from styles import POSStyles
from styles.buttons import ButtonStyles
from styles.layouts import layout_config

from components.pos.order_list_widget import OrderListWidget
from components.pos.product_grid_widget import ProductGridWidget
from components.pos.totals_widget import TotalsWidget
from components.pos.search_widget import SearchWidget
from components.keyboard import VirtualKeyboard
from components.pos.order_type_widget import OrderTypeWidget
from components.pos.horizontal_buttons_widget import HorizontalButtonsWidget
from components.pos.transaction_buttons_widget import TransactionButtonsWidget
from components.pos.payment_buttons_widget import PaymentButtonsWidget
from components.numpad import NumpadWidget, NumpadMode

from models.product_catalog import PRODUCT_PRICES

class POSView(QWidget):
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
        
        self.transaction_buttons = None  # Will be initialized in _create_products_widget

        self._setup_ui()
        self._update_time()

    def _setup_ui(self):
        """Initialize the main UI structure"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 10)
        main_layout.setSpacing(0)

        # Add top bar
        top_bar_container = self._create_top_bar()
        main_layout.addWidget(top_bar_container)

        # Main Content Area with Splitter
        content_splitter = QSplitter(Qt.Horizontal)
        content_splitter.setStyleSheet(POSStyles.SPLITTER)
        
        # Left Side - Order Details
        self.order_widget = self._create_order_widget()
        self.order_widget.setStyleSheet(POSStyles.ORDER_PANEL(
            self.layout_config.get_pos_layout()['order_panel_width']
        ))
        content_splitter.addWidget(self.order_widget)
        
        # Right Side - Products Grid
        self.products_widget = self._create_products_widget()
        content_splitter.addWidget(self.products_widget)
        
        main_layout.addWidget(content_splitter, 1)

        # Create and add bottom bar
        self.bottom_bar = self._create_bottom_bar()
        main_layout.addWidget(self.bottom_bar)

    def _create_top_bar(self):
        """Create top bar with employee info, search, and lock button"""
        pos_layout = self.layout_config.get_pos_layout()
        self.top_bar = QFrame()
        self.top_bar.setStyleSheet(POSStyles.TOP_BAR(
            pos_layout['top_bar_height']
        ))
        
        # Main layout
        layout = QHBoxLayout(self.top_bar)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Employee Zone with DateTime
        emp_zone = QFrame()
        emp_zone.setStyleSheet(POSStyles.EMPLOYEE_ZONE)
        emp_layout = QHBoxLayout(emp_zone)
        emp_layout.setSpacing(8)
        emp_layout.setContentsMargins(0, 0, 0, 0) 
        
        # Employee icon
        emp_icon = QLabel()
        renderer = QSvgRenderer("assets/images/employee_icon.svg")
        pixmap = QPixmap(40, 40)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        emp_icon.setPixmap(pixmap)
        emp_id = QLabel(f"Emp ID: {self.user_id}")
        emp_id.setStyleSheet(POSStyles.EMPLOYEE_ID)
        
        # DateTime Zone
        time_zone = QFrame()
        time_zone.setStyleSheet(POSStyles.DATE_TIME_ZONE)
        time_layout = QVBoxLayout(time_zone)
        time_layout.setContentsMargins(10, 5, 10, 5)
        time_layout.setSpacing(2)

        self.date_label = QLabel()
        self.date_label.setStyleSheet(POSStyles.DATE_LABEL)

        self.time_label = QLabel()
        self.time_label.setStyleSheet(POSStyles.TIME_LABEL)

        time_layout.addWidget(self.date_label)
        time_layout.addWidget(self.time_label)

        # Add widgets to employee zone
        emp_layout.addWidget(emp_icon)
        emp_layout.addWidget(emp_id)
        emp_layout.addWidget(time_zone)

        # Search Section (Centered)
        search_container = QFrame()
        search_container.setStyleSheet("background: transparent;")
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create and connect search widget
        self.search_input = SearchWidget(self)
        self.search_input.search_changed.connect(self._filter_products)
        
        # Add search elements to search layout
        search_layout.addStretch(1)
        search_layout.addWidget(self.search_input)
        search_layout.addStretch(1)

        # Controls Zone (Lock Button)
        controls_zone = QFrame()
        controls_layout = QHBoxLayout(controls_zone)
        controls_layout.setSpacing(8)
        controls_layout.setContentsMargins(0, 0, 0, 0)

        # Lock button
        lock_btn = QPushButton()
        renderer = QSvgRenderer("assets/images/lock_screen.svg")
        pixmap = QPixmap(55, 55)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        lock_btn.setIcon(QIcon(pixmap))
        lock_btn.setIconSize(QSize(55, 55))
        lock_btn.setStyleSheet(POSStyles.LOCK_BUTTON)
        lock_btn.clicked.connect(self._handle_lock)
        
        controls_layout.addWidget(lock_btn)
        
        # Add all zones to main layout
        layout.addWidget(emp_zone)
        layout.addWidget(search_container, 1)
        layout.addWidget(controls_zone)
        
        return self.top_bar

    def _create_order_widget(self):
        """Create order panel"""
        order_frame = QFrame()
        
        layout = QVBoxLayout(order_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create and connect order list widget
        self.order_list = OrderListWidget()
        self.order_list.order_cleared.connect(self._on_order_cleared)
        self.order_list.item_removed.connect(self._on_item_removed)
        layout.addWidget(self.order_list)
        
        # Add horizontal buttons widget and connect signal
        self.horizontal_buttons = HorizontalButtonsWidget(self)
        self.horizontal_buttons.action_triggered.connect(self._on_horizontal_action)
        layout.addWidget(self.horizontal_buttons)

        return order_frame

    def _create_products_widget(self):
        """Create products panel"""
        products_frame = QFrame()
        
        # Main layout for products area
        main_layout = QVBoxLayout(products_frame)
        main_layout.setContentsMargins(0, 5, 0, 0)
        main_layout.setSpacing(8)

        # Container for products grid and center panel
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)

        # Center buttons panel
        center_panel = QFrame()
        center_panel.setFixedWidth(120)
        center_panel.setStyleSheet("""
            QFrame {
                background: white;
                border-left: 1px solid #DEDEDE;
                border-right: 1px solid #DEDEDE;
            }
        """)
        
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(8)

        # Create and add transaction buttons widget
        self.transaction_buttons = TransactionButtonsWidget()
        self.transaction_buttons.action_triggered.connect(self._on_transaction_action)
        center_layout.addWidget(self.transaction_buttons)

        # Create and connect product grid
        self.product_grid = ProductGridWidget()
        self.product_grid.product_selected.connect(self._handle_product_click)
        
        # Add panels to content layout
        content_layout.addWidget(center_panel)
        content_layout.addWidget(self.product_grid, 1)

        # Add content container to main layout
        main_layout.addWidget(content_container, 1)

        # Create intermediate container for numpad and payment sections
        intermediate_container = QFrame()
        intermediate_container.setFixedHeight(350)  # Set fixed height for the container
        intermediate_container.setStyleSheet("""
            QFrame {
                background: white;
                border-top: 1px solid #DEDEDE;
            }
        """)
        
        # Layout for intermediate container
        intermediate_layout = QHBoxLayout(intermediate_container)
        intermediate_layout.setContentsMargins(10, 10, 10, 10)
        intermediate_layout.setSpacing(10)
        intermediate_layout.addStretch()

        # Add numpad widget (left side)
        self.numpad_widget = NumpadWidget(self)
        # Connect to track value changes
        self.numpad_widget.display.textChanged.connect(self._handle_numpad_value_change)
        intermediate_layout.addWidget(self.numpad_widget)

        # Create right side container for totals and payment
        right_container = QFrame()
        right_layout = QHBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)
        right_layout.addStretch()
        # Add payment buttons to right container
        self.payment_buttons = PaymentButtonsWidget()
        self.payment_buttons.action_triggered.connect(self._on_payment_action)
        right_layout.addWidget(self.payment_buttons)

        # Add totals widget to right container
        self.totals_widget = TotalsWidget(self.exchange_rate)
        right_layout.addWidget(self.totals_widget)

        # Add right container to intermediate layout
        intermediate_layout.addWidget(right_container, 1)

        # Add intermediate container to main layout
        main_layout.addWidget(intermediate_container)

        return products_frame

    def _create_bottom_bar(self):
        """Bottom bar remains unchanged - contains only order type widget"""
        bottom_bar = QFrame()
        bottom_bar.setStyleSheet(POSStyles.BOTTOM_BAR(
            self.layout_config.get_pos_layout()['bottom_bar_height']
        ))
        layout = QHBoxLayout(bottom_bar)
        layout.setContentsMargins(10, 5, 10, 10)
        layout.setSpacing(6)

        # Create and add order type widget
        self.order_type_widget = OrderTypeWidget()
        self.order_type_widget.order_type_changed.connect(self._on_order_type_changed)
        layout.addWidget(self.order_type_widget)
        
        layout.addStretch()

        return bottom_bar

    def _on_transaction_action(self, action_type):
        """HHook for transaction-related coordination.
        
        Future use cases:
        - Order state management
        - Cross-widget coordination
        - Permission checking
        - Logging/tracking
        """
        # Example future coordination:
        # if action_type == 'HOLD':
        #     self.order_list.setEnabled(False)
        #     self.totals_widget.update_status("On Hold")
        pass

    def _on_horizontal_action(self, action_type):
        """Hook for horizontal button coordination.
        
        Future use cases:
        - Order state changes
        - UI updates across widgets
        - Event logging
        """
        # Example future coordination:
        # if action_type == 'VOID':
        #     self._clear_current_order()
        #     self._update_transaction_log()
        pass

    def _on_payment_action(self, action_type):
        """Hook for payment-related coordination.
        
        Future use cases:
        - Payment flow management
        - Receipt generation
        - Order status updates
        - Cross-widget coordination for payment process
        """
        pass

    def _filter_products(self):
        """Filter products based on search input"""
        search_text = self.search_input.text()
        self.product_grid.set_search_text(search_text)

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

    # Event Handlers
    def _on_order_cleared(self):
        """Handle order being cleared"""
        self._update_totals()

    def _on_item_removed(self, item):
        """Handle item removal from order"""
        self._update_totals()

    def _on_order_type_changed(self, order_type):
        """Handle order type changes"""
        pass

    def _update_totals(self):
        """Update totals display"""
        total_usd = self.order_list.total_amount
        self.totals_widget.update_totals(total_usd)

    def _update_time(self):
        """Update the time display"""
        current = QDateTime.currentDateTime()
        self.date_label.setText(current.toString("dd-MM-yyyy"))
        self.time_label.setText(current.toString("h:mm AP"))

    def _handle_lock(self):
        """Handle lock button click"""
        from ..view_manager import ViewManager
        ViewManager.get_instance().switch_back_to_pin_view_from_pos(self.user_id)
        self.deleteLater()