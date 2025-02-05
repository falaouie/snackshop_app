

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

    def _create_order_widget(self):
        """Create order panel with modern styling and order list"""
        order_frame = QFrame()
        order_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-right: 1px solid #DEDEDE;
            }
            QLabel {
                color: #333;
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
        
        # USD Total
        usd_layout = QHBoxLayout()
        usd_label = QLabel("Total USD")
        self.usd_amount = QLabel("$0.00")
        self.usd_amount.setProperty("class", "currency-usd")
        usd_layout.addWidget(usd_label)
        usd_layout.addStretch()
        usd_layout.addWidget(self.usd_amount)
        
        # LBP Total
        lbp_layout = QHBoxLayout()
        lbp_label = QLabel("Total LBP")
        self.lbp_amount = QLabel("0")
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
        item_widget.setStyleSheet("""
            QFrame {
                background: white;
                border-bottom: 1px solid #EEEEEE;
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
        
        self.order_list_layout.addWidget(item_widget)
        self.order_list_layout.addStretch()

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

    def _show_category_items(self, category):
        # Previous category handling code...
        
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