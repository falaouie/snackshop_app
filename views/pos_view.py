from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QPushButton, QFrame, QScrollArea, QGridLayout, QSplitter,
                             QToolButton, QMenu, QMainWindow, QWidget)
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtSvg import QSvgRenderer
from components.keyboard import KeyboardEnabledInput, VirtualKeyboard, KeyboardType
from button_definitions.types import (
    PaymentButtonType,
    TransactionButtonType,
    HorizontalButtonType,
    OrderButtonType,
    ProductButtonType,
    CategoryButtonType
)
from button_definitions.payment import PaymentButtonConfig
from button_definitions.transaction import TransactionButtonConfig
from button_definitions.order import OrderButtonConfig
from button_definitions.horizontal import HorizontalButtonConfig
from button_definitions.product import ProductButtonConfig
from button_definitions.category import CategoryButtonConfig
from styles.buttons import ButtonStyles
from styles import POSStyles, AppStyles
# from config.screen_config import screen_config
from models.product_catalog import (
    CATEGORIES,
    PRODUCTS_BY_CATEGORY,
    PRODUCT_PRICES,
    get_products_for_category,
    get_product_price
)

from styles.layouts import layout_config

class POSView(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.layout_config = layout_config.get_instance()
        self.order_items = []
        self.exchange_rate = 90000
        self.horizontal_category_buttons = {}
        self.selected_horizontal_category = None
        self.category_buttons = {}
        self.selected_category = None
        self.categories = CATEGORIES 
        self.keyboard = VirtualKeyboard(self)
        
        # Use imported prices
        self.prices = PRODUCT_PRICES

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000) 

        self._setup_ui()
        self._update_time()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 10)  # Added bottom margin
        main_layout.setSpacing(0)

        self.keyboard = VirtualKeyboard(self)

        # Initialize selected item tracking
        self.selected_item = None
        
        # Add top bar - call only once and store the result
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
        
        # Middle - Products Grid
        self.products_widget = self._create_products_widget()
        
        content_splitter.addWidget(self.products_widget)
        
        # Add splitter to main layout with spacing at the bottom
        main_layout.addWidget(content_splitter, 1)

        # Create and add bottom bar with proper spacing
        self._create_bottom_bar()
        main_layout.addWidget(self.bottom_bar, 0)

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
        emp_layout.addWidget(time_zone)  # Changed from time_layout to time_zone

        # Search Section (Centered)
        search_container = QFrame()
        search_container.setStyleSheet("background: transparent;")
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create search input
        self.search_input = SearchLineEdit(self)
        self.search_input.setPlaceholderText("Search products...")
        self.search_input.setStyleSheet(POSStyles.SEARCH_INPUT(
            pos_layout['search_input']['width'],
            pos_layout['search_input']['height']
        ))

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
        layout.addWidget(search_container, 1)  # Give search container stretch priority
        layout.addWidget(controls_zone)
        
        return self.top_bar

    def _create_order_widget(self):
        """Create order panel"""
        order_frame = QFrame()
        order_frame.setStyleSheet(POSStyles.ORDER_PANEL(
            self.layout_config.get_pos_layout()['order_panel_width']
        ))
        
        layout = QVBoxLayout(order_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Order Header
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
        header_layout.setContentsMargins(10, 5, 0, 5)  # left, top, right, and bottom
        
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
        menu_btn.clicked.connect(self.on_dots_clicked)
        
        header_layout.addWidget(order_label)
        header_layout.addStretch()
        header_layout.addWidget(menu_btn)
        
        layout.addWidget(header_frame)
        
        # Order Items Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)   
        scroll_area.setStyleSheet(POSStyles.SCROLL_AREA)
        self.order_list_widget = QWidget()
        self.order_list_widget.setStyleSheet(POSStyles.ORDER_LIST_WIDGET)
        self.order_list_layout = QVBoxLayout(self.order_list_widget)
        self.order_list_layout.setContentsMargins(5, 5, 5, 5)
        self.order_list_layout.setSpacing(5)
        self.order_list_layout.addStretch()
        
        scroll_area.setWidget(self.order_list_widget)
        layout.addWidget(scroll_area)
        
        # Add quantity summary
        self.quantity_summary = self._create_quantity_summary()
        layout.addWidget(self.quantity_summary)

        # Add horizontal buttons section
        horizontal_buttons_frame = QFrame()
        horizontal_buttons_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-left: 1px solid #DEDEDE;
                border-top: 1px solid #DEDEDE;
            }
        """)
        
        horizontal_layout = QHBoxLayout(horizontal_buttons_frame)
        horizontal_layout.setContentsMargins(0, 10, 0, 10)
        horizontal_layout.setSpacing(8)
        
        for button_type in HorizontalButtonType:
            config = HorizontalButtonConfig.get_config(button_type)
            btn = QPushButton(config['text'])
            btn.setStyleSheet(ButtonStyles.get_horizontal_button_style(button_type))
            button_config = self.layout_config.get_button_config('horizontal')
            btn.setFixedSize(
                button_config['width'],
                button_config['height']
            )
            if config['action']:
                btn.clicked.connect(getattr(self, config['action']))
            horizontal_layout.addWidget(btn)
        
        layout.addWidget(horizontal_buttons_frame)

        return order_frame
    
    def add_order_item(self, item_name):
        """Add an item to the order or increment its quantity if it exists"""
        # Find if item already exists in order
        existing_item = None
        for item in self.order_items:
            if item.name == item_name:
                existing_item = item
                break
        
        if existing_item:
            existing_item.quantity += 1
            self._update_order_display()
        else:
            # Create new order item
            price = self.prices.get(item_name, 0)
            new_item = OrderItem(item_name, price)
            self.order_items.append(new_item)
            self._add_item_to_display(new_item)
            # Update quantity summary when adding new item
            self._update_quantity_summary()
        
        self._update_totals()

    def _add_item_to_display(self, item):
        """Add a new item row to the order display"""
        # Remove stretch if exists
        for i in reversed(range(self.order_list_layout.count())):
            if self.order_list_layout.itemAt(i).widget() is None:
                self.order_list_layout.takeAt(i)
        
        # Create item row
        item_widget = QFrame()
        item_widget.setProperty('selected', False)  # Track selection state
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

    def _on_item_clicked(self, widget, event):
        """Handle item selection but allow the event to propagate."""
        if event.button() == Qt.LeftButton:
            # Handle item selection
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

        # Pass event to the default handler
        QWidget.mousePressEvent(widget, event)


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

    def _update_totals(self):
        """Update the total amounts in USD and LBP"""
        total_usd = sum(item.get_total() for item in self.order_items)
        total_lbp = total_usd * self.exchange_rate
        
        self.usd_amount.setText(f"${total_usd:.2f}")
        self.lbp_amount.setText(f"LBP {total_lbp:,.0f}")
    
    def _create_products_widget(self):
        """Create products panel"""
        products_frame = QFrame()
        products_frame.setStyleSheet("""
            QFrame {
                background: #F8F9FA;
            }
        """)
        
        # Main layout for products area
        main_layout = QVBoxLayout(products_frame)
        main_layout.setContentsMargins(0, 5, 0, 0)
        main_layout.setSpacing(8)

        # Horizontal Categories Row
        horizontal_categories = QFrame()
        horizontal_categories.setStyleSheet("""
            QFrame {
                background: transparent;
            }
        """)
        horizontal_layout = QHBoxLayout(horizontal_categories)
        horizontal_layout.setContentsMargins(5, 0, 5, 0)
        horizontal_layout.setSpacing(8)

        # Horizontal category buttons
        self.horizontal_category_buttons = {}

        # self.categories = CATEGORIES

        self.selected_horizontal_category = None

        for category in self.categories:
            config = CategoryButtonConfig.get_config(
                CategoryButtonType.CATEGORY,
                category
            )
            btn = QPushButton(config['text'])
            
            # Initial style (unselected)
            grid_config = self.layout_config.get_product_grid_config()
            btn.setStyleSheet(ButtonStyles.get_category_button_style(is_selected=False))
            btn.setFixedSize(
                grid_config['category_button']['width'],
                grid_config['category_button']['height']
            )
            
            btn.clicked.connect(lambda checked, c=category: self._show_category_items(c))
            horizontal_layout.addWidget(btn)
            self.horizontal_category_buttons[category] = btn

        horizontal_layout.addStretch()
        main_layout.addWidget(horizontal_categories)

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

        # Create vertical buttons section
        vertical_section = QFrame()
        vertical_layout = QVBoxLayout(vertical_section)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.setSpacing(8)

        for button_type in TransactionButtonType:
            config = TransactionButtonConfig.get_config(button_type)
            btn = QPushButton(config['text'])
            btn.setStyleSheet(ButtonStyles.get_transaction_button_style(button_type))
            button_config = self.layout_config.get_button_config('transaction')
            btn.setFixedSize(
                button_config['width'],
                button_config['height']
            )
            if config['action']:
                btn.clicked.connect(getattr(self, config['action']))
            vertical_layout.addWidget(btn)

        vertical_layout.addStretch()
        center_layout.addWidget(vertical_section)

        # Products Grid Area
        products_scroll = QScrollArea()
        products_scroll.setWidgetResizable(True)
        products_scroll.setStyleSheet(POSStyles.SCROLL_AREA)
        
        products_container = QWidget()
        self.products_grid = QGridLayout(products_container)
        self.products_grid.setSpacing(10)
        self.products_grid.setContentsMargins(5, 5, 5, 5)
        products_scroll.setWidget(products_container)
        
        # Add products scroll area to content layout
        content_layout.addWidget(center_panel)
        content_layout.addWidget(products_scroll, 1)

        # Add content container to main layout
        main_layout.addWidget(content_container, 1)
        
        # Create and add totals frame with order type buttons
        totals_frame = self._create_totals_frame()
        main_layout.addWidget(totals_frame)
        
        # Initialize first category
        self._show_category_items(self.categories[0])
        
        return products_frame
    
    def _create_totals_frame(self):
        """Create totals frame with order type buttons and amounts"""
        self.totals_frame = QFrame()
        self.totals_frame.setStyleSheet(POSStyles.TOTALS_FRAME)
        
        # Main horizontal layout
        totals_layout = QHBoxLayout(self.totals_frame)
        totals_layout.setContentsMargins(15, 10, 15, 10)
        totals_layout.setSpacing(20)  # Increased spacing between sections

        # Order Type Buttons Section (Left)
        order_buttons_container = QFrame()
        order_buttons_layout = QHBoxLayout(order_buttons_container)
        order_buttons_layout.setContentsMargins(0, 0, 0, 0)
        order_buttons_layout.setSpacing(10)

        button_style = ButtonStyles.get_order_button_style()
        button_config = self.layout_config.get_button_config('order_type')

        for button_type in OrderButtonType:
            config = OrderButtonConfig.get_config(button_type)
            btn = QPushButton(config['text'])
            btn.setStyleSheet(button_style)
            btn.setFixedSize(
                button_config['width'],
                button_config['height']
            )
            btn.setCheckable(True)
            if config.get('default_selected', False):
                btn.setChecked(True)
            if config['action']:
                btn.clicked.connect(getattr(self, config['action']))
            order_buttons_layout.addWidget(btn)
        
        # Amounts Section (Right)
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
        
        # Add layouts to amounts container
        amounts_layout.addLayout(usd_layout)
        amounts_layout.addLayout(lbp_layout)
        
        # Add sections to main layout
        totals_layout.addWidget(order_buttons_container)
        totals_layout.addStretch(1)  # Add stretch to push amounts to the right
        totals_layout.addWidget(amounts_container)
        
        return self.totals_frame

    def _show_category_items(self, category):
        """Display product items for selected category"""
        # 1. Update horizontal category button styles
        if category in self.horizontal_category_buttons:
            # Reset previously selected button
            if self.selected_horizontal_category:
                prev_btn = self.horizontal_category_buttons[self.selected_horizontal_category]
                prev_btn.setStyleSheet(ButtonStyles.get_category_button_style(is_selected=False))
            
            # Update newly selected button
            curr_btn = self.horizontal_category_buttons[category]
            curr_btn.setStyleSheet(ButtonStyles.get_category_button_style(is_selected=True))
            self.selected_horizontal_category = category

        # 2. Clear existing products grid
        for i in reversed(range(self.products_grid.count())):
            widget = self.products_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # 3. Get items and apply search filter
        items = PRODUCTS_BY_CATEGORY[category]
        search_text = self.search_input.text().strip().lower()
        filtered_items = items
        if search_text:
            filtered_items = [item for item in items if search_text in item.lower()]

        # 4. Get the base product button style once for all buttons
        product_style = ButtonStyles.get_product_button_style()

        # 5. Create and add product buttons to grid
        for i, item in enumerate(filtered_items):
            # Get product configuration with category context
            product_config = ProductButtonConfig.get_config(
                ProductButtonType.PRODUCT,
                item, 
                category
            )
            
            # Create button with product config
            btn = QPushButton(product_config['text'])
            btn.setStyleSheet(product_style)
            grid_config = self.layout_config.get_product_grid_config()
            btn.setFixedSize(
                grid_config['product_button']['width'],
                grid_config['product_button']['height']
            )
            # Use lambda with default argument to capture current item value
            btn.clicked.connect(lambda checked, name=item: self._handle_product_click(name))
            
            # Calculate grid position
            row = i // 3  # 3 columns per row
            col = i % 3
            self.products_grid.addWidget(btn, row, col)

        # 6. Fill empty grid slots to maintain layout
        remaining_slots = 3 - (len(filtered_items) % 3)
        if remaining_slots < 3:
            start_pos = len(filtered_items)
            for i in range(remaining_slots):
                empty_widget = QWidget()
                row = start_pos // 3
                col = (start_pos + i) % 3
                self.products_grid.addWidget(empty_widget, row, col)

        # 7. Add stretch to bottom of grid
        self.products_grid.setRowStretch(self.products_grid.rowCount(), 1)
        
    def _create_bottom_bar(self):
        """Create bottom action bar"""
        self.bottom_bar = QFrame()
        self.bottom_bar.setStyleSheet(POSStyles.BOTTOM_BAR(
            self.layout_config.get_pos_layout()['bottom_bar_height']
        ))
        layout = QHBoxLayout(self.bottom_bar)
        layout.setContentsMargins(10, 5, 10, 10)
        layout.setSpacing(6)
        
        layout.addStretch()

        for button_type in PaymentButtonType:
            config = PaymentButtonConfig.get_config(button_type)
            btn = QPushButton(config['text'])
            btn.setStyleSheet(ButtonStyles.get_payment_button_style(button_type))
            button_config = self.layout_config.get_button_config('payment')
            btn.setFixedSize(
                button_config['width'],
                button_config['height']
            )
            
            if config['action']:
                btn.clicked.connect(getattr(self, config['action']))
            layout.addWidget(btn)


    def _update_time(self):
        current = QDateTime.currentDateTime()
        self.date_label.setText(current.toString("dd-MM-yyyy"))
        self.time_label.setText(current.toString("h:mm AP"))

    def on_dots_clicked(self):
        """Handle three dots menu click with various order options"""
        # Create menu
        menu = QMenu(self)
        menu.setStyleSheet(POSStyles.MENU)

        # Add Clear Order action
        clear_action = menu.addAction("Cancel Order")
        clear_item = menu.addAction("Remove Selected Item")
        clear_action.setIcon(QIcon("assets/images/clear.png"))
        
        # Show menu at button position
        action = menu.exec_(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))
        
        # Handle menu actions
        if action == clear_action:
            self._clear_order()
        
        if action == clear_item:
            self._void_selected_item()

    def _clear_order(self):
        """Clear all items from the current order"""
        # Show confirmation dialog
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
            
            # Update display
            self._update_order_display()
            self._update_totals()
            self._update_quantity_summary() 

    def _void_selected_item(self):
        """Remove the selected item from the order"""
        if self.selected_item and hasattr(self.selected_item, 'order_item'):
            # Remove item from order items list
            self.order_items.remove(self.selected_item.order_item)
            
            # Clear selection
            self.selected_item = None
            
            # Update display
            self._update_order_display()
            self._update_totals()

    def _handle_lock(self):
        """Handle lock button click - return to PIN view"""
        # Import here to avoid circular import
        from .view_manager import ViewManager
        ViewManager.get_instance().switch_back_to_pin_view_from_pos(self.user_id)
        # Delete current POS view
        self.deleteLater()

    def _filter_products(self):
        """Filter products based on search input"""
        search_text = self.search_input.text().lower()
        current_category = self.selected_horizontal_category or self.categories[0]
        
        # Clear existing products
        for i in reversed(range(self.products_grid.count())):
            widget = self.products_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Get items for current category
        items = PRODUCTS_BY_CATEGORY
        
        # Filter items based on search text
        filtered_items = [item for item in items[current_category] 
                        if search_text in item.lower()]
        
        # Add filtered product buttons
        for i, item in enumerate(filtered_items):
            btn = QPushButton(item)
            grid_config = self.layout_config.get_product_grid_config()
            btn.setFixedSize(
                grid_config['product_button']['width'],
                grid_config['product_button']['height']
            )
            btn.setStyleSheet(ButtonStyles.get_product_button_style())
            btn.clicked.connect(lambda checked, name=item: self._handle_product_click(name))
            row = i // 3
            col = i % 3
            self.products_grid.addWidget(btn, row, col)
        
        # Fill empty slots
        remaining_slots = 3 - (len(filtered_items) % 3)
        if remaining_slots < 3:
            start_pos = len(filtered_items)
            for i in range(remaining_slots):
                empty_widget = QWidget()
                row = start_pos // 3
                col = (start_pos + i) % 3
                self.products_grid.addWidget(empty_widget, row, col)
        
        self.products_grid.setRowStretch(self.products_grid.rowCount(), 1)

    def _handle_product_click(self, item_name):
        """Handle product button click - add item and clear search"""
        self.add_order_item(item_name)
        # Clear search field and reshow all items in current category
        self.search_input.clear()
        self._show_category_items(self.selected_horizontal_category)

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
    
    def process_cash_payment(self):
        """Handle cash payment"""
        # Implement cash payment logic
        print("Cash button clicked")

    def process_other_payment(self):
        """Handle other payment types"""
        # Implement other payment logic
        print("Other Payment button clicked")

    def hold_transaction(self):
        """Handle hold transaction"""
        # Implement hold logic
        print("Hold horizontal button clicked")

    def void_transaction(self):
        """Handle void transaction"""
        # Implement void logic
        print("Void horizontal button clicked")

    def paid_in(self):
        """Handle paid in"""
        # Implement paid in logic
        print("Paid in button clicked")

    def paid_out(self):
        """Handle paid out"""
        # Implement paid out logic
        print("Paid out button clicked")

    def no_sale(self):
        """Handle no sale"""
        # Implement no sale logic
        print("No Sale horizontal button clicked")

    def apply_discount(self):
        """Handle discount"""
        # Implement discount logic
        print("Discount button clicked")

    def show_numpad(self):
        """Show numpad"""
        # Implement numpad display logic
        print("num pad button clicked")

    def set_dine_in(self):
        """Handle dine in order type selection"""
        print("Dine in button clicked")

    def set_take_away(self):
        """Handle take away order type selection"""
        print("Take away button clicked")

    def set_delivery(self):
        """Handle delivery order type selection"""
        print("Delivery button clicked")

    def hold_order(self):
        """Handle hold order action"""
        print("Hold button clicked")

    def void_order(self):
        """Handle void order action"""
        print("Void button clicked")

    def no_sale(self):
        """Handle no sale order action"""
        print("No Sale button clicked")

class OrderItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.quantity = 1

    def get_total(self):
        return self.price * self.quantity
    
class SearchLineEdit(KeyboardEnabledInput):
    def __init__(self, parent=None):
        super().__init__(parent, style_type='search', keyboard_type=KeyboardType.FULL)
        self.parent_view = parent
        
        # Load search icon (left)
        search_icon = QSvgRenderer("assets/images/search.svg")
        self.search_pixmap = QPixmap(20, 20)
        self.search_pixmap.fill(Qt.transparent)
        painter = QPainter(self.search_pixmap)
        search_icon.render(painter)
        painter.end()

        # Connect text changed signal for filtering
        self.textChanged.connect(parent._filter_products)
        
        # Adjust style to leave space for both icons
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DEDEDE;
                border-radius: 20px;
                padding: 8px 40px 8px 40px; /* Left 40px for search, Right 40px for backspace */
                font-size: 14px;
                color: #333;
                min-width: 300px;
                max-width: 400px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                outline: none;
            }
        """)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.drawPixmap(12, (self.height() - 20) // 2, self.search_pixmap)