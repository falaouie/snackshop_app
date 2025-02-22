def _create_products_widget(self):
    """Create products panel with updated layout structure"""
    products_frame = QFrame()
    
    # Main layout for products area
    main_layout = QHBoxLayout(products_frame)
    main_layout.setContentsMargins(0, 5, 0, 0)
    main_layout.setSpacing(8)

    # Center panel - now extends full height
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

    # Create and add transaction buttons widget
    self.transaction_buttons = TransactionButtonsWidget()
    self.transaction_buttons.action_triggered.connect(self._on_transaction_action)
    center_layout.addWidget(self.transaction_buttons)
    center_layout.addStretch()  # Pushes buttons to top

    # Add center panel to main layout
    main_layout.addWidget(center_panel)

    # Right side container for product grid and intermediate section
    right_container = QWidget()
    right_layout = QVBoxLayout(right_container)
    right_layout.setContentsMargins(0, 0, 0, 0)
    right_layout.setSpacing(8)

    # Create and connect product grid
    self.product_grid = ProductGridWidget()
    self.product_grid.product_selected.connect(self._handle_product_click)
    right_layout.addWidget(self.product_grid, 1)

    # Intermediate section (numpad and payment)
    intermediate_container = QFrame()
    intermediate_container.setFixedHeight(350)
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
    self.numpad_widget = NumpadWidget(self)
    self.numpad_widget.display.textChanged.connect(self._handle_numpad_value_change)
    intermediate_layout.addWidget(self.numpad_widget)

    # Create container for totals and payment
    payment_container = QFrame()
    payment_layout = QHBoxLayout(payment_container)
    payment_layout.setContentsMargins(0, 0, 0, 0)
    payment_layout.setSpacing(10)

    # Add payment buttons
    self.payment_buttons = PaymentButtonsWidget()
    self.payment_buttons.action_triggered.connect(self._on_payment_action)
    payment_layout.addWidget(self.payment_buttons)

    # Add totals widget
    self.totals_widget = TotalsWidget(self.exchange_rate)
    payment_layout.addWidget(self.totals_widget)

    # Add payment container to intermediate layout
    intermediate_layout.addWidget(payment_container, 1)

    # Add intermediate container to right layout
    right_layout.addWidget(intermediate_container)

    # Add right container to main layout
    main_layout.addWidget(right_container, 1)

    return products_frame