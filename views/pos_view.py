from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox,
                             QPushButton, QFrame, QScrollArea, QGridLayout, QSplitter, QToolButton, QMenu, QMainWindow)
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor, QFont, QLinearGradient
from PyQt5.QtSvg import QSvgRenderer
from . import styles
from utilities.utils import ApplicationUtils
from config.screen_config import screen_config

class POSView(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.screen_config = screen_config
        self.order_items = []  # List to store order items
        self.exchange_rate = 90000  # LBP per USD
        
        # Add these new attributes for tracking horizontal category buttons
        self.horizontal_category_buttons = {}
        self.selected_horizontal_category = None
        
        # Existing attributes
        self.category_buttons = {}
        self.selected_category = None
        
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
        
        # Top Bar
        self._create_top_bar()
        main_layout.addWidget(self.top_bar)

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
        content_splitter.addWidget(self.products_widget)
        
        # Add splitter to main layout with spacing at the bottom
        main_layout.addWidget(content_splitter, 1)

        # Create and add bottom bar with proper spacing
        self._create_bottom_bar()
        main_layout.addWidget(self.bottom_bar, 0)

    def _create_top_bar(self):
        """Create modern top bar with distinct zones"""
        self.top_bar = QFrame()
        self.top_bar.setStyleSheet("""
            QFrame {
                background: #F0F0F0;
                border-bottom: 1px solid #DEDEDE;
            }
        """)
        self.top_bar.setFixedHeight(60)
        
        layout = QHBoxLayout(self.top_bar)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Employee Zone with DateTime
        emp_zone = QFrame()
        emp_zone.setStyleSheet("background: transparent; border: none;")
        emp_layout = QHBoxLayout(emp_zone)
        emp_layout.setSpacing(8)
        emp_layout.setContentsMargins(0, 0, 0, 0) 
        
        # Employee icon (using SVG)
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
        
        # DateTime Zone - Now vertically aligned
        time_zone = QFrame()
        time_zone.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)
        time_layout = QVBoxLayout(time_zone)  # Changed to QVBoxLayout for vertical alignment
        time_layout.setContentsMargins(10, 5, 10, 5)
        time_layout.setSpacing(2)  # Reduced spacing between date and time
        
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

        # First VLine separator after employee zone
        first_separator = QFrame()
        first_separator.setFrameShape(QFrame.VLine)
        first_separator.setStyleSheet("""
            background: #DEDEDE;
            margin-top: 10px;
            margin-bottom: 10px;
        """)

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

        # Center buttons zone
        center_buttons_zone = QFrame()
        center_buttons_layout = QHBoxLayout(center_buttons_zone)
        center_buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add initial spacer
        center_buttons_layout.addStretch(1)
        
        # Create order type buttons
        order_types = ["Dine In", "Take-Away", "Delivery"]
        for i, order_type in enumerate(order_types):
            btn = QPushButton(order_type)
            btn.setStyleSheet(button_style)
            btn.setCheckable(True)
            btn.setFixedWidth(100)  # Fixed width for all buttons
            center_buttons_layout.addWidget(btn)
            if order_type == "Dine In":
                btn.setChecked(True)
                
            # Add spacer after each button
            center_buttons_layout.addStretch(1)
        
        # Controls Zone
        controls_zone = QFrame()
        controls_layout = QHBoxLayout(controls_zone)
        controls_layout.setSpacing(8)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        
        # Second VLine separator before controls
        second_separator = QFrame()
        second_separator.setFrameShape(QFrame.VLine)
        second_separator.setStyleSheet("""
            background: #DEDEDE;
            margin-top: 10px;
            margin-bottom: 10px;
        """)

        # Lock button with modern style
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
        
        # Add all zones to layout
        layout.addWidget(emp_zone)
        # layout.addWidget(first_separator)
        layout.addWidget(center_buttons_zone)
        # layout.addWidget(second_separator)
        layout.addWidget(controls_zone)
        
        # Timer for updating time
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)
        self._update_time()

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
        
        # Totals Section
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
                font-size: 18px;
                font-weight: bold;
                color: #2196F3;
            }
            .currency-lbp {
                font-size: 14px;
                color: #666;
            }
        """)
        totals_layout = QVBoxLayout(self.totals_frame)
        totals_layout.setContentsMargins(15, 10, 15, 10)
        totals_layout.setSpacing(8)
        
        
        # USD Total (Primary)
        usd_layout = QHBoxLayout()
        usd_label = QLabel("Total USD")
        self.usd_amount = QLabel("$0.00")  # Store as instance attribute
        self.usd_amount.setProperty("class", "currency-usd")
        usd_layout.addWidget(usd_label)
        usd_layout.addStretch()
        usd_layout.addWidget(self.usd_amount)
        
        # LBP Total (Secondary)
        lbp_layout = QHBoxLayout()
        lbp_label = QLabel("Total LBP")
        self.lbp_amount = QLabel("0")  # Store as instance attribute
        self.lbp_amount.setProperty("class", "currency-lbp")
        lbp_layout.addWidget(lbp_label)
        lbp_layout.addStretch()
        lbp_layout.addWidget(self.lbp_amount)
        
        totals_layout.addLayout(usd_layout)
        totals_layout.addLayout(lbp_layout)
        
        layout.addWidget(self.totals_frame)
        
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
        total_label = QLabel(f"${item.get_total():.2f}")
        total_label.setAlignment(Qt.AlignRight)
        total_label.setFixedWidth(60)
        
        item_layout.addWidget(qty_label)
        item_layout.addWidget(name_label)
        item_layout.addWidget(total_label)
        
        # Store reference to the order item
        item_widget.order_item = item
        
        # Add click handling
        item_widget.mousePressEvent = lambda event, widget=item_widget: self._on_item_clicked(widget)
        
        self.order_list_layout.addWidget(item_widget)
        self.order_list_layout.addStretch()

    def _on_item_clicked(self, clicked_widget):
        """Handle item selection"""
        # Deselect all other items
        for i in range(self.order_list_layout.count()):
            widget = self.order_list_layout.itemAt(i).widget()
            if widget and isinstance(widget, QFrame):
                widget.setProperty('selected', False)
                widget.style().unpolish(widget)
                widget.style().polish(widget)
        
        # Select clicked item
        clicked_widget.setProperty('selected', True)
        clicked_widget.style().unpolish(clicked_widget)
        clicked_widget.style().polish(clicked_widget)
        
        # Store reference to selected item
        self.selected_item = clicked_widget

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
        
        self.usd_amount.setText(f"${total_usd:.2f}")
        self.lbp_amount.setText(f"{total_lbp:,.0f}")
    
    def _create_products_widget(self):
        """Create products panel with modern styling"""
        products_frame = QFrame()
        products_frame.setStyleSheet("""
            QFrame {
                background: #F8F9FA;
            }
        """)
        
        # Main layout for products area
        main_layout = QVBoxLayout(products_frame)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Horizontal Categories Row - Full width including right panel space
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

        # Container for products grid and right panel
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)

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
        content_layout.addWidget(products_scroll, 1)

        # Right side buttons panel
        right_panel = QFrame()
        right_panel.setFixedWidth(120)
        right_panel.setStyleSheet("""
            QFrame {
                background: white;
                border-left: 1px solid #DEDEDE;
            }
        """)
        
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(8, 8, 8, 8)
        right_layout.setSpacing(8)
        
        # Add spacing widget to push down the first button
        # spacer = QWidget()
        # spacer.setFixedHeight(48)  # Height of category button + spacing
        # right_layout.addWidget(spacer)
        
        # Generic buttons for right panel
        for i in range(5):
            btn = QPushButton(f"Button {i+1}")
            btn.setStyleSheet("""
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
            btn.setFixedHeight(40)
            right_layout.addWidget(btn)

        right_layout.addStretch()
        
        content_layout.addWidget(right_panel)
        
        # Add content container to main layout
        main_layout.addWidget(content_container, 1)
        
        # Initialize first category
        self._show_category_items(self.categories[0])
        
        return products_frame

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
                        "Vegan Sandwich", "BLT2", "Tuna", "Veggie3", "Egg Sandwich2", "Steak N Cheese 2",
                        "Vegan Sandwich", "BLT3", "Tuna", "Veggie4", "Egg Sandwich3", "Steak N Cheese 3"],
            "Sandwiches": ["Chicken Club6", "BLT5", "Tuna8", "Veggie5", "Egg Sandwich4", 
                        "Steak N Cheese", "Vegan Sandwich"],
            "Snacks": ["Chips", "Popcorn", "Nuts", "Pretzels"],
            "Beverages": ["Coffee", "Tea", "Soda", "Soda Diet", "Lemonade", "Water"],
            "Desserts": ["Cookies", "Brownies", "Muffins", "Fruit Cup"]
        }
        
        # Add product buttons with modern styling
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
        """Create bottom action bar with modern styling and proper margins"""
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
        layout.setContentsMargins(10, 5, 10, 10)  # Increased bottom margin to 10
        layout.setSpacing(6)
        
        # Transaction buttons with modern styling
        transaction_buttons = {
            "Hold": {"bg": "#FFC107", "hover": "#FFB300", "text": "#000000"},
            "VOID": {"bg": "#F44336", "hover": "#E53935", "text": "#FFFFFF"},
            "DISCOUNT": {"bg": "#4CAF50", "hover": "#43A047", "text": "#FFFFFF"},
            "PAID IN": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
            "PAID OUT": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
            "NO SALE": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"}
        }

        for btn_text, colors in transaction_buttons.items():
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
                    min-height: 60px;
                    max-height: 60px;
                }}
                QPushButton:hover {{
                    background-color: {colors['hover']};
                }}
            """)
            btn.setFixedSize(90, 40)
            
            # Connect void functionality to the Void button
            if btn_text == "VOID":
                btn.clicked.connect(self._clear_order)
                # btn.clicked.connect(self._void_selected_item)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # CREDIT Payment button
        pay_crd_btn = QPushButton("CREDIT")
        pay_crd_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFBF00;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 14px;
                font-weight: 500;
                min-height: 60px;
                max-height: 60px;
            }
            QPushButton:hover {
                background-color: #FFB300;
            }
        """)
        pay_crd_btn.setFixedSize(120, 40)
        layout.addWidget(pay_crd_btn)

        # Cash Payment button
        pay_cash_btn = QPushButton("CASH")
        pay_cash_btn.setStyleSheet("""
            QPushButton {
                background-color: darkgreen;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 20px;
                font-weight: 500;
                min-height: 60px;
                max-height: 60px;
            }
            QPushButton:hover {
                background-color: #48A848;
            }
        """)
        pay_cash_btn.setFixedSize(120, 40)
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
        clear_action.setIcon(QIcon("assets/images/clear.png"))  # Assuming you have this icon
        
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

class OrderItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.quantity = 1

    def get_total(self):
        return self.price * self.quantity