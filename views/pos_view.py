from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox,
                             QPushButton, QFrame, QScrollArea, QGridLayout, QSplitter, QToolButton, QMenu)
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
        self.order_widget.setFixedWidth(250)
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
        layout.setContentsMargins(15, 5, 15, 5)
        
        # Employee Zone
        emp_zone = QFrame()
        emp_zone.setStyleSheet("background: transparent; border: none;")
        emp_layout = QHBoxLayout(emp_zone)
        emp_layout.setSpacing(10)
        
        # Employee icon (using SVG)
        emp_icon = QLabel()
        renderer = QSvgRenderer(bytes('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
            <circle cx="16" cy="16" r="16" fill="#2196F3"/>
            <circle cx="16" cy="12" r="6" fill="#FFFFFF"/>
            <path d="M16 19c-5 0-9 2.5-9 6v2h18v-2c0-3.5-4-6-9-6z" fill="#FFFFFF"/>
        </svg>'''.encode()))
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        emp_icon.setPixmap(pixmap)
        
        emp_id = QLabel(f"EMP ID: {self.user_id}")
        emp_id.setStyleSheet("color: #333; font-weight: 500;")
        
        emp_layout.addWidget(emp_icon)
        emp_layout.addWidget(emp_id)
        
        # DateTime Zone
        time_zone = QFrame()
        time_zone.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #DEDEDE;
                border-radius: 4px;
            }
        """)
        time_layout = QHBoxLayout(time_zone)
        time_layout.setContentsMargins(10, 5, 10, 5)
        
        self.date_label = QLabel()
        self.date_label.setStyleSheet("color: #666; margin-right: 10px;")
        
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet("background: #DEDEDE;")
        
        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: #333; font-weight: 500; margin-left: 10px;")
        
        time_layout.addWidget(self.date_label)
        time_layout.addWidget(separator)
        time_layout.addWidget(self.time_label)
        
        # Controls Zone
        controls_zone = QFrame()
        controls_layout = QHBoxLayout(controls_zone)
        controls_layout.setSpacing(15)
        
        # Lock button with modern style
        lock_btn = QPushButton()
        lock_btn.setIcon(QIcon("assets/images/lock_screen.png"))
        lock_btn.setIconSize(QSize(24, 24))
        lock_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 0.05);
                border-radius: 4px;
            }
        """)
        
        # Exit button with modern style
        exit_btn = QPushButton()
        exit_btn.setIcon(QIcon("assets/images/exit_app.png"))
        exit_btn.setIconSize(QSize(24, 24))
        exit_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 0.05);
                border-radius: 4px;
            }
        """)
        app_utils = ApplicationUtils()
        exit_btn.clicked.connect(app_utils.close_application)
        
        controls_layout.addWidget(lock_btn)
        controls_layout.addWidget(exit_btn)
        
        # Add all zones to layout
        layout.addWidget(emp_zone)
        layout.addStretch()
        layout.addWidget(time_zone)
        layout.addStretch()
        layout.addWidget(controls_zone)
        
        # Timer for updating time
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)
        self._update_time()

    def _create_order_widget(self):
        """Create order panel with enhanced USD display"""
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
                border-bottom: 1px solid #DEDEDE;
            }
            QLabel {
                color: #2196F3;
                font-size: 16px;
                font-weight: 500;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 10, 10, 10)
        
        order_label = QLabel("ORDER # 1234")
        
        menu_btn = QToolButton()
        menu_btn.setText("⋮")
        menu_btn.setStyleSheet("""
            QToolButton {
                border: none;
                color: #666;
                font-size: 20px;
                padding: 5px;
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
        main_layout = QHBoxLayout(products_frame)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Products Grid Area (Middle)
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
        
        # Categories Panel (Right)
        categories_panel = QFrame()
        categories_panel.setFixedWidth(120)
        categories_panel.setStyleSheet("""
            QFrame {
                background: white;
                border-left: 1px solid #DEDEDE;
            }
        """)
        
        categories_layout = QVBoxLayout(categories_panel)
        categories_layout.setContentsMargins(8, 8, 8, 8)
        categories_layout.setSpacing(8)
        
        # Categories with modern styling
        self.category_buttons = {}
        self.categories = ["Freq Items", "Sandwiches", "Snacks", "Beverages", "Desserts"]
        self.selected_category = None
        
        for category in self.categories:
            btn = QPushButton(category)
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
            btn.clicked.connect(lambda checked, c=category: self._show_category_items(c))
            categories_layout.addWidget(btn)
            self.category_buttons[category] = btn
        
        categories_layout.addStretch()
        
        # Add widgets to main layout
        main_layout.addWidget(products_scroll, 1)  # Products grid takes available space
        main_layout.addWidget(categories_panel)   # Fixed width categories panel
        
        # Initialize first category after the buttons are created
        self._show_category_items(self.categories[0])
        
        return products_frame

    def _show_category_items(self, category):
        """Display product items for selected category"""
        # Update button styles
        if self.selected_category:
            self.category_buttons[self.selected_category].setProperty("selected", False)
            self.category_buttons[self.selected_category].setStyleSheet("""
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
        
        self.category_buttons[category].setProperty("selected", True)
        self.category_buttons[category].setStyleSheet("""
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
        self.selected_category = category
        
        # Clear existing products
        for i in reversed(range(self.products_grid.count())):
            widget = self.products_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Sample items
        items = {
            "Freq Items": ["Chicken Club", "BLT", "Tuna", "Veggie", "Egg Sandwich", "Steak N Cheese", 
                          "Vegan Sandwich", "BLT", "Tuna", "Veggie", "Egg Sandwich", "Steak & Cheese"],
            "Sandwiches": ["Chicken Club", "BLT", "Tuna", "Veggie", "Egg Sandwich", 
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
                    border-radius: 4px;
                    padding: 8px;
                    color: #333;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background: #F8F9FA;
                    border-color: #2196F3;
                }
                QPushButton:pressed {
                    background: #F1F1F1;
                }
            """)
            btn.setFixedSize(100, 50)
            btn.clicked.connect(lambda checked, name=item: self.add_order_item(name))  # Connect click to add_order_item
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
        layout.setSpacing(10)
        
        # Transaction buttons with modern styling
        transaction_buttons = {
            "Hold": {"bg": "#FFC107", "hover": "#FFB300", "text": "#000000"},
            "Void": {"bg": "#F44336", "hover": "#E53935", "text": "#FFFFFF"},
            "Discount": {"bg": "#4CAF50", "hover": "#43A047", "text": "#FFFFFF"},
            "BLANK1": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
            "BLANK2": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"},
            "BLANK3": {"bg": "#9E9E9E", "hover": "#757575", "text": "#FFFFFF"}
        }

        for btn_text, colors in transaction_buttons.items():
            btn = QPushButton(btn_text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {colors['bg']};
                    color: {colors['text']};
                    border: none;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 13px;
                    font-weight: 500;
                    min-height: 60px;
                    max-height: 60px;
                }}
                QPushButton:hover {{
                    background-color: {colors['hover']};
                }}
            """)
            btn.setFixedSize(70, 60)
            
            # Connect void functionality to the Void button
            if btn_text == "Void":
                btn.clicked.connect(self._void_selected_item)
                
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Payment button with enhanced styling
        pay_btn = QPushButton("Payment")
        pay_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 14px;
                font-weight: 500;
                min-height: 60px;
                max-height: 60px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        pay_btn.setFixedSize(120, 60)
        layout.addWidget(pay_btn)

    def _update_time(self):
        current = QDateTime.currentDateTime()
        self.date_label.setText(current.toString("dd-MM-yyyy"))
        self.time_label.setText(current.toString("hh:mm AP"))

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
        clear_action = menu.addAction("Clear Order")
        clear_action.setIcon(QIcon("assets/images/clear.png"))  # Assuming you have this icon
        
        # Show menu at button position
        action = menu.exec_(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))
        
        # Handle menu actions
        if action == clear_action:
            self._clear_order()

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

class OrderItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.quantity = 1

    def get_total(self):
        return self.price * self.quantity