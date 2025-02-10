from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox,
                             QPushButton, QFrame, QScrollArea, QGridLayout, QSplitter,
                             QToolButton, QMenu, QMainWindow, QLineEdit)
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtSvg import QSvgRenderer
from . import styles
# from utilities.utils import ApplicationUtils
from config.screen_config import screen_config

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
        self.keyboard_visible = False
        self.virtual_keyboard = None
        
        # Sample prices (you would typically get these from a database)
        self.prices = {
            "Chicken Club": 8.50,
            "BLT": 6.50,
            "Tuna": 7.00,
            "Veggie": 6.00,
            "Egg Sandwich": 5.50,
            "Steak N Cheese": 9.50,
            "Vegan Sandwich": 7.50,
            "Chips": 2.00,
            "Popcorn": 2.50,
            "Nuts": 3.00,
            "Pretzels": 2.50,
            "Coffee": 3.50,
            "Tea": 2.50,
            "Soda": 2.00,
            "Soda Diet": 2.00,
            "Lemonade": 3.00,
            "Water": 1.50,
            "Cookies": 2.50,
            "Brownies": 3.50,
            "Muffins": 3.00,
            "Fruit Cup": 4.00
        }
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 10)  # Added bottom margin
        main_layout.setSpacing(0)

        # Initialize selected item tracking
        self.selected_item = None
        
        # Add top bar - call only once and store the result
        top_bar_container = self._create_top_bar()
        main_layout.addWidget(top_bar_container)

        # Main Content Area with Splitter
        content_splitter = QSplitter(Qt.Horizontal)
        content_splitter.setStyleSheet("""
            QSplitter::handle {
                background: #DEDEDE;
                width: 1px;
            }
        """)
        
        # Left Side - Order Details
        self.order_widget = self._create_order_widget()
        self.order_widget.setFixedWidth(350)
        content_splitter.addWidget(self.order_widget)
        
        # Middle - Products Grid
        self.products_widget = self._create_products_widget()

        # Create virtual keyboard after products widget
        self.virtual_keyboard = VirtualKeyboard(self)
        self.virtual_keyboard.hide()  # Initially hidden

        content_splitter.addWidget(self.products_widget)
        
        # Add splitter to main layout with spacing at the bottom
        main_layout.addWidget(content_splitter, 1)

        # Create and add bottom bar with proper spacing
        self._create_bottom_bar()
        main_layout.addWidget(self.bottom_bar, 0)

    def _create_top_bar(self):
        """Create top bar with employee info, search, and lock button"""
        self.top_bar = QFrame()
        self.top_bar.setStyleSheet("""
            QFrame {
                background: #F0F0F0;
                border-bottom: 1px solid #DEDEDE;
            }
        """)
        self.top_bar.setFixedHeight(60)
        
        # Main layout
        layout = QHBoxLayout(self.top_bar)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Employee Zone with DateTime
        emp_zone = QFrame()
        emp_zone.setStyleSheet("background: transparent; border: none;")
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
        emp_id.setStyleSheet("color: #333; font-weight: 500;")
        
        # DateTime Zone
        time_zone = QFrame()
        time_zone.setStyleSheet("QFrame { background: transparent; border: none; }")
        time_layout = QVBoxLayout(time_zone)
        time_layout.setContentsMargins(10, 5, 10, 5)
        time_layout.setSpacing(2)
        
        self.date_label = QLabel()
        self.date_label.setStyleSheet("color: #666;")
        
        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: #333; font-weight: 500; padding-left: 4px;")
        
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
        
        # Create search input with embedded icon
        self.search_input = SearchLineEdit()
        self.search_input.textChanged.connect(self._filter_products)
        self.search_input.setPlaceholderText("Search products...")
        self.search_input.setFixedHeight(40)
        
        # Create keyboard toggle button
        keyboard_btn = QPushButton()
        keyboard_btn.setIcon(QIcon("assets/images/keyboard.svg"))
        keyboard_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background: #F8F9FA;
                border-radius: 12px;
            }
        """)
        keyboard_btn.setIconSize(QSize(70, 40))
        keyboard_btn.clicked.connect(self._toggle_keyboard)

        # Add search elements to search layout and keyboard button
        search_layout.addStretch(1)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(keyboard_btn)
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
        lock_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                padding: 0px;
            }
            QPushButton:hover {
                background: rgba(229, 57, 53, 0.1);
                border-radius: 4px;
            }
        """)
        lock_btn.clicked.connect(self._handle_lock)
        
        controls_layout.addWidget(lock_btn)
        
        # Add all zones to main layout
        layout.addWidget(emp_zone)
        layout.addWidget(search_container, 1)  # Give search container stretch priority
        layout.addWidget(controls_zone)
        
        # Timer for updating time
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)
        self._update_time()

        return self.top_bar
    
    def _show_keyboard(self):
        """Show virtual keyboard and set focus"""
        if not self.keyboard_visible:
            self.virtual_keyboard.set_search_input(self.search_input)
            self.virtual_keyboard.show()
            self.keyboard_visible = True

    def _toggle_keyboard(self):
        """Toggle virtual keyboard visibility"""
        if not self.keyboard_visible:
            self._show_keyboard()
        else:
            self.virtual_keyboard.hide()
            self.keyboard_visible = False

    def resizeEvent(self, event):
        """Handle resize events to maintain keyboard positioning"""
        super().resizeEvent(event)
        if self.keyboard_visible and self.virtual_keyboard:
            self.virtual_keyboard.showEvent(event)  # Trigger repositioning

    def _create_order_widget(self):
        """Create order panel"""
        order_frame = QFrame()
        order_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-right: 1px solid #DEDEDE;
            }
        """)
        
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
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: white;
            }
            QScrollBar:vertical {
                border: none;
                background: #F8F9FA;
                width: 8px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #DEDEDE;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        self.order_list_widget = QWidget()
        self.order_list_widget.setStyleSheet("""
            QWidget {
                background: white;
            }
            QLabel {
                padding: 5px;
            }
        """)
        self.order_list_layout = QVBoxLayout(self.order_list_widget)
        self.order_list_layout.setContentsMargins(5, 5, 5, 5)
        self.order_list_layout.setSpacing(5)
        self.order_list_layout.addStretch()
        
        scroll_area.setWidget(self.order_list_widget)
        layout.addWidget(scroll_area)
        
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
        horizontal_buttons = {
            "BTN 1": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
            "BTN 2": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
            "BTN 3": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"}
        }

        for btn_text, colors in horizontal_buttons.items():
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
            btn.setFixedSize(100, 60)
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

    def _update_totals(self):
        """Update the total amounts in USD and LBP"""
        total_usd = sum(item.get_total() for item in self.order_items)
        total_lbp = total_usd * self.exchange_rate
        
        self.usd_amount.setText(f"$ {total_usd:.2f}")
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
        main_layout.setContentsMargins(0, 5, 0, 0)  # Removed bottom margin
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
        self.categories = ["Main", "Sandwiches", "Snacks", "Beverages", "Desserts"]
        self.selected_horizontal_category = None

        for category in self.categories:
            btn = QPushButton(category)
            btn.setStyleSheet("""
                QPushButton {
                    background: white;
                    border: 1px solid #DEDEDE;
                    border-radius: 4px;
                    padding: 4px;
                    color: #333;
                    text-align: center;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background: #F8F9FA;
                    border-color: #2196F3;
                }
            """)
            btn.setFixedSize(120, 40)
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
            btn.setFixedSize(100, 60)

            if btn_text == "VOID":
                btn.clicked.connect(self._clear_order)
            
            button_container.addWidget(btn)
            vertical_layout.addLayout(button_container)

        vertical_layout.addStretch()
        center_layout.addWidget(vertical_section)

        # Products Grid Area
        products_scroll = QScrollArea()
        products_scroll.setWidgetResizable(True)
        products_scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #F8F9FA;
                width: 8px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #DEDEDE;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
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
        self.totals_frame.setStyleSheet("""
            QFrame {
                background: #F8F9FA;
                border-top: 1px solid #DEDEDE;
            }
            QLabel {
                color: #333;
            }
            .currency-usd {
                font-size: 24px;
                font-weight: bold;
                color: #03991f;
            }
            .currency-lbp {
                font-size: 20px;
                color: #666;
            }
        """)
        
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
        button_style = """
            QPushButton {
                background: white;
                border: 1px solid #DEDEDE;
                border-radius: 4px;
                padding: 8px 16px;
                color: #333;
                font-size: 13px;
                height: 36px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #F8F9FA;
                border-color: #2196F3;
            }
            QPushButton:checked {
                background: #2196F3;
                border-color: #2196F3;
                color: white;
            }
        """
        
        # Create order type buttons
        order_types = ["Dine In", "Take-Away", "Delivery"]
        for order_type in order_types:
            btn = QPushButton(order_type)
            btn.setStyleSheet(button_style)
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
        self.usd_amount = QLabel("$ 0.00")
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
        # Update button styles - now handles both horizontal and vertical buttons independently
        if category in self.horizontal_category_buttons:
            # Reset previously selected horizontal button
            if self.selected_horizontal_category:
                self.horizontal_category_buttons[self.selected_horizontal_category].setStyleSheet("""
                    QPushButton {
                        background: white;
                        border: 1px solid #DEDEDE;
                        border-radius: 4px;
                        padding: 8px;
                        color: #333;
                        text-align: center;
                        font-size: 13px;
                    }
                    QPushButton:hover {
                        background: #F8F9FA;
                        border-color: #2196F3;
                    }
                """)
            
            # Update selected horizontal button
            self.horizontal_category_buttons[category].setStyleSheet("""
                QPushButton {
                    background: #2196F3;
                    border: none;
                    border-radius: 4px;
                    padding: 8px;
                    color: white;
                    text-align: center;
                    font-size: 13px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background: #1E88E5;
                }
            """)
            self.selected_horizontal_category = category
            
        # Clear existing products
        for i in reversed(range(self.products_grid.count())):
            widget = self.products_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Sample items (this would typically come from a database)
        items = {
            "Main": ["Chicken Club", "BLT", "Tuna", "Veggie", "Egg Sandwich", "Steak N Cheese", 
                        "Vegan Sandwich", "BLT 2", "Tuna", "Veggie 3", "Egg Sandwich 2", "Steak N Cheese 2",
                        "Vegan Sandwich", "BLT 3", "Tuna", "Another Vegan Sandwich", "Another BLT", "Another Tuna"],
            "Sandwiches": ["Chicken Club6", "BLT5", "Tuna8", "Veggie5", "Egg Sandwich4", 
                        "Steak N Cheese", "Vegan Sandwich"],
            "Snacks": ["Chips", "Popcorn", "Nuts", "Pretzels"],
            "Beverages": ["Coffee", "Tea", "Soda", "Soda Diet", "Lemonade", "Water"],
            "Desserts": ["Cookies", "Brownies", "Muffins", "Fruit Cup"]
        }
        
        # Add product buttons
        for i, item in enumerate(items[category]):
            btn = QPushButton(item)
            btn.setStyleSheet("""
                QPushButton {
                    background: white;
                    border: 1px solid #DEDEDE;
                    border-radius: 16px;
                    padding: 8px;
                    color: #333;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: #F8F9FA;
                    border-color: #2196F3;
                }
                QPushButton:pressed {
                    background: #F1F1F1;
                }
            """)
            btn.setFixedSize(140, 60)
            btn.clicked.connect(lambda checked, name=item: self.add_order_item(name))
            row = i // 3
            col = i % 3
            self.products_grid.addWidget(btn, row, col)
        
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
        self.bottom_bar.setFixedHeight(80)
        self.bottom_bar.setStyleSheet("""
            QFrame {
                background: #F8F9FA;
                border-top: 1px solid #DEDEDE;
                min-height: 80px;
                max-height: 80px;
                margin-bottom: 10px;  /* Add margin to bottom */
            }
        """)
        
        layout = QHBoxLayout(self.bottom_bar)
        layout.setContentsMargins(10, 5, 10, 10)
        layout.setSpacing(6)
        
        layout.addStretch()
        
        # OTHER Payment button
        pay_oth_btn = QPushButton("PAY OTHER")
        pay_oth_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFBF00;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 5px 5px;
                margin-right: 15px;
                font-size: 18px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #FFB300;
            }
        """)
        pay_oth_btn.setFixedSize(140, 50)
        layout.addWidget(pay_oth_btn)

        # Cash Payment button
        pay_cash_btn = QPushButton("PAY CASH")
        pay_cash_btn.setStyleSheet("""
            QPushButton {
                background-color: darkgreen;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 5px 5px;
                font-size: 20px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #48A848;
            }
        """)
        pay_cash_btn.setFixedSize(140, 50)
        layout.addWidget(pay_cash_btn)

    def _update_time(self):
        current = QDateTime.currentDateTime()
        self.date_label.setText(current.toString("dd-MM-yyyy"))
        self.time_label.setText(current.toString("h:mm AP"))

    def on_dots_clicked(self):
        """Handle three dots menu click with various order options"""
        # Create menu
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #DEDEDE;
                border-radius: 4px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
                color: #333;
            }
            QMenu::item:selected {
                background-color: #F0F0F0;
                color: #2196F3;
            }
            QMenu::separator {
                height: 1px;
                background: #DEDEDE;
                margin: 5px 0px;
            }
        """)

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
                QPushButton:hover {
                    background: rgba(229, 57, 53, 0.1);
                    border-radius: 4px;
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
        items = {
            "Main": ["Chicken Club", "BLT", "Tuna", "Veggie", "Egg Sandwich", "Steak N Cheese", 
                    "Vegan Sandwich", "BLT2", "Tuna", "Veggie3", "Egg Sandwich2", "Steak N Cheese 2",
                    "Vegan Sandwich", "BLT3", "Tuna", "Another Vegan Sandwich", "Another BLT", "Another Tuna"],
            "Sandwiches": ["Chicken Club6", "BLT5", "Tuna8", "Veggie5", "Egg Sandwich4", 
                        "Steak N Cheese", "Vegan Sandwich"],
            "Snacks": ["Chips", "Popcorn", "Nuts", "Pretzels"],
            "Beverages": ["Coffee", "Tea", "Soda", "Soda Diet", "Lemonade", "Water"],
            "Desserts": ["Cookies", "Brownies", "Muffins", "Fruit Cup"]
        }
        
        # Filter items based on search text
        filtered_items = [item for item in items[current_category] 
                        if search_text in item.lower()]
        
        # Add filtered product buttons
        for i, item in enumerate(filtered_items):
            btn = QPushButton(item)
            btn.setStyleSheet("""
                QPushButton {
                    background: white;
                    border: 1px solid #DEDEDE;
                    border-radius: 16px;
                    padding: 8px;
                    color: #333;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: #F8F9FA;
                    border-color: #2196F3;
                }
                QPushButton:pressed {
                    background: #F1F1F1;
                }
            """)
            btn.setFixedSize(140, 60)
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
        # Clear search field
        self.search_input.clear()
        # Optionally hide keyboard if it's visible
        # if self.keyboard_visible:
        #     self.virtual_keyboard.hide()
        #     self.keyboard_visible = False

class OrderItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.quantity = 1

    def get_total(self):
        return self.price * self.quantity
    
class SearchLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_view = parent

        # Load search icon (left)
        search_icon = QSvgRenderer("assets/images/search.svg")
        self.search_pixmap = QPixmap(20, 20)
        self.search_pixmap.fill(Qt.transparent)
        painter = QPainter(self.search_pixmap)
        search_icon.render(painter)
        painter.end()
        
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

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.parent_view:
            self.parent_view._show_keyboard()

class VirtualKeyboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_input = None
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(Qt.WA_StyledBackground, True)  # Enable stylesheet on widget
        
        # Initialize animation properties
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(1000)  # 1 second duration
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)  # Smooth easing
        
        self._setup_ui()
        self.hide()

    def _setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        # Close button
        close_btn = QPushButton("×")
        close_btn.setFixedSize(24, 24)
        close_btn.clicked.connect(self._on_close)
        close_btn.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 24px;
                font-weight: bold;
                margin: 5px;
                padding: 0px;
            }
        """)
        
        # Add close button to top-left
        close_layout = QHBoxLayout()
        close_layout.addWidget(close_btn)
        close_layout.addStretch()
        main_layout.addLayout(close_layout)

        # Container for QWERTY and Numpad
        keyboard_container = QHBoxLayout()
        keyboard_container.setSpacing(5)  # Space between QWERTY and numpad

        # QWERTY Section (Left side)
        qwerty_widget = QWidget()
        qwerty_layout = QGridLayout(qwerty_widget)
        qwerty_layout.setSpacing(10)

        # QWERTY Keys
        qwerty_rows = [
            list('QWERTYUIOP'),
            list('ASDFGHJKL'),
            list('ZXCVBNM')
        ]

        # Create and add QWERTY keys
        for row, letters in enumerate(qwerty_rows):
            for col, letter in enumerate(letters):
                btn = QPushButton(letter)
                btn.setFixedSize(50, 50)
                btn.clicked.connect(lambda checked, l=letter: self._on_key_press(l))
                btn.setStyleSheet("""
                    QPushButton {
                        background: white;
                        border: 1px solid #DEDEDE;
                        border-radius: 10px;
                        padding: 8px;
                        color: #333;
                        font-size: 18px;
                    }
                    QPushButton:hover {
                        background: #F8F9FA;
                        border-color: #2196F3;
                    }
                """)
                # Center-align shorter rows
                offset = (10 - len(letters)) // 2 if row == 2 else 0
                qwerty_layout.addWidget(btn, row, col + offset)

        keyboard_container.addWidget(qwerty_widget, stretch=7)

        # Numpad Section (Right side)
        numpad_widget = QWidget()
        numpad_layout = QGridLayout(numpad_widget)
        numpad_layout.setSpacing(10)

        # Numpad keys layout
        numpad_keys = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['CL','0', '⌫']
        ]

        # Create and add numpad keys
        for row, keys in enumerate(numpad_keys):
            for col, key in enumerate(keys):
                btn = QPushButton(key)
                btn.setFixedSize(50, 50)
                if key == '⌫':
                    btn.clicked.connect(self._on_backspace)
                    btn.setStyleSheet("""
                        QPushButton {
                            background: white;
                            border: 1px solid #DEDEDE;
                            border-radius: 10px;
                            padding: 8px;
                            color: #333;
                            font-size: 16px;
                        }
                        QPushButton:hover {
                            background: #F8F9FA;
                            border-color: #2196F3;
                        }
                    """)
                    numpad_layout.addWidget(btn, row + 1, col)
                elif key == 'CL':
                    btn.clicked.connect(self._on_clear) 
                    btn.setStyleSheet("""
                        QPushButton {
                            background: white;
                            border: 1px solid #DEDEDE;
                            border-radius: 10px;
                            padding: 8px;
                            color: #333;
                            font-size: 16px;
                        }
                        QPushButton:hover {
                            background: #F8F9FA;
                            border-color: #2196F3;
                        }
                    """)
                    numpad_layout.addWidget(btn, row + 1, col)
                else:
                    btn.clicked.connect(lambda checked, k=key: self._on_key_press(k))
                    btn.setStyleSheet("""
                        QPushButton {
                            background: white;
                            border: 1px solid #DEDEDE;
                            border-radius: 8px;
                            color: #333;
                            font-size: 16px;
                        }
                        QPushButton:hover {
                            background: #F8F9FA;
                            border-color: #2196F3;
                        }
                    """)
                    numpad_layout.addWidget(btn, row + 1, col)
        
        keyboard_container.addWidget(numpad_widget, stretch=3)

        # Add keyboard container to main layout
        main_layout.addLayout(keyboard_container)

        # Space bar
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(5)

        # Space bar (reduced width)
        space_btn = QPushButton(' ')
        space_btn.setFixedHeight(45)
        space_btn.clicked.connect(lambda: self._on_key_press(' '))
        space_btn.setStyleSheet("""
            QPushButton {
                background: white;
                border: 1px solid #DEDEDE;
                border-radius: 8px;
                color: #333;
                font-size: 14px;
                min-width: 300px;
                margin-left: 40px;
                margin-right: 50px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background: #F8F9FA;
                border-color: #2196F3;
            }
        """)
        bottom_row.addWidget(space_btn, 70)  # 70% width

        # enter button
        enter_btn = QPushButton('↵  ENTER')  # Enter/Return symbol
        enter_btn.setFixedSize(175, 45)
        enter_btn.clicked.connect(self._on_enter)
        enter_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
                margin-right: 15px;
            }
            QPushButton:hover {
                background: #1E88E5;
            }
        """)
        bottom_row.addWidget(enter_btn, 30)  # 30% width

        main_layout.addLayout(bottom_row)

        self.setStyleSheet("""
            VirtualKeyboard {
                background: darkgrey;
                border-top: none;
                border-radius: 10px;
                padding: 10px;
            }
        """)

    def showEvent(self, event):
        """Override show event to animate keyboard sliding up"""
        super().showEvent(event)
        if self.parent():
            self.adjustSize()
            parent = self.parent()
            
            # Calculate final position (where keyboard should end up)
            right_padding = 20
            bottom_padding = 40
            target_x = parent.width() - self.width() - right_padding
            target_y = parent.height() - self.height() - bottom_padding
            
            # Ensure it doesn't go off-screen
            target_x = max(0, target_x)
            target_y = max(0, target_y)
            
            # Set up animation from bottom of screen to target position
            start_rect = QRect(target_x, parent.height(), self.width(), self.height())
            end_rect = QRect(target_x, target_y, self.width(), self.height())
            
            self.animation.setStartValue(start_rect)
            self.animation.setEndValue(end_rect)
            
            # Start animation
            self.animation.start()

        if self.search_input:
            self.search_input.setFocus()

    def hideEvent(self, event):
        """Override hide event to animate keyboard sliding down"""
        super().hideEvent(event)
        if self.parent() and not self.animation.state() == QPropertyAnimation.Running:
            current_geometry = self.geometry()
            end_rect = QRect(
                current_geometry.x(),
                self.parent().height(),
                self.width(),
                self.height()
            )
            
            # Set up hide animation
            self.animation.setStartValue(current_geometry)
            self.animation.setEndValue(end_rect)
            
            # Connect animation finished signal to actually hide the widget
            self.animation.finished.connect(self._finish_hide)
            self.animation.start()
            
            # Don't call parent's hide event yet - wait for animation
            event.ignore()
        else:
            super().hideEvent(event)

    def _finish_hide(self):
        """Called when hide animation completes"""
        super().hide()
        # Disconnect to prevent memory leaks
        try:
            self.animation.finished.disconnect(self._finish_hide)
        except TypeError:
            pass  # In case it's already disconnected

    def show(self):
        """Override show to ensure proper animation handling"""
        if not self.isVisible():
            super().show()
        elif self.animation.state() == QPropertyAnimation.Running:
            self.animation.stop()
            super().show()

    def hide(self):
        """Override hide to start the sliding down animation"""
        if self.isVisible() and self.parent():
            current_geometry = self.geometry()
            end_rect = QRect(
                current_geometry.x(),
                self.parent().height(),
                self.width(),
                self.height()
            )
            
            # Set up hide animation
            self.animation.setStartValue(current_geometry)
            self.animation.setEndValue(end_rect)
            
            # Connect animation finished signal to actually hide the widget
            self.animation.finished.connect(self._finish_hide)
            self.animation.start()
        else:
            super().hide()

    def _on_key_press(self, key):
        """Handle virtual keyboard key presses"""
        if self.search_input:
            # Get current cursor position
            cursor_pos = self.search_input.cursorPosition()
            current_text = self.search_input.text()
            
            # Insert the key at cursor position
            new_text = current_text[:cursor_pos] + key + current_text[cursor_pos:]
            self.search_input.setText(new_text)
            
            # Move cursor after inserted character
            self.search_input.setCursorPosition(cursor_pos + 1)
            self.search_input.setFocus()  # Maintain focus on input

    def _on_backspace(self):
        """Handle virtual keyboard backspace"""
        if self.search_input:
            cursor_pos = self.search_input.cursorPosition()
            current_text = self.search_input.text()
            
            if cursor_pos > 0:
                # Remove character before cursor
                new_text = current_text[:cursor_pos-1] + current_text[cursor_pos:]
                self.search_input.setText(new_text)
                self.search_input.setCursorPosition(cursor_pos - 1)
        self.search_input.setFocus()  # Maintain focus

    def _on_clear(self):
        if self.search_input:
            self.search_input.clear()
            self.search_input.setFocus()

    def _on_enter(self):
        if self.search_input:
            self.hide()
            if self.parent():
                self.parent().keyboard_visible = False

    def set_search_input(self, search_input):
        """Set the input field and ensure it has focus"""
        self.search_input = search_input
        if self.search_input:
            self.search_input.setFocus()
            
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key_Escape:
            self._on_close()
            
    def _on_close(self):
        """Handle closing the keyboard"""
        self.hide()
        if self.parent():
            self.parent().keyboard_visible = False