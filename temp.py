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

        # Use the new transaction buttons widget
        self.transaction_buttons = TransactionButtonsWidget()
        self.transaction_buttons.action_triggered.connect(self._handle_transaction_action)
        center_layout.addWidget(self.transaction_buttons)

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