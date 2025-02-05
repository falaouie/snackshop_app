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
        
        # Left Side - Order Details (Fixed width)
        self.order_widget = self._create_order_widget()
        self.order_widget.setFixedWidth(300)
        content_splitter.addWidget(self.order_widget)
        
        # Middle - Products Grid
        self.products_widget = self._create_products_widget()
        content_splitter.addWidget(self.products_widget)
        
        # Right Side - Categories (Fixed width)
        self.categories_widget = self._create_categories_widget()
        self.categories_widget.setFixedWidth(150)
        content_splitter.addWidget(self.categories_widget)
        
        main_layout.addWidget(content_splitter)

        # Bottom Bar
        self._create_bottom_bar()
        main_layout.addWidget(self.bottom_bar)

    def _create_top_bar(self):
        self.top_bar = QFrame()
        self.top_bar.setStyleSheet(styles.POSStyles.TOP_BAR)
        self.top_bar.setFixedHeight(80)
        
        layout = QHBoxLayout(self.top_bar)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # Employee info and time
        info_layout = QVBoxLayout()
        emp_info = QLabel(f"Emp ID: {self.user_id}")
        emp_info.setStyleSheet(styles.POSStyles.TOP_BAR_TEXT)
        
        self.time_label = QLabel()
        self.time_label.setStyleSheet(styles.POSStyles.TOP_BAR_TEXT)
        
        info_layout.addWidget(emp_info)
        info_layout.addWidget(self.time_label)
        layout.addLayout(info_layout)
        
        layout.addStretch()
        
        # Add exit button
        exit_button = QPushButton("EXIT")
        exit_button.setStyleSheet(styles.POSStyles.EXIT_BUTTON)
        exit_button.clicked.connect(ApplicationUtils.close_application)
        layout.addWidget(exit_button)

        # Timer for updating time
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)
        self._update_time()

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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Order Header
        header = QLabel("ORDER # 1234")
        header.setStyleSheet(styles.POSStyles.SECTION_HEADER)
        header.setAlignment(Qt.AlignLeft)
        layout.addWidget(header)
        
        # Order Items Area
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
        
        for label, amount in [("Subtotal", "$0.00"), ("Tax (5%)", "$0.00"), ("Total", "$0.00")]:
            row = QHBoxLayout()
            label_widget = QLabel(label)
            amount_widget = QLabel(amount)
            row.addWidget(label_widget)
            row.addWidget(amount_widget)
            summary_layout.addLayout(row)
        
        layout.addWidget(summary_frame)
        
        return order_frame

    def _create_products_widget(self):
        products_frame = QFrame()
        products_frame.setStyleSheet(styles.POSStyles.PRODUCTS_PANEL)
        
        layout = QGridLayout(products_frame)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Sample products for demonstration
        products = ["Chicken Club", "BLT", "Tuna", "Veggie", 
                   "Egg Sandwich", "Steak & Cheese", "Vegan Sandwich"]
        
        for i, product in enumerate(products):
            btn = QPushButton(product)
            btn.setStyleSheet(styles.POSStyles.PRODUCT_BUTTON)
            btn.setFixedSize(150, 100)
            row = i // 3
            col = i % 3
            layout.addWidget(btn, row, col)
        
        return products_frame

    def _create_categories_widget(self):
        categories_frame = QFrame()
        categories_frame.setStyleSheet(styles.POSStyles.CATEGORIES_PANEL)
        
        layout = QVBoxLayout(categories_frame)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)
        
        categories = ["Freq Items", "Sandwiches", "Snacks", "Beverages", "Desserts"]
        
        for category in categories:
            btn = QPushButton(category)
            btn.setStyleSheet(styles.POSStyles.CATEGORY_BUTTON)
            btn.setFixedHeight(40)
            layout.addWidget(btn)
        
        layout.addStretch()
        return categories_frame

    def _create_bottom_bar(self):
        self.bottom_bar = QFrame()
        self.bottom_bar.setStyleSheet(styles.POSStyles.BOTTOM_BAR)
        self.bottom_bar.setFixedHeight(60)
        
        layout = QHBoxLayout(self.bottom_bar)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Transaction Controls
        for btn_text in ["New Order", "Hold", "Void", "Discount"]:
            btn = QPushButton(btn_text)
            btn.setStyleSheet(styles.POSStyles.BOTTOM_BAR_BUTTON)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Payment Button
        pay_btn = QPushButton("Payment")
        pay_btn.setStyleSheet(styles.POSStyles.PAYMENT_BUTTON)
        layout.addWidget(pay_btn)