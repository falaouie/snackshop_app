from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout,
                             QStackedWidget, QSplitter)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QFont
from datetime import datetime
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
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Left Side - Order Details (40%)
        self.order_widget = self._create_order_widget()
        content_splitter.addWidget(self.order_widget)
        
        # Right Side - Products (60%)
        self.products_widget = self._create_products_widget()
        content_splitter.addWidget(self.products_widget)
        
        # Set split ratio (40:60)
        total_width = self.width()
        content_splitter.setSizes([int(total_width * 0.4), int(total_width * 0.6)])
        
        main_layout.addWidget(content_splitter)

        # Bottom Bar
        self._create_bottom_bar()
        main_layout.addWidget(self.bottom_bar)

    def _create_top_bar(self):
        self.top_bar = QFrame()
        self.top_bar.setStyleSheet(styles.POSStyles.TOP_BAR)
        self.top_bar.setFixedHeight(60)
        
        layout = QHBoxLayout(self.top_bar)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Logo and Cashier Info group
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
        self.time_label = QLabel(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.time_label.setStyleSheet(styles.POSStyles.TOP_BAR_TEXT)
        left_group.addWidget(self.time_label)
        
        layout.addLayout(left_group)
        layout.addStretch()
        
        # Right-side buttons
        for btn_text in ["Back Office", "Lock", "Sign Out"]:
            btn = QPushButton(btn_text)
            btn.setStyleSheet(styles.POSStyles.TOP_BAR_BUTTON)
            btn.setFixedSize(100, 40)
            layout.addWidget(btn)

    def _create_order_widget(self):
        order_frame = QFrame()
        order_frame.setStyleSheet(styles.POSStyles.ORDER_PANEL)
        
        layout = QVBoxLayout(order_frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)  # Remove spacing between elements
        
        # Order Header
        header = QLabel("Current Order")
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

    def _create_products_widget(self):
        products_frame = QFrame()
        products_frame.setStyleSheet(styles.POSStyles.PRODUCTS_PANEL)
        
        layout = QVBoxLayout(products_frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Category Buttons
        category_layout = QHBoxLayout()
        categories = {
            "Sandwiches": ["Chicken Club", "BLT", "Tuna", "Veggie"],
            "Snacks": ["Chips", "Popcorn", "Nuts", "Pretzels"],
            "Beverages": ["Coffee", "Tea", "Soda", "Water"],
            "Desserts": ["Cookies", "Brownies", "Muffins", "Fruit Cup"]
        }
        
        self.category_buttons = []
        for category in categories.keys():
            btn = QPushButton(category)
            btn.setStyleSheet(styles.POSStyles.CATEGORY_BUTTON)
            btn.setFixedHeight(40)
            btn.setCheckable(True)
            category_layout.addWidget(btn)
            self.category_buttons.append(btn)
            
        layout.addLayout(category_layout)
        
        # Products Grid Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(styles.POSStyles.SCROLL_AREA)
        
        self.products_widget = QWidget()
        products_grid = QGridLayout(self.products_widget)
        products_grid.setSpacing(10)
        
        # Sample products for first category
        self._populate_products_grid(categories["Sandwiches"])
        
        scroll_area.setWidget(self.products_widget)
        layout.addWidget(scroll_area)
        
        return products_frame

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