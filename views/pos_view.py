from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox,
                             QPushButton, QFrame, QScrollArea, QGridLayout, QSplitter, QToolButton)
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor, QFont
from PyQt5.QtSvg import QSvgRenderer
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
        self.order_widget.setFixedWidth(300)
        content_splitter.addWidget(self.order_widget)
        
        # Middle - Products Grid
        self.products_widget = self._create_products_widget()
        self.products_widget.setFixedWidth(500)
        content_splitter.addWidget(self.products_widget)
        
        main_layout.addWidget(content_splitter)

        # Bottom Bar
        self._create_bottom_bar()
        main_layout.addWidget(self.bottom_bar)

    def _create_top_bar(self):
        self.top_bar = QFrame()
        self.top_bar.setStyleSheet("""
            QFrame {
                background-color: #E8E8E8;
                border: none;
            }
            QFrame[class="zone"] {
                background-color: white;
                border-radius: 8px;
                margin: 2px;
                padding: 5px 5px;
            }
        """)
        self.top_bar.setFixedHeight(60)
        
        layout = QHBoxLayout(self.top_bar)
        layout.setContentsMargins(2, 0, 2, 0)
        layout.setSpacing(15)  # Space between zones
        
        # Left Zone - Employee Info
        emp_zone = QFrame()
        emp_zone.setProperty("class", "zone")
        emp_layout = QHBoxLayout(emp_zone)
        
        # Employee icon and ID
        emp_icon = QLabel()
        renderer = QSvgRenderer("assets/images/employee_icon.svg")
        pixmap = QPixmap(32, 32)  # Your desired size
        pixmap.fill(Qt.transparent)  # Make background transparent
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        emp_icon.setPixmap(pixmap)
        emp_icon.setFixedSize(32, 32)
        
        emp_info = QLabel(f"EMP ID: {self.user_id}")
        emp_info.setStyleSheet("font-size: 14px; font-weight: bold; color: #333333;")
        
        emp_layout.addWidget(emp_icon)
        emp_layout.addWidget(emp_info)
        emp_layout.addStretch()
        
        # Center Zone - DateTime
        time_zone = QFrame()
        time_zone.setProperty("class", "zone")
        time_layout = QHBoxLayout(time_zone)
        
        self.date_label = QLabel()
        self.date_label.setStyleSheet("font-size: 12px; color: #666666;")
        
        # Vertical separator
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet("background-color: #E0E0E0;")
        separator.setFixedWidth(2)
        
        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333333;")
        
        time_layout.addWidget(self.date_label)
        time_layout.addWidget(separator)
        time_layout.addWidget(self.time_label)
        
        # Right Zone - Controls
        controls_zone = QFrame()
        controls_zone.setProperty("class", "zone")
        controls_layout = QHBoxLayout(controls_zone)
        controls_layout.setSpacing(20)
        
        # Lock button
        lock_label = QLabel()
        pixmap = QPixmap("assets/images/lock_screen.png")
        scaled_pixmap = pixmap.scaled(QSize(32, 32), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        lock_label.setPixmap(scaled_pixmap)
        
        # Exit button
        exit_button = QPushButton()
        pixmap = QPixmap("assets/images/exit_app.png")
        scaled_pixmap = pixmap.scaled(QSize(32, 32), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        exit_button.setIcon(QIcon(scaled_pixmap))
        exit_button.setIconSize(scaled_pixmap.size())
        exit_button.setFlat(True)
        exit_button.setStyleSheet("QPushButton { border: none; }")
        app_utils = ApplicationUtils()
        exit_button.clicked.connect(app_utils.close_application)
        
        controls_layout.addWidget(lock_label)
        controls_layout.addWidget(exit_button)
        
        # Add all zones to main layout
        layout.addWidget(emp_zone, 1)
        layout.addWidget(time_zone, 2)
        layout.addWidget(controls_zone, 1)

        # Timer for updating time
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)
        self._update_time()

    def _update_time(self):
        current = QDateTime.currentDateTime()
        self.date_label.setText(current.toString("dd-MM-yyyy"))
        self.time_label.setText(current.toString("hh:mm AP"))

    def _create_order_widget(self):
        order_frame = QFrame()
        order_frame.setStyleSheet(styles.POSStyles.ORDER_PANEL)
        order_frame.setFixedSize(300, 450)

        layout = QVBoxLayout(order_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create a container frame for the header
        header_frame = QFrame()
        header_frame.setFixedHeight(50)  # Set a fixed height for the header area
        header_frame.setStyleSheet("background: transparent;")

        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 0, 10, 0)
        header_layout.setAlignment(Qt.AlignVCenter)

        # Create the embossed order header label
        header = EmbossedLabel("ORDER # 1234")
        header.setStyleSheet("font-size: 14px; font-weight: bold; color: #008CBA;")

        # Create the clickable three-dot button
        dots_button = QToolButton()
        dots_button.setText("⋮")
        dots_button.setStyleSheet("font-size: 18px; border: none; background: transparent;")
        dots_button.clicked.connect(self.on_dots_clicked)

        # Add widgets to the header layout
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(dots_button)

        # Add the header frame to the main layout
        layout.addWidget(header_frame)

        # Other widgets (scroll area, summary, etc.)
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
        
        # Add total labels
        for label, amount in [("Total USD", "$1.00"), ("Total LBP", "90,000")]:
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
        products_container.setFixedWidth(350)
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
            "Freq Items": ["Chicken Club", "BLT", "Tuna", "Veggie", "Egg Sandwich", "Steak N Cheese", "Vegan Sandwich", "BLT", "Tuna", "Veggie", "Egg Sandwich", "Steak & Cheese", "Vegan Sandwich"],
            "Sandwiches": ["Chicken Club", "BLT", "Tuna", "Veggie", "Egg Sandwich", 
                        "Steak N Cheese", "Vegan Sandwich"],
            "Snacks": ["Chips", "Popcorn", "Nuts", "Pretzels"],
            "Beverages": ["Coffee", "Tea", "Soda", "Soda Diet", "Lemonade", "Water"],
            "Desserts": ["Cookies", "Brownies", "Muffins", "Fruit Cup"]
        }
        
        # Add new products in 3-column grid
        for i, item in enumerate(items[category]):
            btn = QPushButton(item)
            btn.setStyleSheet(styles.POSStyles.PRODUCT_BUTTON)
            btn.setFixedSize(100, 50)
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
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Transaction Controls with color mapping
        transaction_buttons = {
            "Hold": {"bg": "#FFD700", "text": "#000000"},      # Gold background, black text
            "Void": {"bg": "#FF4136", "text": "#FFFFFF"},      # Red background, white text
            "Discount": {"bg": "#2ECC40", "text": "#FFFFFF"},  # Green background, white text
            "BLANK1": {"bg": "#808080", "text": "#FFFFFF"},    # Gray background, white text
            "BLANK2": {"bg": "#808080", "text": "#FFFFFF"},    # Gray background, white text
            "BLANK3": {"bg": "#808080", "text": "#FFFFFF"}     # Gray background, white text
        }

        for btn_text, colors in transaction_buttons.items():
            btn = QPushButton(btn_text)
            btn.setStyleSheet(f"""
                {styles.POSStyles.BOTTOM_BAR_BUTTON};
                background-color: {colors['bg']};
                color: {colors['text']};
            """)
            btn.setFixedSize(70, 70)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Payment Button
        pay_btn = QPushButton("Payment")
        pay_btn.setStyleSheet(styles.POSStyles.PAYMENT_BUTTON)
        pay_btn.setFixedSize(120, 70)
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

    def on_dots_clicked(self):
        # Placeholder action when clicked
        QMessageBox.information(self, "Settings", "Three dots clicked!")

class EmbossedLabel(QLabel):
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Get the font metrics to calculate vertical centering
        fm = painter.fontMetrics()
        text_height = fm.height()
        
        # Calculate vertical center position
        y_pos = (self.height() - text_height) // 2 + fm.ascent()
        
        # Draw shadow (bottom-right)
        painter.setPen(QColor(50, 50, 50, 150))  # Dark shadow
        painter.drawText(2, y_pos + 1, self.text())
        
        # Draw highlight (top-left)
        painter.setPen(QColor(255, 255, 255, 180))  # White highlight
        painter.drawText(0, y_pos - 1, self.text())
        
        # Draw main text
        painter.setPen(QColor(0, 150, 255))  # Main text color
        painter.drawText(1, y_pos, self.text())