from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget,
                             QPushButton, QFrame, QScrollArea, QGridLayout, QSplitter)
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime
from PyQt5.QtGui import QPixmap
from . import styles

class POSView(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Bar
        self._create_top_bar()
        main_layout.addWidget(self.top_bar)
        
        # Main Content Area with Splitter
        # content_splitter = QSplitter(Qt.Horizontal)
        
        # Left Side - Order Details (30%)
        self.order_widget = self._order_details_widget()
        main_layout.addWidget(self.order_widget)
        
        # Middle - Numbers Section (5%)
        self.numbers_widget = self._create_numbers_widget()
        # content_splitter.addWidget(self.numbers_widget)
        
        # Right Side - Products (65%)
        self.products_widget = self._create_products_widget()
        # content_splitter.addWidget(self.products_widget)
        
        # Set split proportions (30:5:65)
        # content_splitter.setSizes([300, 50, 650])
        
        # main_layout.addWidget(content_splitter)
        main_layout.addStretch()

        # Bottom Bar
        self._create_bottom_bar()
        main_layout.addWidget(self.bottom_bar)

    def _create_top_bar(self):
        self.top_bar = QFrame()
        self.top_bar.setStyleSheet(styles.POSStyles.TOP_BAR)
        self.top_bar.setFixedHeight(60)
        
        layout = QHBoxLayout(self.top_bar)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Logo and Info group
        left_group = QHBoxLayout()
        
        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("assets/images/silver_system_logo.png")
        scaled_pixmap = pixmap.scaled(QSize(100, 50), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        left_group.addWidget(logo_label)
        
        # Cashier Info
        cashier_info = QLabel(f"Cashier ID: {self.user_id}")
        cashier_info.setStyleSheet(styles.POSStyles.TOP_BAR_TEXT)
        left_group.addWidget(cashier_info)
        
        # Date/Time
        self.time_label = QLabel()
        self.time_label.setStyleSheet(styles.POSStyles.TOP_BAR_TEXT)
        left_group.addWidget(self.time_label)  # Add to left_group instead of main layout
        
        # Timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)
        self._update_time()
        
        layout.addLayout(left_group)
        layout.addStretch()
        
        # Right-side buttons
        for btn_text in ["Back Office", "Lock", "Sign Out"]:
            btn = QPushButton(btn_text)
            btn.setStyleSheet(styles.POSStyles.TOP_BAR_BUTTON)
            btn.setFixedSize(100, 40)
            layout.addWidget(btn)

    def _update_time(self):
        current = QDateTime.currentDateTime()
        date_str = current.toString("dd-MM-yyyy")
        time_str = current.toString("hh:mm:ss AP")
        self.time_label.setText(f"{date_str} {time_str}")

    def _order_details_widget(self):
        order_frame = QFrame()
        order_frame.setStyleSheet(styles.POSStyles.ORDER_PANEL)
        
        layout = QVBoxLayout(order_frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)
        
        # Order Header
        header = QLabel("Order Details")
        header.setStyleSheet(styles.POSStyles.SECTION_HEADER)
        layout.addWidget(header)
        
        # Order Items List with scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(styles.POSStyles.SCROLL_AREA)
        
        order_list = QWidget()
        order_list.setStyleSheet("background: white;")
        scroll_area.setWidget(order_list)
        layout.addWidget(scroll_area)
        
        # Order Summary
        summary_frame = QFrame()
        summary_frame.setStyleSheet(styles.POSStyles.SUMMARY_PANEL)
        summary_layout = QVBoxLayout(summary_frame)
        summary_layout.setSpacing(10)
        
        # Add subtotal, tax, total with consistent alignment
        for label, amount in [("Subtotal", "$0.00"), ("Tax (5%)", "$0.00"), ("Total", "$0.00")]:
            row = QHBoxLayout()
            row.setContentsMargins(10, 5, 10, 5)
            label_widget = QLabel(label)
            amount_widget = QLabel(amount)
            amount_widget.setAlignment(Qt.AlignRight)
            row.addWidget(label_widget)
            row.addStretch()
            row.addWidget(amount_widget)
            summary_layout.addLayout(row)
        
        layout.addWidget(summary_frame)
        
        return order_frame
    
    def _create_numbers_widget(self):
        numbers_frame = QFrame()
        numbers_frame.setStyleSheet(styles.POSStyles.NUMBERS_PANEL)
        
        layout = QVBoxLayout(numbers_frame)
        layout.setContentsMargins(5, 10, 5, 10)
        
        # Add stretch to push keypad to bottom
        layout.addStretch()
        
        # Numbers grid for 1-9
        grid = QGridLayout()
        grid.setSpacing(5)
        
        # Add number buttons 1-9
        for i in range(9):
            row = i // 3
            col = i % 3
            btn = QPushButton(str(i + 1))
            btn.setFixedSize(40, 40)
            btn.setStyleSheet(styles.POSStyles.NUMBER_BUTTON)
            grid.addWidget(btn, row, col)
        
        layout.addLayout(grid)
        
        # Bottom row with arrows and 0
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(5)
        
        # Down arrow, 0, Up arrow
        btn_down = QPushButton("▼")
        btn_0 = QPushButton("0")
        btn_up = QPushButton("▲")
        
        for btn in [btn_down, btn_0, btn_up]:
            btn.setFixedSize(40, 40)
            btn.setStyleSheet(styles.POSStyles.NUMBER_BUTTON)
            bottom_row.addWidget(btn)
        
        layout.addLayout(bottom_row)
        return numbers_frame

    def _create_products_widget(self):
        products_frame = QFrame()
        products_frame.setStyleSheet(styles.POSStyles.PRODUCTS_PANEL)
        
        self.products_layout = QVBoxLayout(products_frame)
        self.products_layout.setContentsMargins(10, 10, 10, 10)
        self.products_layout.setSpacing(0)
        
        self.stacked_widget = QStackedWidget()
        
        # Categories page
        categories_page = QWidget()
        categories_layout = QVBoxLayout(categories_page)
        categories_layout.setSpacing(0)
        categories_layout.setContentsMargins(0, 0, 0, 0)
        
        # Quick Actions header
        quick_header = QFrame()
        quick_header.setStyleSheet(styles.POSStyles.HEADER_FRAME)
        quick_header_layout = QVBoxLayout(quick_header)
        quick_header_layout.setContentsMargins(10, 5, 10, 5)
        
        quick_label = QLabel("Quick Actions")
        quick_label.setStyleSheet(styles.POSStyles.SECTION_HEADER)
        quick_header_layout.addWidget(quick_label)
        
        categories_layout.addWidget(quick_header)
        
        # Quick items row
        quick_items = QGridLayout()
        quick_items.setSpacing(10)
        quick_items.setContentsMargins(10, 10, 10, 0)
        for i in range(5):
            btn = QPushButton(f"Item {i+1}")
            btn.setStyleSheet(styles.POSStyles.PRODUCT_BUTTON)
            btn.setFixedSize(150, 100)
            quick_items.addWidget(btn, 0, i)
        categories_layout.addLayout(quick_items)
        
        # Categories header
        cat_header = QFrame()
        cat_header.setStyleSheet(styles.POSStyles.HEADER_FRAME)
        cat_header_layout = QVBoxLayout(cat_header)
        cat_header_layout.setContentsMargins(10, 5, 10, 5)
        
        categories_label = QLabel("Categories")
        categories_label.setStyleSheet(styles.POSStyles.SECTION_HEADER)
        cat_header_layout.addWidget(categories_label)
        
        categories_layout.addWidget(cat_header)
        
        # Categories grid
        categories_grid = QGridLayout()
        categories_grid.setSpacing(10)
        categories_grid.setContentsMargins(10, 10, 10, 10)
        
        categories = ["Sandwiches", "Snacks", "Beverages", "Desserts"]
        position = 0
        
        # Add category buttons
        for category in categories:
            btn = QPushButton(category)
            btn.setStyleSheet(styles.POSStyles.PRODUCT_BUTTON)
            btn.setFixedSize(150, 100)
            btn.clicked.connect(lambda checked, c=category: self._show_category_items(c))
            categories_grid.addWidget(btn, position // 5, position % 5)
            position += 1
        
        # Add empty buttons to fill grid (30 total slots)
        while position < 25:  # 6 rows of 5
            btn = QPushButton()
            btn.setEnabled(False)
            btn.setFixedSize(150, 100)
            btn.setStyleSheet(styles.POSStyles.PRODUCT_BUTTON_DISABLED)
            categories_grid.addWidget(btn, position // 5, position % 5)
            position += 1
        
        categories_layout.addLayout(categories_grid)
        
        # Items pages
        self.items_pages = {}
        for category in categories:
            page = self._create_items_page(category)
            self.items_pages[category] = page
        
        self.stacked_widget.addWidget(categories_page)
        for page in self.items_pages.values():
            self.stacked_widget.addWidget(page)
        
        self.products_layout.addWidget(self.stacked_widget)
        return products_frame

    def _create_items_page(self, category):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(10)
        
        # Back button
        back_btn = QPushButton("BACK")
        back_btn.setFixedSize(100, 40)
        back_btn.setStyleSheet(styles.POSStyles.BACK_BUTTON)
        back_btn.clicked.connect(self._show_categories)
        layout.addWidget(back_btn)
        
        # Items grid
        items_grid = QGridLayout()
        items_grid.setSpacing(10)
        
        # Sample items
        items = {
            "Sandwiches": ["Chicken Club", "BLT", "Tuna", "Veggie"],
            "Snacks": ["Chips", "Popcorn", "Nuts", "Pretzels"],
            "Beverages": ["Coffee", "Tea", "Soda", "Water"],
            "Desserts": ["Cookies", "Brownies", "Muffins", "Fruit Cup"]
        }
        
        position = 0
        for item in items[category]:
            btn = QPushButton(item)
            btn.setStyleSheet(styles.POSStyles.PRODUCT_BUTTON)
            btn.setFixedSize(150, 100)
            items_grid.addWidget(btn, position // 5, position % 5)
            position += 1
        
        layout.addLayout(items_grid)
        layout.addStretch()
        return page
    
    def _show_category_items(self, category):
        self.stacked_widget.setCurrentWidget(self.items_pages[category])

    def _show_categories(self):
        self.stacked_widget.setCurrentIndex(0)

    def _create_bottom_bar(self):
        self.bottom_bar = QFrame()
        self.bottom_bar.setStyleSheet(styles.POSStyles.BOTTOM_BAR)
        self.bottom_bar.setFixedHeight(60)
        
        layout = QHBoxLayout(self.bottom_bar)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Transaction Controls
        transaction_buttons = ["New Order", "Hold", "Void", "Discount"]
        for btn_text in transaction_buttons:
            btn = QPushButton(btn_text)
            btn.setStyleSheet(styles.POSStyles.BOTTOM_BAR_BUTTON)
            btn.setFixedSize(100, 40)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Payment Button
        pay_btn = QPushButton("Payment")
        pay_btn.setStyleSheet(styles.POSStyles.PAYMENT_BUTTON)
        pay_btn.setFixedSize(120, 40)
        layout.addWidget(pay_btn)

    def _populate_products_grid(self, products):
        # Clear existing products
        for i in reversed(range(self.products_widget.layout().count())): 
            self.products_widget.layout().itemAt(i).widget().deleteLater()
        
        # Add new products
        for i, product in enumerate(products):
            btn = QPushButton(product)
            btn.setStyleSheet(styles.POSStyles.PRODUCT_BUTTON)
            btn.setFixedSize(150, 100)
            self.products_widget.layout().addWidget(btn, i//3, i%3)