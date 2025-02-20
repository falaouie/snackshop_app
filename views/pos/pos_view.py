from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                                QPushButton, QFrame, QSplitter)
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtSvg import QSvgRenderer

from button_definitions.types import (
    PaymentButtonType,
    TransactionButtonType,
    HorizontalButtonType
)
from button_definitions.payment import PaymentButtonConfig
from button_definitions.transaction import TransactionButtonConfig
from button_definitions.horizontal import HorizontalButtonConfig 

from styles import POSStyles
from styles.buttons import ButtonStyles
from styles.layouts import layout_config

from components.pos.order_list_widget import OrderListWidget
from components.pos.product_grid_widget import ProductGridWidget
from components.pos.totals_widget import TotalsWidget
from components.pos.search_widget import SearchWidget
from components.keyboard import VirtualKeyboard
from components.pos.order_type_widget import OrderTypeWidget
from components.pos.horizontal_buttons_widget import HorizontalButtonsWidget

from models.product_catalog import PRODUCT_PRICES

class POSView(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.layout_config = layout_config.get_instance()
        self.exchange_rate = 90000
        self.prices = PRODUCT_PRICES 
        self.keyboard = VirtualKeyboard(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)
        
        self._setup_ui()
        self._update_time()

    def _setup_ui(self):
        """Initialize the main UI structure"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 10)
        main_layout.setSpacing(0)

        # Add top bar
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
        
        # Right Side - Products Grid
        self.products_widget = self._create_products_widget()
        content_splitter.addWidget(self.products_widget)
        
        main_layout.addWidget(content_splitter, 1)

        # Create and add bottom bar
        self.bottom_bar = self._create_bottom_bar()
        main_layout.addWidget(self.bottom_bar)

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
        emp_layout.addWidget(time_zone)

        # Search Section (Centered)
        search_container = QFrame()
        search_container.setStyleSheet("background: transparent;")
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create and connect search widget
        self.search_input = SearchWidget(self)
        self.search_input.search_changed.connect(self._filter_products)
        
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
        layout.addWidget(search_container, 1)
        layout.addWidget(controls_zone)
        
        return self.top_bar

    def _create_order_widget(self):
        """Create order panel"""
        order_frame = QFrame()
        
        layout = QVBoxLayout(order_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create and connect order list widget
        self.order_list = OrderListWidget()
        self.order_list.order_cleared.connect(self._on_order_cleared)
        self.order_list.item_removed.connect(self._on_item_removed)
        layout.addWidget(self.order_list)
        
        # Add horizontal buttons widget and connect signal
        self.horizontal_buttons = HorizontalButtonsWidget(self)
        self.horizontal_buttons.action_triggered.connect(self._handle_horizontal_action)
        layout.addWidget(self.horizontal_buttons)

        return order_frame
    
    # Add new handler method:
    def _handle_horizontal_action(self, action_type):
        """Handle horizontal button actions"""
        action_map = {
            'hold': self.hold_transaction,
            'void': self.void_transaction,
            'no_sale': self.no_sale
        }
        
        if action_type in action_map:
            action_map[action_type]()

    def _create_products_widget(self):
        """Create products panel"""
        products_frame = QFrame()
        
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

        # Create and connect product grid
        self.product_grid = ProductGridWidget()
        self.product_grid.product_selected.connect(self._handle_product_click)
        
        # Add panels to content layout
        content_layout.addWidget(center_panel)
        content_layout.addWidget(self.product_grid, 1)

        # Add content container to main layout
        main_layout.addWidget(content_container, 1)

        # Create and add totals widget
        self.totals_widget = TotalsWidget(self.exchange_rate)
        main_layout.addWidget(self.totals_widget)
        
        return products_frame

    def _create_bottom_bar(self):
        """Create bottom action bar"""
        bottom_bar = QFrame()
        bottom_bar.setStyleSheet(POSStyles.BOTTOM_BAR(
            self.layout_config.get_pos_layout()['bottom_bar_height']
        ))
        layout = QHBoxLayout(bottom_bar)
        layout.setContentsMargins(10, 5, 10, 10)
        layout.setSpacing(6)

        # Create and add order type widget
        self.order_type_widget = OrderTypeWidget()
        self.order_type_widget.order_type_changed.connect(self._on_order_type_changed)
        layout.addWidget(self.order_type_widget)
        
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

        return bottom_bar

    # Event Handlers
    def _filter_products(self):
        """Filter products based on search input"""
        search_text = self.search_input.text()
        self.product_grid.set_search_text(search_text)

    def _handle_product_click(self, item_name):
        """Handle product button click"""
        self.order_list.add_item(item_name, self.prices.get(item_name, 0))
        self._update_totals()
        self.search_input.clear_search()

    def _on_order_cleared(self):
        """Handle order being cleared"""
        self._update_totals()

    def _on_item_removed(self, item):
        """Handle item removal from order"""
        self._update_totals()

    def _on_order_type_changed(self, order_type):
        """Handle order type changes"""
        pass

    def _update_totals(self):
        """Update totals display"""
        total_usd = self.order_list.total_amount
        self.totals_widget.update_totals(total_usd)

    def _update_time(self):
        """Update the time display"""
        current = QDateTime.currentDateTime()
        self.date_label.setText(current.toString("dd-MM-yyyy"))
        self.time_label.setText(current.toString("h:mm AP"))

    def _handle_lock(self):
        """Handle lock button click"""
        from ..view_manager import ViewManager
        ViewManager.get_instance().switch_back_to_pin_view_from_pos(self.user_id)
        self.deleteLater()

    # Payment/Transaction Methods
    def process_cash_payment(self):
        """Handle cash payment"""
        print("Cash button clicked")

    def process_other_payment(self):
        """Handle other payment types"""
        print("Other Payment button clicked")

    def hold_transaction(self):
        """Handle hold transaction"""
        print("Not This Hold horizontal button clicked")

    def void_transaction(self):
        """Handle void transaction"""
        print("Not This Void horizontal button clicked")

    def paid_in(self):
        """Handle paid in"""
        print("Paid in button clicked")

    def paid_out(self):
        """Handle paid out"""
        print("Paid out button clicked")

    def no_sale(self):
        """Handle no sale"""
        print("Vertical No Sale button clicked")

    def apply_discount(self):
        """Handle discount"""
        print("Discount button clicked")

    def show_numpad(self):
        """Show numpad"""
        print("num pad button clicked")