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
from models.order_item import OrderItem
from components.pos.order_list_widget import OrderListWidget
from components.pos.product_grid_widget import ProductGridWidget
from components.pos.totals_widget import TotalsWidget

class POSView(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.layout_config = layout_config.get_instance()
        self.order_items = []
        self.exchange_rate = 90000
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

        layout = QVBoxLayout(order_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create OrderListWidget
        self.order_list = OrderListWidget()
        layout.addWidget(self.order_list)
        
        # Connect signals
        self.order_list.item_selected.connect(self._on_order_item_selected)
        self.order_list.item_removed.connect(self._on_order_item_removed)
        self.order_list.order_cleared.connect(self._on_order_cleared)
        
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

    def _on_order_item_selected(self, item):
        """Handle order item selection"""
        self.selected_item = item

    def _on_order_item_removed(self, item):
        """Handle order item removal"""
        self._update_totals()

    def _on_order_cleared(self):
        """Handle order cleared"""
        self._update_totals()

    def add_order_item(self, item_name):
        """Add an item to the order"""
        price = self.prices.get(item_name, 0)
        self.order_list.add_item(item_name, price)
        self._update_totals()
    
    def _update_totals(self):
        """Update the total amounts in USD and LBP"""
        # Get total from order list widget
        total_usd = self.order_list.total_amount
        # Update both currency displays using totals widget
        self.totals_widget.update_totals(total_usd)
    
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

        # Create and add product grid widget
        self.product_grid = ProductGridWidget()
        self.product_grid.product_selected.connect(self._handle_product_click)
        
        # Add panels to content layout
        content_layout.addWidget(center_panel)
        content_layout.addWidget(self.product_grid, 1)

        # Add content container to main layout
        main_layout.addWidget(content_container, 1)
        
        # Create and add totals frame with order type buttons
        totals_frame = self._create_totals_frame()
        main_layout.addWidget(totals_frame)
        
        return products_frame
    
    def _create_totals_frame(self):
        """Create totals frame with order type buttons and amounts"""
        self.totals_widget = TotalsWidget(self.exchange_rate)
        
        # Connect signals
        self.totals_widget.order_type_changed.connect(self._handle_order_type_change)
        
        return self.totals_widget
    
    def _handle_order_type_change(self, order_type):
        """Handle order type selection"""
        if order_type == OrderButtonType.DINE_IN.value:
            self.set_dine_in()
        elif order_type == OrderButtonType.TAKE_AWAY.value:
            self.set_take_away()
        elif order_type == OrderButtonType.DELIVERY.value:
            self.set_delivery()
        
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

    def _handle_lock(self):
        """Handle lock button click - return to PIN view"""
        # Import here to avoid circular import
        from .view_manager import ViewManager
        ViewManager.get_instance().switch_back_to_pin_view_from_pos(self.user_id)
        # Delete current POS view
        self.deleteLater()

    def _filter_products(self):
        """Filter products based on search input"""
        search_text = self.search_input.text()
        self.product_grid.set_search_text(search_text)

    def _handle_product_click(self, item_name):
        """Handle product button click - add item and clear search"""
        self.add_order_item(item_name)
        # Clear search field which will automatically refresh the grid
        self.search_input.clear()

    
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

    def hold_order(self):
        """Handle hold order action"""
        print("Hold button clicked")

    def void_order(self):
        """Handle void order action"""
        print("Void button clicked")

    def no_sale(self):
        """Handle no sale order action"""
        print("No Sale button clicked")

# class OrderItem:
#     def __init__(self, name, price):
#         self.name = name
#         self.price = price
#         self.quantity = 1

#     def get_total(self):
#         return self.price * self.quantity
    
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