from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget,
                             QPushButton, QFrame, QScrollArea, QGridLayout, QSplitter)
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime
from PyQt5.QtGui import QPixmap, QIcon
from . import styles
from utilities.utils import ApplicationUtils

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
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Left Side - Order Details
        self.order_widget = self._create_order_widget()
        content_splitter.addWidget(self.order_widget)
        
        # Right Side - Products
        self.products_widget = self._create_products_widget()
        content_splitter.addWidget(self.products_widget)
        
        main_layout.addWidget(content_splitter)

        # Bottom Bar
        self._create_bottom_bar()
        main_layout.addWidget(self.bottom_bar)

    def _create_top_bar(self):
        self.top_bar = QFrame()
        self.top_bar.setStyleSheet(styles.POSStyles.TOP_BAR)
        self.top_bar.setFixedHeight(80)
        
        layout = QHBoxLayout(self.top_bar)
        layout.setContentsMargins(0, 0, 0, 0) # left, top, right, and bottom
        
        # Info group
        left_group = QHBoxLayout()
        
        # Vertical layout for emp_info and time_label
        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(10, 5, 10, 5)  # left, top, right, and bottom
        vertical_layout.setSpacing(0)  # No space between emp_info and time_label

        # Emp Info
        emp_info = QLabel(f"Emp ID: {self.user_id}")
        emp_info.setStyleSheet(styles.POSStyles.TOP_BAR_TEXT)
        emp_info.setFixedHeight(30)
        vertical_layout.addWidget(emp_info)
        
        # Date/Time
        self.time_label = QLabel()
        self.time_label.setStyleSheet(styles.POSStyles.TOP_BAR_TEXT)
        self.time_label.setFixedHeight(20)
        vertical_layout.addWidget(self.time_label)  # Add to left_group instead of main layout
        
        # Add the vertical layout to the left_group
        left_group.addLayout(vertical_layout)
        
        layout.addLayout(left_group)
        layout.addStretch()

        # Timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)
        self._update_time()

        # lock
        lock_label = QLabel()
        pixmap = QPixmap("assets/images/lock_screen.png")
        scaled_pixmap = pixmap.scaled(QSize(75, 100), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        lock_label.setPixmap(scaled_pixmap)
        layout.addWidget(lock_label)
        
        # Exit
        exit_button = QPushButton()

        # Load the pixmap and scale it
        pixmap = QPixmap("assets/images/exit_app.png")
        scaled_pixmap = pixmap.scaled(QSize(150, 75), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Set the scaled pixmap as the icon for the button
        exit_button.setIcon(QIcon(scaled_pixmap))
        exit_button.setIconSize(scaled_pixmap.size())

        # Make the button flat (no border)
        exit_button.setFlat(True)

        # Set the style sheet to remove the background and border
        exit_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: transparent;
                border: none;
            }
            QPushButton:pressed {
                background: transparent;
                border: none;
            }
        """)

        # Connect the button's clicked signal to the close method
        app_utils = ApplicationUtils()
        exit_button.clicked.connect(app_utils.close_application)

        layout.addWidget(exit_button)

    def _update_time(self):
        current = QDateTime.currentDateTime()
        date_str = current.toString("dd-MM-yyyy")
        time_str = current.toString("hh:mm AP")
        self.time_label.setText(f"{date_str} {time_str}")

    def _create_order_widget(self):
        order_frame = QFrame()
        order_frame.setStyleSheet(styles.POSStyles.ORDER_PANEL)
        order_frame.setFixedSize(300, 450)

        layout = QVBoxLayout(order_frame)
        layout.setContentsMargins(0, 0, 0, 0) # left, top, right, and bottom
        layout.setSpacing(0)
        
        # Order Header
        header = QLabel("ORDER # 1234")
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
            row.setContentsMargins(10, 5, 10, 5) # left, top, right, and bottom
            label_widget = QLabel(label)
            label_widget.setAlignment(Qt.AlignRight)
            amount_widget = QLabel(amount)
            amount_widget.setAlignment(Qt.AlignRight)
            # row.addStretch()
            row.addWidget(label_widget)
            
            row.addWidget(amount_widget)
            summary_layout.addLayout(row)
        
        layout.addWidget(summary_frame)
        
        return order_frame

    def _create_products_widget(self):
        products_frame = QFrame()
        products_frame.setStyleSheet(styles.POSStyles.PRODUCTS_PANEL)
        
        # Create main horizontal splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side - Products area with scroll
        products_scroll = QScrollArea()
        products_scroll.setWidgetResizable(True)
        products_scroll.setStyleSheet(styles.POSStyles.SCROLL_AREA)
        
        products_container = QWidget()
        self.products_grid = QGridLayout(products_container)
        self.products_grid.setSpacing(10)
        self.products_grid.setContentsMargins(10, 10, 10, 10)
        products_scroll.setWidget(products_container)
        
        # Right side - Categories
        categories_widget = QWidget()
        categories_layout = QVBoxLayout(categories_widget)
        categories_layout.setSpacing(10)
        categories_layout.setContentsMargins(10, 10, 10, 10)
        

        # Add category buttons
        self.category_buttons = {}
        categories = ["Freq Items", "Sandwiches", "Snacks", "Beverages", "Desserts"]
        self.selected_category = None
        
        for category in categories:
            btn = QPushButton(category)
            btn.setStyleSheet(styles.POSStyles.PRODUCT_BUTTON)
            btn.setFixedHeight(40)
            btn.clicked.connect(lambda checked, c=category: self._show_category_items(c))
            categories_layout.addWidget(btn)
            self.category_buttons[category] = btn
        
        categories_layout.addStretch()
        
        # Add both sides to splitter
        splitter.addWidget(products_scroll)
        splitter.addWidget(categories_widget)
        
        # Set initial splitter sizes (70% products, 30% categories)
        splitter.setSizes([700, 300])
        
        # Add splitter to main layout
        main_layout = QVBoxLayout(products_frame)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(splitter)
        
        # Select first category by default
        QTimer.singleShot(0, lambda: self._show_category_items(categories[0]))
        
        return products_frame
    
    def _show_category_items(self, category):
    # Update button styles
        if self.selected_category:
            self.category_buttons[self.selected_category].setStyleSheet(
                styles.POSStyles.PRODUCT_BUTTON
            )
        
        self.category_buttons[category].setStyleSheet(
            styles.POSStyles.CATEGORY_BUTTON_SELECTED
        )
        self.selected_category = category
        
        # Clear existing products
        for i in reversed(range(self.products_grid.count())):
            widget = self.products_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Sample items (this would typically come from a database)
        items = {
            "Freq Items": ["Chicken Club", "BLT", "Tuna", "Veggie", "Egg Sandwich", "Steak & Cheese", "Vegan Sandwich"],
            "Sandwiches": ["Chicken Club", "BLT", "Tuna", "Veggie", "Egg Sandwich", 
                        "Steak & Cheese", "Vegan Sandwich"],
            "Snacks": ["Chips", "Popcorn", "Nuts", "Pretzels"],
            "Beverages": ["Coffee", "Tea", "Soda", "Soda Diet", "Lemonade", "Water"],
            "Desserts": ["Cookies", "Brownies", "Muffins", "Fruit Cup"]
        }
        
        # Add new products in 3-column grid
        for i, item in enumerate(items[category]):
            btn = QPushButton(item)
            btn.setStyleSheet(styles.POSStyles.PRODUCT_BUTTON)
            btn.setFixedSize(100, 100)
            row = i // 3
            col = i % 3
            self.products_grid.addWidget(btn, row, col)
        
        # Add empty grid items to maintain layout
        remaining_slots = 3 - (len(items[category]) % 3)
        if remaining_slots < 3:
            start_pos = len(items[category])
            for i in range(remaining_slots):
                empty_widget = QWidget()
                row = start_pos // 3
                col = (start_pos + i) % 3
                self.products_grid.addWidget(empty_widget, row, col)

    def _show_categories(self):
        self.stacked_widget.setCurrentIndex(0)

    def _create_bottom_bar(self):
        self.bottom_bar = QFrame()
        self.bottom_bar.setStyleSheet(styles.POSStyles.BOTTOM_BAR)
        # self.bottom_bar.setFixedHeight(60)
        
        layout = QHBoxLayout(self.bottom_bar)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Transaction Controls
        transaction_buttons = ["New Order", "Hold", "Void", "Discount"]
        for btn_text in transaction_buttons:
            btn = QPushButton(btn_text)
            btn.setStyleSheet(styles.POSStyles.BOTTOM_BAR_BUTTON)
            # btn.setFixedSize(100, 40)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Payment Button
        pay_btn = QPushButton("Payment")
        pay_btn.setStyleSheet(styles.POSStyles.PAYMENT_BUTTON)
        # pay_btn.setFixedSize(120, 40)
        layout.addWidget(pay_btn)

    def _populate_products_grid(self, products):
        # Clear existing products
        for i in reversed(range(self.products_widget.layout().count())): 
            self.products_widget.layout().itemAt(i).widget().deleteLater()
        
        # Add new products
        for i, product in enumerate(products):
            btn = QPushButton(product)
            btn.setStyleSheet(styles.POSStyles.PRODUCT_BUTTON)
            # btn.setFixedSize(150, 100)
            self.products_widget.layout().addWidget(btn, i//3, i%3)