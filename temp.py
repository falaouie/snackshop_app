# Add to existing imports at top of pos_view.py
from PyQt5.QtWidgets import (QGridLayout, QLineEdit)

class POSView(QWidget):
    # ... existing code remains the same until _create_products_widget ...

    def _create_products_widget(self):
        """Create products panel with updated layout structure"""
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

        # Add transaction buttons to center panel
        self.transaction_buttons = TransactionButtonsWidget()
        self.transaction_buttons.action_triggered.connect(self._on_transaction_action)
        center_layout.addWidget(self.transaction_buttons)

        # Create and connect product grid
        self.product_grid = ProductGridWidget()
        self.product_grid.product_selected.connect(self._handle_product_click)
        
        # Add panels to content layout
        content_layout.addWidget(center_panel)
        content_layout.addWidget(self.product_grid, 1)

        # Add content container to main layout
        main_layout.addWidget(content_container, 1)

        # Create intermediate container for numpad and payment sections
        intermediate_container = QFrame()
        intermediate_container.setFixedHeight(350)  # Set fixed height for the container
        intermediate_container.setStyleSheet("""
            QFrame {
                background: white;
                border-top: 1px solid #DEDEDE;
            }
        """)
        
        # Layout for intermediate container
        intermediate_layout = QHBoxLayout(intermediate_container)
        intermediate_layout.setContentsMargins(10, 10, 10, 10)
        intermediate_layout.setSpacing(10)

        # Add numpad widget (left side)
        self.numpad_widget = self._create_numpad_widget()
        intermediate_layout.addWidget(self.numpad_widget)

        # Create right side container for totals and payment
        right_container = QFrame()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        # Add totals widget to right container
        self.totals_widget = TotalsWidget(self.exchange_rate)
        right_layout.addWidget(self.totals_widget)

        # Add payment buttons to right container
        self.payment_buttons = PaymentButtonsWidget()
        self.payment_buttons.action_triggered.connect(self._on_payment_action)
        right_layout.addWidget(self.payment_buttons)

        # Add right container to intermediate layout
        intermediate_layout.addWidget(right_container, 1)

        # Add intermediate container to main layout
        main_layout.addWidget(intermediate_container)
        
        return products_frame

    def _create_numpad_widget(self):
        """Create the numpad widget with updated dimensions"""
        # Main container for the numpad
        numpad_container = QFrame()
        numpad_container.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #DEDEDE;
                border-radius: 4px;
            }
        """)
        numpad_container.setFixedWidth(350)  # Fixed width remains the same
        
        # Main horizontal layout
        main_layout = QHBoxLayout(numpad_container)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        # Create mode buttons container
        mode_container = QFrame()
        mode_layout = QVBoxLayout(mode_container)
        mode_layout.setContentsMargins(0, 0, 0, 0)
        mode_layout.setSpacing(4)
        
        # Mode button styles
        mode_button_style = """
            QPushButton {
                background: #F5F5F5;
                border: 1px solid #DEDEDE;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                min-width: 60px;
                min-height: 60px;  /* Increased height for better touch targets */
            }
            QPushButton:hover {
                background: #EBEBEB;
            }
            QPushButton:checked {
                background: #007AFF;
                color: white;
                border: none;
            }
        """

        # Create mode buttons
        mode_buttons = []
        for mode in ['QTY', 'WGT', 'USD', 'LBP']:
            btn = QPushButton(mode)
            btn.setCheckable(True)
            btn.setStyleSheet(mode_button_style)
            mode_layout.addWidget(btn)
            mode_buttons.append(btn)
        
        # Set QTY as default selected
        mode_buttons[0].setChecked(True)
        
        # Add stretch to bottom of mode buttons
        mode_layout.addStretch()

        # Create right side container (display + numpad)
        right_container = QFrame()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)

        # Create display
        display = QLineEdit()
        display.setAlignment(Qt.AlignRight)
        display.setReadOnly(True)
        display.setText("0")
        display.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DEDEDE;
                border-radius: 4px;
                padding: 8px;
                font-size: 24px;  /* Increased font size */
                background: #F9F9F9;
                min-height: 50px;  /* Increased height */
            }
        """)
        right_layout.addWidget(display)

        # Create numpad grid
        numpad_grid = QFrame()
        grid_layout = QGridLayout(numpad_grid)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(8)  # Increased spacing

        # Number button style
        number_button_style = """
            QPushButton {
                background: white;
                border: 1px solid #DEDEDE;
                border-radius: 4px;
                padding: 8px;
                font-size: 20px;  /* Increased font size */
                min-width: 70px;  /* Increased width */
                min-height: 70px; /* Increased height */
            }
            QPushButton:hover {
                background: #F5F5F5;
            }
            QPushButton:pressed {
                background: #EBEBEB;
            }
        """

        # Create number buttons
        numbers = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['0', '.', 'C']
        ]

        for i, row in enumerate(numbers):
            for j, num in enumerate(row):
                btn = QPushButton(num)
                btn.setStyleSheet(number_button_style)
                grid_layout.addWidget(btn, i, j)

        right_layout.addWidget(numpad_grid)

        # Add containers to main layout
        main_layout.addWidget(mode_container)
        main_layout.addWidget(right_container, 1)

        return numpad_container

    def _create_bottom_bar(self):
        """Bottom bar remains unchanged - contains only order type widget"""
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

        return bottom_bar