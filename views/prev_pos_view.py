def __init__(self, user_id, parent=None, user_data=None):
        super().__init__()
        self.user_id = user_id
        self.parent_container = parent
        self.user_data = user_data
        self.db = parent.db
        self.initUI()
    
    def initUI(self):
        # Set window title and maximize
        self.setWindowTitle('Snack Shop POS')
        self.setWindowState(Qt.WindowMaximized)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create top bar
        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar)
        
        # Create content area
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        
        # Create left panel (Order Details)
        left_panel = self.create_left_panel()
        content_layout.addWidget(left_panel, stretch=1)
        
        # Create right panel (Menu Items)
        right_panel = self.create_right_panel()
        content_layout.addWidget(right_panel, stretch=2)
        
        main_layout.addWidget(content_widget)
        
        # Create bottom bar
        bottom_bar = self.create_bottom_bar()
        main_layout.addWidget(bottom_bar)
    
    def create_top_bar(self):
        top_bar = QFrame()
        top_bar.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 1px solid #cccccc;
            }
        """)
        top_bar.setFixedHeight(60)
        
        layout = QHBoxLayout(top_bar)
        
        # Left side - Employee info
        left_widget = QWidget()
        left_layout = QHBoxLayout(left_widget)
        
        # Get employee name from database
        with sqlite3.connect(self.db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT first_name, last_name 
                FROM emp_employees 
                WHERE employee_id = ?
            ''', (self.user_id,))
            result = cursor.fetchone()
            if result:
                employee_name = f'{result[0]} {result[1]}'
            else:
                employee_name = f'User {self.user_id}'

        # Employee name and control buttons
        emp_label = QLabel(employee_name)
        date_label = QLabel(QDate.currentDate().toString('dd-MM-yyyy'))
        lock_btn = QPushButton('Lock')
        signout_btn = QPushButton('Sign Out')
        
        lock_btn.clicked.connect(self.lock_session)
        signout_btn.clicked.connect(self.sign_out)
        
        left_layout.addWidget(emp_label)
        left_layout.addWidget(lock_btn)
        left_layout.addWidget(signout_btn)
        left_layout.addWidget(date_label)
        
        # Right side - Back Office button
        backoffice_btn = QPushButton('Back Office')
        backoffice_btn.clicked.connect(self.open_back_office)
        
        layout.addWidget(left_widget)
        layout.addStretch()
        layout.addWidget(backoffice_btn)
        
        return top_bar
        
    def open_back_office(self):
        self.back_office = BackOffice(self.user_data, self)
        self.back_office.show()
        self.hide()
    
    def lock_session(self):
        # Open PIN view for the same user
        if self.parent_container:
            # Reset authentication container to PIN view
            self.parent_container.reset_to_pin_view(self.user_id)
            # Show the main window again
            self.parent_container.parent().show()
            # Close the landing page
            self.close()
            
    def sign_out(self):
        # Return to User ID view
        if self.parent_container:
            # Reset authentication container to User ID view
            self.parent_container.reset_to_user_id_view()
            # Show the main window again
            self.parent_container.parent().show()
            self.close()

    
        
    def create_left_panel(self):
        left_panel = QFrame()
        left_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
        """)
        
        layout = QVBoxLayout(left_panel)
        
        # Order header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        
        order_label = QLabel('Current Order #1234')
        order_label.setStyleSheet('font-size: 14pt; font-weight: bold;')
        
        clear_btn = QPushButton('Clear Order')
        clear_btn.clicked.connect(self.clear_order)
        
        header_layout.addWidget(order_label)
        header_layout.addWidget(clear_btn)
        
        # Order items table
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(4)
        self.order_table.setHorizontalHeaderLabels(['Item', 'Qty', 'Price', 'Total'])
        self.order_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.order_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Order totals
        totals_widget = QWidget()
        totals_layout = QGridLayout(totals_widget)
        
        subtotal_label = QLabel('Subtotal:')
        tax_label = QLabel('Tax:')
        total_label = QLabel('Total:')
        
        self.subtotal_value = QLabel('$0.00')
        self.tax_value = QLabel('$0.00')
        self.total_value = QLabel('$0.00')
        
        totals_layout.addWidget(subtotal_label, 0, 0)
        totals_layout.addWidget(self.subtotal_value, 0, 1)
        totals_layout.addWidget(tax_label, 1, 0)
        totals_layout.addWidget(self.tax_value, 1, 1)
        totals_layout.addWidget(total_label, 2, 0)
        totals_layout.addWidget(self.total_value, 2, 1)
        
        layout.addWidget(header_widget)
        layout.addWidget(self.order_table)
        layout.addWidget(totals_widget)
        
        return left_panel
        
    def create_right_panel(self):
        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
        """)
        
        layout = QVBoxLayout(right_panel)
        
        # Category tabs
        self.category_tabs = QTabWidget()
        
        # Create tabs for each category
        categories = ['Sandwiches', 'Beverages', 'Snacks', 'Desserts', 'Combos']
        for category in categories:
            tab = QWidget()
            tab_layout = QGridLayout(tab)
            
            # Add menu item buttons to grid
            # This would be populated from database
            for i in range(12):  # Example with 12 items per category
                btn = QPushButton(f'{category} Item {i+1}\n$9.99')
                btn.setMinimumSize(120, 80)
                btn.clicked.connect(lambda checked, item=f'{category} Item {i+1}': 
                                  self.add_item_to_order(item))
                row = i // 4
                col = i % 4
                tab_layout.addWidget(btn, row, col)
            
            self.category_tabs.addTab(tab, category)
        
        layout.addWidget(self.category_tabs)
        
        return right_panel
        
    def create_bottom_bar(self):
        bottom_bar = QFrame()
        bottom_bar.setStyleSheet("""
            QFrame {
                background-color: white;
                border-top: 1px solid #cccccc;
            }
        """)
        bottom_bar.setFixedHeight(60)
        
        layout = QHBoxLayout(bottom_bar)
        
        # Left side - Order info
        items_count = QLabel('Items: 0')
        layout.addWidget(items_count)
        
        layout.addStretch()
        
        # Right side - Checkout button
        checkout_btn = QPushButton('Checkout')
        checkout_btn.setMinimumSize(120, 40)
        checkout_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14pt;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        checkout_btn.clicked.connect(self.show_checkout_dialog)
        
        layout.addWidget(checkout_btn)
        
        return bottom_bar
        
    def add_item_to_order(self, item_name):
        # Add item to order table
        row_position = self.order_table.rowCount()
        self.order_table.insertRow(row_position)
        
        self.order_table.setItem(row_position, 0, QTableWidgetItem(item_name))
        self.order_table.setItem(row_position, 1, QTableWidgetItem('1'))
        self.order_table.setItem(row_position, 2, QTableWidgetItem('$9.99'))
        self.order_table.setItem(row_position, 3, QTableWidgetItem('$9.99'))
        
        self.update_totals()
        
    def update_totals(self):
        # Calculate totals based on order items
        subtotal = 0
        for row in range(self.order_table.rowCount()):
            total_str = self.order_table.item(row, 3).text()
            total = float(total_str.replace('$', ''))
            subtotal += total
        
        tax = subtotal * 0.08  # 8% tax rate
        total = subtotal + tax
        
        self.subtotal_value.setText(f'${subtotal:.2f}')
        self.tax_value.setText(f'${tax:.2f}')
        self.total_value.setText(f'${total:.2f}')
        
    def clear_order(self):
        self.order_table.setRowCount(0)
        self.update_totals()
        
    def show_checkout_dialog(self):
        # Show payment dialog
        # This would be implemented as a separate class
        pass