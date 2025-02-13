from components.keyboard import KeyboardEnabledInput, VirtualKeyboard, KeyboardType
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QPushButton, QFrame, QScrollArea, QGridLayout, QSplitter,
                             QToolButton, QMenu, QMainWindow, qApp)
from components.keyboard import KeyboardEnabledInput
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime, QEvent
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtSvg import QSvgRenderer
from . import styles
# from utilities.utils import ApplicationUtils
from config.screen_config import screen_config
from models.product_catalog import (
    CATEGORIES,
    PRODUCTS_BY_CATEGORY,
    PRODUCT_PRICES,
    get_products_for_category,
    get_product_price
)
from models.button_definitions import (
    ORDER_TYPES,
    HORIZONTAL_BUTTONS,
    TRANSACTION_BUTTONS,
    PAYMENT_BUTTONS
)

class POSView(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.screen_config = screen_config
        self.order_items = []
        self.exchange_rate = 90000
        self.horizontal_category_buttons = {}
        self.selected_horizontal_category = None
        self.category_buttons = {}
        self.selected_category = None

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
        content_splitter.setStyleSheet(styles.POSStyles.SPLITTER)
        
        # Left Side - Order Details
        self.order_widget = self._create_order_widget()
        self.order_widget.setFixedWidth(self.screen_config.get_size('pos_order_panel_width'))
        self.order_widget.setStyleSheet(styles.POSStyles.ORDER_PANEL)
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
        self.top_bar = QFrame()
        self.top_bar.setStyleSheet(styles.POSStyles.TOP_BAR)
        self.top_bar.setFixedHeight(self.screen_config.get_size('pos_top_bar_height'))
        
        # Main layout
        layout = QHBoxLayout(self.top_bar)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Employee Zone with DateTime
        emp_zone = QFrame()
        emp_zone.setStyleSheet(styles.POSStyles.EMPLOYEE_ZONE)
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
        emp_id.setStyleSheet(styles.POSStyles.EMPLOYEE_ID)
        
        # DateTime Zone
        time_zone = QFrame()
        time_zone.setStyleSheet(styles.POSStyles.DATE_TIME_ZONE)
        time_layout = QVBoxLayout(time_zone)
        time_layout.setContentsMargins(10, 5, 10, 5)
        time_layout.setSpacing(2)

        self.date_label = QLabel()
        self.date_label.setStyleSheet(styles.POSStyles.DATE_LABEL)

        self.time_label = QLabel()
        self.time_label.setStyleSheet(styles.POSStyles.TIME_LABEL)

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
        self.search_input.setFixedSize(
            self.screen_config.get_size('pos_search_input_width'),
            self.screen_config.get_size('pos_search_input_height')
        )
        self.search_input.setStyleSheet(styles.POSStyles.SEARCH_INPUT)

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
        lock_btn.setStyleSheet(styles.POSStyles.LOCK_BUTTON)
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
        order_frame.setStyleSheet(styles.POSStyles.ORDER_PANEL)
        
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
        scroll_area.setStyleSheet(styles.POSStyles.SCROLL_AREA)
        self.order_list_widget = QWidget()
        self.order_list_widget.setStyleSheet(styles.POSStyles.ORDER_LIST_WIDGET)
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
        
        # Add the horizontal buttons
        # horizontal_buttons = {
        #     "BTN 1": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
        #     "BTN 2": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
        #     "BTN 3": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"}
        # }

        for btn_text, colors in HORIZONTAL_BUTTONS.items():
            btn = QPushButton(btn_text)
            btn.setStyleSheet(styles.POSStyles.get_action_button_style(btn_text, colors))
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
        self.categories = CATEGORIES
        self.selected_horizontal_category = None

        for category in self.categories:
            btn = QPushButton(category)
            btn.setFixedSize(
                self.screen_config.get_size('pos_category_button_width'),
                self.screen_config.get_size('pos_category_button_height')
            )
            btn.setStyleSheet(styles.POSStyles.HORIZONTAL_CATEGORY_BUTTON)
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

        # Vertical transaction buttons
        transaction_buttons = {
            "Hold": {"bg": "#FFC107", "hover": "#FFB300", "text": "#000000"},
            "VOID": {"bg": "#F44336", "hover": "#E53935", "text": "#FFFFFF"},
            "PAID IN": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
            "PAID OUT": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
            "NO SALE": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
            "DISCOUNT": {"bg": "#4CAF50", "hover": "#43A047", "text": "#FFFFFF"},
            "Blank": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
            "NUM PAD": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"}
        }

        # Create vertical buttons section
        vertical_section = QFrame()
        vertical_layout = QVBoxLayout(vertical_section)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.setSpacing(8)

        for btn_text, colors in transaction_buttons.items():
            button_container = QHBoxLayout()
            button_container.setContentsMargins(0, 0, 0, 0)

            btn = QPushButton(btn_text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {colors['bg']};
                    color: {colors['text']};
                    border: none;
                    border-radius: 10px;
                    padding: 5px;
                    margin: 3px;
                    font-size: 13px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: {colors['hover']};
                }}
            """)
            btn.setFixedSize(100, 50)

            if btn_text == "VOID":
                btn.clicked.connect(self._clear_order)
            
            button_container.addWidget(btn)
            vertical_layout.addLayout(button_container)

        vertical_layout.addStretch()
        center_layout.addWidget(vertical_section)

        # Products Grid Area
        products_scroll = QScrollArea()
        products_scroll.setWidgetResizable(True)
        products_scroll.setStyleSheet(styles.POSStyles.SCROLL_AREA)
        
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
        self.totals_frame.setStyleSheet(styles.POSStyles.TOTALS_FRAME)
        
        # Main horizontal layout
        totals_layout = QHBoxLayout(self.totals_frame)
        totals_layout.setContentsMargins(15, 10, 15, 10)
        totals_layout.setSpacing(20)  # Increased spacing between sections
        
        # Order Type Buttons Section (Left)
        order_buttons_container = QFrame()
        order_buttons_layout = QHBoxLayout(order_buttons_container)
        order_buttons_layout.setContentsMargins(0, 0, 0, 0)
        order_buttons_layout.setSpacing(10)
        
        # Button styles
        # button_style = """
        #     QPushButton {
        #         background: white;
        #         border: 1px solid #DEDEDE;
        #         border-radius: 4px;
        #         padding: 8px 16px;
        #         color: #333;
        #         font-size: 13px;
        #         height: 36px;
        #         min-width: 100px;
        #     }
        #     QPushButton:hover {
        #         background: #F8F9FA;
        #         border-color: #2196F3;
        #     }
        #     QPushButton:checked {
        #         background: #2196F3;
        #         border-color: #2196F3;
        #         color: white;
        #     }
        # """
        
        # Create order type buttons
        # order_types = ["Dine In", "Take-Away", "Delivery"]
        for order_type in ORDER_TYPES:
            btn = QPushButton(order_type)
            btn.setStyleSheet(styles.POSStyles.ORDER_TYPE_BUTTON)
            btn.setCheckable(True)
            if order_type == "Dine In":
                btn.setChecked(True)
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
        # Update button styles - handles horizontal buttons
        if category in self.horizontal_category_buttons:
            # Reset previously selected horizontal button style
            if self.selected_horizontal_category:
                self.horizontal_category_buttons[self.selected_horizontal_category].setStyleSheet(
                    styles.POSStyles.HORIZONTAL_CATEGORY_BUTTON
                )
            
            # Update selected horizontal button style
            self.horizontal_category_buttons[category].setStyleSheet(
                styles.POSStyles.HORIZONTAL_CATEGORY_BUTTON_SELECTED
            )
            self.selected_horizontal_category = category
            
        # Clear existing products
        for i in reversed(range(self.products_grid.count())):
            widget = self.products_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Get items for current category from product catalog
        items = PRODUCTS_BY_CATEGORY

        # Apply current search filter if exists
        search_text = self.search_input.text().strip()
        if search_text:
            # Filter items based on search text
            filtered_items = [item for item in items[category] 
                            if search_text.lower() in item.lower()]
            
            # Add filtered product buttons
            for i, item in enumerate(filtered_items):
                btn = QPushButton(item)
                btn.setFixedSize(
                    self.screen_config.get_size('pos_product_button_width'),
                    self.screen_config.get_size('pos_product_button_height')
                )
                btn.setStyleSheet(styles.POSStyles.PRODUCT_BUTTON)
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
        else:
            # Add all product buttons for category
            for i, item in enumerate(items[category]):
                btn = QPushButton(item)
                btn.setFixedSize(
                    self.screen_config.get_size('pos_product_button_width'),
                    self.screen_config.get_size('pos_product_button_height')
                )
                btn.setStyleSheet(styles.POSStyles.PRODUCT_BUTTON)
                btn.clicked.connect(lambda checked, name=item: self._handle_product_click(name))
                row = i // 3
                col = i % 3
                self.products_grid.addWidget(btn, row, col)
            
            # Fill empty slots
            remaining_slots = 3 - (len(items[category]) % 3)
            if remaining_slots < 3:
                start_pos = len(items[category])
                for i in range(remaining_slots):
                    empty_widget = QWidget()
                    row = start_pos // 3
                    col = (start_pos + i) % 3
                    self.products_grid.addWidget(empty_widget, row, col)

        self.products_grid.setRowStretch(self.products_grid.rowCount(), 1)
        
        # Fill empty slots
        remaining_slots = 3 - (len(items[category]) % 3)
        if remaining_slots < 3:
            start_pos = len(items[category])
            for i in range(remaining_slots):
                empty_widget = QWidget()
                row = start_pos // 3
                col = (start_pos + i) % 3
                self.products_grid.addWidget(empty_widget, row, col)

    def _create_bottom_bar(self):
        """Create bottom action bar"""
        self.bottom_bar = QFrame()
        bottom_bar_height = self.screen_config.get_size('pos_bottom_bar_height')
        self.bottom_bar.setStyleSheet(
            styles.POSStyles.BOTTOM_BAR.format(
                height=bottom_bar_height
            )
        )
        layout = QHBoxLayout(self.bottom_bar)
        layout.setContentsMargins(10, 5, 10, 10)
        layout.setSpacing(6)
        
        layout.addStretch()
        
        # OTHER Payment button
        pay_oth_btn = QPushButton("PAY OTHER")
        pay_oth_btn.setStyleSheet(styles.POSStyles.get_pay_button_style("other"))
        pay_oth_btn.setFixedSize(
            self.screen_config.get_size('pos_action_button_width'),
            self.screen_config.get_size('pos_action_button_height')
        )
        layout.addWidget(pay_oth_btn)

        # Cash Payment button
        pay_cash_btn = QPushButton("PAY CASH")
        pay_cash_btn.setStyleSheet(styles.POSStyles.get_pay_button_style("cash"))
        pay_cash_btn.setFixedSize(
            self.screen_config.get_size('pos_action_button_width'),
            self.screen_config.get_size('pos_action_button_height')
        )
        layout.addWidget(pay_cash_btn)

    def _update_time(self):
        current = QDateTime.currentDateTime()
        self.date_label.setText(current.toString("dd-MM-yyyy"))
        self.time_label.setText(current.toString("h:mm AP"))

    def on_dots_clicked(self):
        """Handle three dots menu click with various order options"""
        # Create menu
        menu = QMenu(self)
        menu.setStyleSheet(styles.POSStyles.MENU)

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
        # Get the main window
        main_window = self.parent()
        while main_window and not isinstance(main_window, QMainWindow):
            main_window = main_window.parent()
            
        if main_window:
            # Create central widget to hold everything
            central_widget = QWidget()
            main_window.setCentralWidget(central_widget)
            main_layout = QVBoxLayout(central_widget)
            main_layout.setContentsMargins(20, 20, 20, 20)
            
            # Top bar with logo
            top_bar = QHBoxLayout()
            
            # Logo
            logo_label = QLabel()
            pixmap = QPixmap("assets/images/silver_system_logo.png")
            scaled_pixmap = pixmap.scaled(
                QSize(screen_config.get_size('logo_width'), 
                    screen_config.get_size('logo_height')),
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setStyleSheet(styles.AppStyles.LOGO_CONTAINER)
            top_bar.addWidget(logo_label)
            top_bar.addStretch()
            
            # Exit button
            exit_btn = QPushButton()
            renderer = QSvgRenderer("assets/images/exit_app.svg")
            pixmap = QPixmap(150, 150)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            exit_btn.setIcon(QIcon(pixmap))
            exit_btn.setIconSize(QSize(150, 150))
            exit_btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    padding: 0px;
                }
            """)
            from utilities.utils import ApplicationUtils
            app_utils = ApplicationUtils()
            exit_btn.clicked.connect(app_utils.close_application)
            top_bar.addWidget(exit_btn)
            
            main_layout.addLayout(top_bar)
            main_layout.addStretch()
            
            # Center container horizontally
            center_layout = QHBoxLayout()
            center_layout.addStretch()
            
            # Import and create auth container here to avoid circular import
            from .auth_view import AuthenticationContainer
            auth_container = AuthenticationContainer()
            auth_container.setFocusPolicy(Qt.StrongFocus)  # Enable keyboard focus
            auth_container.switch_to_pin_view(self.user_id)
            center_layout.addWidget(auth_container)
            
            center_layout.addStretch()
            main_layout.addLayout(center_layout)
            main_layout.addStretch()
            
            # Ensure proper focus chain
            auth_container.setFocus()
            auth_container.pin_view.setFocus()  # Give focus to pin view specifically
            
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
            btn.setFixedSize(
                    self.screen_config.get_size('pos_product_button_width'),
                    self.screen_config.get_size('pos_product_button_height')
                )
            btn.setStyleSheet(styles.POSStyles.PRODUCT_BUTTON)
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