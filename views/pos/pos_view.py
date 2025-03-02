from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                                QPushButton, QFrame, QSplitter, QMessageBox)
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtSvg import QSvgRenderer

from styles import POSStyles
from styles.order_widgets import OrderWidgetStyles
from styles.layouts import layout_config
from config.layouts.order_list_layout import order_layout_config

from components.common.top_bar import TopBarWidget
from components.pos.order_list_widget import OrderListWidget
from components.pos.product_grid_widget import ProductGridWidget
from components.pos.totals_widget import TotalsWidget
from components.pos.search_widget import KeyboardEnabledSearchWidget as SearchWidget

from components.pos.order_type_widget import OrderTypeWidget
from components.pos.transaction_buttons_widget import TransactionButtonsWidget
from components.keyboard import VirtualKeyboard
from components.numpad import NumpadWidget
from components.pos.usd_preset_widget import USDPresetWidget
from components.pos.lbp_preset_widget import LBPPresetWidget
from components.pos.card_payment_widget import CardPaymentWidget
from components.pos.other_payment_widget import OtherPaymentWidget
from components.pos.cash_usd_payment_widget import CashUSDPaymentWidget
from components.pos.cash_lbp_payment_widget import CashLBPPaymentWidget 

from controllers.pos_controller import POSController


class POSView(QWidget):
    # Define constants
    BUTTON_PROTECTION_TIMEOUT_MS = 500

    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.layout_config = layout_config.get_instance()

        self.current_currency_mode = None  # Tracks which currency type is active

         # Create controller 
        self.controller = POSController()
        
        # Get exchange rate from controller
        self.exchange_rate = self.controller.get_exchange_rate()

        self.keyboard = VirtualKeyboard(self)
        self.pending_quantity = None  # Track pending quantity from numpad
        self.pending_value = None  # Track pending value from numpad

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self._update_time)
        # self.timer.start(1000)

        # Track last clicked product and timer
        self.last_numpad_product = None
        self.button_protection_timer = QTimer(self)
        self.button_protection_timer.setSingleShot(True)
        self.button_protection_timer.timeout.connect(self._reset_button_protection)

        self._setup_ui()
        # self._update_time()

    def _setup_ui(self):
        """Initialize the main UI structure"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 10)
        main_layout.setSpacing(0)

        # Add top bar with simplified initialization
        self.top_bar = TopBarWidget(user_id=self.user_id, parent=self)
        
        # Connect signals immediately after creation
        self.top_bar.search_changed.connect(self._filter_products)
        self.top_bar.lock_clicked.connect(self._handle_lock)
        
        # Store reference to search widget for later use
        self.search_input = self.top_bar.get_search_widget()
        
        # Add to layout
        main_layout.addWidget(self.top_bar)

        # Create main content area with splitter
        content_splitter = QSplitter(Qt.Horizontal)
        content_splitter.setStyleSheet(POSStyles.SPLITTER)
        content_splitter.setHandleWidth(
            self.layout_config.get_pos_layout()['splitter_handle_width']
        )
        
        # Left container (will hold left column)
        left_container = QWidget()
        left_container.setStyleSheet(POSStyles.LEFT_CONTAINER())
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(
            self.layout_config.get_pos_layout()['order_type_button_spacing']
        )
        
        # Create inner splitter for order_list and center_panel first
        inner_splitter = QSplitter(Qt.Horizontal)
        inner_splitter.setStyleSheet(POSStyles.SPLITTER)
        inner_splitter.setHandleWidth(
            self.layout_config.get_pos_layout()['splitter_handle_width']
        )
        
        # Left Side - Order Details
        self.order_widget = self._create_order_widget()
        inner_splitter.addWidget(self.order_widget)
        
        # Center Panel
        self.center_panel = self._create_center_panel()
        inner_splitter.addWidget(self.center_panel)

        # Set stretch factors for inner splitter (after adding widgets)
        inner_splitter.setStretchFactor(0, 0)  # Order panel - fixed size
        inner_splitter.setStretchFactor(1, 0)  # Center panel - fixed size
        
        # Make inner splitter non-resizable
        inner_splitter.setChildrenCollapsible(False)
        inner_splitter.handle(0).setAttribute(Qt.WA_TransparentForMouseEvents, True)

        # Add inner splitter to left container first
        left_layout.addWidget(inner_splitter)

        # Create order type container with fixed height
        order_type_container = QWidget()
        order_type_container.setStyleSheet(POSStyles.ORDER_TYPE_CONTAINER())
        order_type_container.setFixedHeight(
            self.layout_config.get_pos_layout()['order_type_container_height']
        )
        order_type_layout = QVBoxLayout(order_type_container)
        order_type_layout.setContentsMargins(0, 0, 0, 0)
        order_type_layout.setSpacing(0)

        # Create and add order type widget 
        self.order_type_widget = OrderTypeWidget()
        self.order_type_widget.order_type_changed.connect(self._on_order_type_changed)
        order_type_layout.addWidget(self.order_type_widget)

        # Add order type container to left layout after the splitter
        left_layout.addWidget(order_type_container)
        
        # Add left container to main splitter
        content_splitter.addWidget(left_container)
        
        # Right Side - Products Grid
        self.products_widget = self._create_products_widget()
        content_splitter.addWidget(self.products_widget)
        
        # Set properties for main content splitter (after adding widgets)
        content_splitter.setChildrenCollapsible(False)
        content_splitter.handle(0).setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        # Add content splitter to main layout
        main_layout.addWidget(content_splitter, 1)

        # Create and add bottom bar
        self.bottom_bar = self._create_bottom_bar()
        main_layout.addWidget(self.bottom_bar)

    def _create_center_panel(self):
        """Create center panel with transaction buttons"""
        center_panel = QFrame()
        # Get width from layout config
        center_width = self.layout_config.get_pos_layout()['center_panel_width']
        # Set explicit size constraints to make it fixed width
        center_panel.setFixedWidth(center_width) 
        center_panel.setStyleSheet(POSStyles.CENTER_PANEL())
        
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(8)

        # Add top stretch for vertical centering
        # center_layout.addStretch(1)

        # Create and add transaction buttons widget
        self.transaction_buttons = TransactionButtonsWidget()
        self.transaction_buttons.action_triggered.connect(self._on_transaction_action)
        
        # Create container for horizontal centering
        button_container = QWidget()
        button_container_layout = QHBoxLayout(button_container)
        button_container_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add stretches for horizontal centering
        button_container_layout.addStretch(1)
        button_container_layout.addWidget(self.transaction_buttons)
        button_container_layout.addStretch(1)
        
        center_layout.addWidget(button_container)
        
        # Add bottom stretch for vertical centering
        center_layout.addStretch(1)

        return center_panel

    def _create_order_widget(self):
        """Create order panel"""
        order_frame = QFrame()

        # Get width from our new config
        order_list_panel_width = order_layout_config.get_size('order_list_panel_width')
        
        # Set explicit size policies to ensure QSplitter respects our width
        order_frame.setMinimumWidth(order_list_panel_width)
        order_frame.setMaximumWidth(order_list_panel_width)

        # Apply styling but remove width from the style (will be controlled by size policies)
        # order_frame.setStyleSheet("""
        #     QFrame {
        #         background: white;
        #         border: 1px solid #DEDEDE;
        #     }
        # """)
        
        layout = QVBoxLayout(order_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create and connect order list widget
        self.order_list = OrderListWidget()
        self.order_list.order_cleared.connect(self._on_order_cleared)
        self.order_list.item_removed.connect(self._on_item_removed)
        layout.addWidget(self.order_list)

        return order_frame


    def _create_products_widget(self):
        """Create products panel with grid and intermediate section"""
        products_frame = QFrame()
        products_frame.setStyleSheet(POSStyles.PRODUCTS_FRAME())

        main_layout = QVBoxLayout(products_frame)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create product grid FIRST
        self.product_grid = ProductGridWidget()
        self.product_grid.product_selected.connect(self._handle_product_click)

        # Then create the category container using the existing product grid
        category_container = self._create_category_container()
        main_layout.addWidget(category_container)

        # Add the product grid
        main_layout.addWidget(self.product_grid, 1)

        # Create and add intermediate section
        intermediate_container = self._create_intermediate_container()
        main_layout.addWidget(intermediate_container)

        return products_frame
    
    def _create_category_container(self):
        """Create container for category buttons"""
        category_container = QWidget()
        category_container.setStyleSheet(POSStyles.CATEGORY_CONTAINER())
        category_container.setFixedHeight(
            self.layout_config.get_pos_layout()['category_container_height']
        )
        
        category_layout = QVBoxLayout(category_container)
        category_layout.setContentsMargins(0, 0, 0, 0)
        category_layout.setSpacing(
            self.layout_config.get_pos_layout()['category_button_spacing']
        )
        
        # Use the existing product grid - remove the conditional creation
        category_layout.addWidget(self.product_grid.get_category_bar())
        
        return category_container
    
    def _create_intermediate_container(self):
        """Create container for numpad and payment section"""
        container = QFrame()
        container.setFixedHeight(
            self.layout_config.get_pos_layout()['intermediate_container_height']
        )
        container.setStyleSheet(POSStyles.INTERMEDIATE_CONTAINER())
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Add numpad
        self.numpad_widget = NumpadWidget(self)
        self.numpad_widget.value_changed.connect(self._handle_numpad_value_change)
        if hasattr(self.numpad_widget, 'clear'):
            old_clear = self.numpad_widget.clear
            def new_clear():
                old_clear()
                self._on_numpad_cleared()
            self.numpad_widget.clear = new_clear
        layout.addWidget(self.numpad_widget)
        
        # Create USD Preset Widget 
        self.usd_preset_widget = USDPresetWidget()
        self.usd_preset_widget.preset_selected.connect(self._handle_preset_selected)

        layout.addWidget(self.usd_preset_widget)

        # Create LBP Preset Widget
        self.lbp_preset_widget = LBPPresetWidget()
        self.lbp_preset_widget.preset_selected.connect(self._handle_preset_selected)

        layout.addWidget(self.lbp_preset_widget)

        # Create payment options container
        payment_container = QFrame()
        payment_container.setStyleSheet(POSStyles.PAYMENT_CONTAINER())
        payment_layout = QVBoxLayout(payment_container)
        payment_layout.setContentsMargins(5, 5, 5, 5)
        payment_layout.setSpacing(10)
        
        # ADD USD widget
        self.cash_usd_widget = CashUSDPaymentWidget()
        # Connect signal from USD widget
        self.cash_usd_widget.payment_requested.connect(
            lambda payment_type: self._on_payment_action(payment_type)
        )
        payment_layout.addWidget(self.cash_usd_widget)
        
        # Add LBP widget
        self.cash_lbp_widget = CashLBPPaymentWidget()
        # Connect signal from LBP widget
        self.cash_lbp_widget.payment_requested.connect(
            lambda payment_type: self._on_payment_action(payment_type)
        )
        payment_layout.addWidget(self.cash_lbp_widget)

        # Create and add card payment widget
        self.card_payment_widget = CardPaymentWidget()
        # Connect signal from card payment widget
        self.card_payment_widget.payment_requested.connect(
            lambda payment_type: self._on_payment_action(payment_type)
        )
        payment_layout.addWidget(self.card_payment_widget)
        
        # Create and add other payment widget
        self.other_payment_widget = OtherPaymentWidget()
        # Connect signal from other payment widget
        self.other_payment_widget.payment_requested.connect(
            lambda payment_type: self._on_payment_action(payment_type)
        )
        payment_layout.addWidget(self.other_payment_widget)
        
        # Add payment container to main layout
        layout.addWidget(payment_container)
        
        # Add totals widget
        self.totals_widget = TotalsWidget(self.exchange_rate)
        layout.addWidget(self.totals_widget)

        return container
    
    def _handle_preset_selected(self, amount):
        """Handle preset amount selection with additive behavior and currency locking"""
        # Determine currency type based on amount
        is_lbp = amount >= 1000  # Simple heuristic to identify LBP
        
        current_value = self.numpad_widget._current_value
        
        # Check if we're starting with a fresh entry or adding to existing
        if current_value == "0":
            # Starting fresh - set the first amount and lock currency type
            new_numeric_value = amount
            self._set_currency_mode(is_lbp)
        else:
            # Adding to existing amount
            try:
                # Convert current value to float, removing any formatting
                current_numeric_value = float(current_value.replace(',', ''))
                # Add the new amount
                new_numeric_value = current_numeric_value + amount
            except ValueError:
                # If there's an error parsing, just use the new amount
                new_numeric_value = amount
                self._set_currency_mode(is_lbp)
        
        # Format the value for display based on currency type
        if is_lbp:
            formatted_value = f"{int(new_numeric_value):,}"
            numerical_value = str(int(new_numeric_value))
            print(f"Updated LBP value: {formatted_value}")  # Debug print
        else:
            formatted_value = f"{new_numeric_value:,.2f}"
            numerical_value = str(new_numeric_value)
            print(f"Updated USD value: ${formatted_value}")  # Debug print
        
        # Update numpad display
        self.numpad_widget._current_value = numerical_value
        self.numpad_widget.display.setText(formatted_value)
        
        # Store the numerical value for payment processing
        self.pending_value = numerical_value

    def _on_numpad_cleared(self):
        """Handle numpad being cleared"""
        # Enable both currency preset buttons
        self._enable_preset_buttons(self.usd_preset_widget, True)
        self._enable_preset_buttons(self.lbp_preset_widget, True)
        self.current_currency_mode = None

    def _set_currency_mode(self, is_lbp):
        """Set currency mode and disable the other currency's presets"""
        if is_lbp:
            # Enable LBP presets, disable USD presets
            self._enable_preset_buttons(self.lbp_preset_widget, True)
            self._enable_preset_buttons(self.usd_preset_widget, False)
            self.current_currency_mode = "LBP"
        else:
            # Enable USD presets, disable LBP presets
            self._enable_preset_buttons(self.usd_preset_widget, True)
            self._enable_preset_buttons(self.lbp_preset_widget, False)
            self.current_currency_mode = "USD"

    def _enable_preset_buttons(self, preset_widget, enabled):
        """Enable or disable all preset buttons in a widget"""
        # Find all QPushButtons in the widget layout
        for i in range(preset_widget.layout().count()):
            item = preset_widget.layout().itemAt(i)
            if item.widget() and isinstance(item.widget(), QPushButton):
                item.widget().setEnabled(enabled)
                if enabled:
                    item.widget().setStyleSheet("""
                        QPushButton {
                            background: white;
                            border: 1px solid #ddd;
                            border-radius: 4px;
                            padding: 5px;
                            font-size: 14px;
                        }
                        QPushButton:hover {
                            background: #f0f0f0;
                            border-color: #1890ff;
                        }
                    """)
                else:
                    item.widget().setStyleSheet("""
                        QPushButton {
                            background: #f5f5f5;
                            border: 1px solid #ddd;
                            border-radius: 4px;
                            padding: 5px;
                            font-size: 14px;
                            color: #999;
                        }
                    """)

    def _create_bottom_bar(self):
        """Create empty bottom bar for future use"""
        bottom_bar = QFrame()
        bottom_bar.setStyleSheet(POSStyles.BOTTOM_BAR(
            self.layout_config.get_pos_layout()['bottom_bar_height']
        ))
        layout = QHBoxLayout(bottom_bar)
        layout.setContentsMargins(10, 5, 10, 10)
        layout.setSpacing(6)
        
        # Add stretch to keep the bar but leave it empty
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

    def _on_payment_action(self, action_type):
        """Handle payment button clicks"""
        try:
            if self.pending_value is not None:
                # First validate the input
                is_valid, message = self.controller.validate_payment_input(
                    action_type, self.pending_value)
                    
                if not is_valid:
                    self._show_validation_message(message)
                    self.pending_value = None
                    self.numpad_widget.clear()
                    return
                    
                # Process the payment
                success, message = self.controller.process_payment(
                    action_type, self.pending_value)
                    
                if not success:
                    self._show_validation_message(message)
                else:
                    print(f"Payment processed: {message}")
                    # Future: Show success message, print receipt, etc.
                    
                self.pending_value = None
                self.numpad_widget.clear()
            else:
                # No amount entered, show message to enter amount first
                self._show_validation_message("Please enter an amount first")
                
        except Exception as e:
            print(f"Error in payment processing: {e}")
            self.pending_value = None
            self.numpad_widget.clear()

    def _filter_products(self, search_text=None):
        """Filter products based on search input"""
        if search_text is None:
            search_text = self.search_input.text()
        
        filtered_products = self.controller.get_filtered_products(search_text)
        self.product_grid.set_search_text(search_text)

    def _handle_product_click(self, item_name):
        """Handle product button click"""
        # If this product is in protection period, ignore the click
        if self.last_numpad_product == item_name and self.button_protection_timer.isActive():
            return

        try:
            # If has pending value from numpad
            if self.pending_value is not None:
                # Validate quantity
                is_valid, message = self.controller.validate_product_quantity(self.pending_value)
                if not is_valid:
                    self._show_validation_message(message)
                    return

                quantity = int(self.pending_value)
                existing_item = self.controller.find_existing_item(item_name)
                if existing_item:
                    self._show_quantity_dialog(item_name, existing_item.quantity, quantity)
                else:
                    success = self.controller.add_product_to_order(item_name, quantity)
                    if not success:
                        self._show_validation_message(f"Failed to add {item_name}")
                    else:
                        self.refresh_order_display()
                
                # Start protection for this product button
                self._protect_button(item_name)
                
                self.pending_value = None
            else:
                # Regular click - add quantity of 1
                success = self.controller.add_product_to_order(item_name)
                if not success:
                    self._show_validation_message(f"Failed to add {item_name}")
                else:
                    self.refresh_order_display()
            
            self.search_input.clear_search()
            self.numpad_widget.clear()
            
        except Exception as e:
            print(f"Error in product click: {e}")
            self.pending_value = None
            self.numpad_widget.clear()

    def refresh_order_display(self):
        """Refresh the order list display from the controller data"""
        # Get current order items from service through controller
        order_summary = self.controller.get_order_summary()
        
        # First clear the current display 
        # We need to directly manipulate the widget to ensure UI is cleared
        self.order_list._clear_display()
        self.order_list.order_items = []
        
        # Re-add each item to the OrderListWidget
        for item_data in order_summary['items']:
            # Create a new OrderItem with proper data
            from models.order_item import OrderItem
            from decimal import Decimal
            
            # Add to internal list first
            item = OrderItem(
                name=item_data['name'],
                price=Decimal(str(item_data['price'])), 
                quantity=item_data['quantity']
            )
            self.order_list.order_items.append(item)
        
        # Update the UI display
        self.order_list._update_display()
        # update totals
        self._update_totals()

    def _protect_button(self, item_name):
        """Request button protection from product grid"""
        self.last_numpad_product = item_name
        self.product_grid.disable_button_temporarily(item_name)
        self.button_protection_timer.start(self.BUTTON_PROTECTION_TIMEOUT_MS)

    def _reset_button_protection(self):
        """Request button protection removal"""
        if self.last_numpad_product:
            self.product_grid.enable_button(self.last_numpad_product)
        self.last_numpad_product = None

    def _show_validation_message(self, message):
        """Show validation message to user"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Input Validation')
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet(OrderWidgetStyles.get_message_box_style())
        msg_box.exec_()
        
        # Clear numpad after validation message
        self.numpad_widget.clear()
        self.pending_value = None

    def _add_product_with_quantity(self, item_name: str, quantity: int):
        """Add new product with specified quantity"""
        
        # Use controller to add product
        success = self.controller.add_product_to_order(item_name, quantity)
        if success:
            self.refresh_order_display()
            
        self.search_input.clear_search()
        self.numpad_widget.clear()

    def _reset_numpad(self):
        """Reset numpad state"""
        self.numpad_widget._current_value = "0"
        self.numpad_widget._update_display()
        self.pending_quantity = None

    def _find_existing_item(self, item_name):
        """Find an existing item in the order list"""
        return self.controller.find_existing_item(item_name)
    
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
        self.numpad_widget.clear()
        self.pending_value = None

    def _update_item_quantity(self, item_name: str, final_quantity: int):
        """Update item quantity in order list"""
        try:
            # Update through controller
            self.controller.update_item_quantity(item_name, final_quantity)
            
            # Refresh the display
            self.refresh_order_display()
            
            self.search_input.clear_search()
            self.numpad_widget.clear()
            
        except Exception as e:
            print(f"Error updating quantity: {e}")  # For debugging
            self.numpad_widget.clear()
            self.pending_value = None

    def _handle_numpad_value_change(self, value: str):
        """Handle numpad value changes"""
        try:
            clean_value = value.strip()
            # Store the raw value - let the action handlers handle validation
            self.pending_value = clean_value if clean_value != '0' else None
        except ValueError:
            self.pending_value = None

    # Event Handlers
    def _on_order_cleared(self):
        """Handle order being cleared"""
        # Clear the order in the service layer
        self.controller.clear_order()
        # Update the UI
        self._update_totals()

    def _on_item_removed(self, item):
        """Handle item removal from order"""
        # Remove the item in the service layer
        self.controller.remove_item_from_order(item)
        # Update the UI
        self._update_totals()

    def _on_order_type_changed(self, order_type):
        """Handle order type changes"""
        self.controller.set_order_type(order_type)

    def _update_totals(self):
        """Update totals display"""
        total_usd = self.controller.get_order_total()
        self.totals_widget.update_totals(total_usd)

    # def _update_time(self):
    #     """Update the time display"""
    #     current = QDateTime.currentDateTime()
    #     self.date_label.setText(current.toString("dd-MM-yyyy"))
    #     self.time_label.setText(current.toString("h:mm AP"))

    def _handle_lock(self):
        """Handle lock button click"""
        from ..view_manager import ViewManager
        ViewManager.get_instance().switch_back_to_pin_view_from_pos(self.user_id)
        self.deleteLater()