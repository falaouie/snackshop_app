import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.db_dir = 'data'
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
        self.db_path = os.path.join(self.db_dir, 'snackshop.db')
        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.executescript('''
                -- System Tables (sys_)
                CREATE TABLE IF NOT EXISTS sys_company (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    address TEXT,
                    phone TEXT,
                    email TEXT,
                    tax_number TEXT,
                    logo BLOB
                );

                CREATE TABLE IF NOT EXISTS sys_permissions (
                    permission_id INTEGER PRIMARY KEY,
                    permission_name TEXT NOT NULL,
                    description TEXT
                );

                CREATE TABLE IF NOT EXISTS sys_roles (
                    role_id INTEGER PRIMARY KEY,
                    role_name TEXT NOT NULL,
                    description TEXT
                );

                CREATE TABLE IF NOT EXISTS sys_role_permissions (
                    role_id INTEGER,
                    permission_id INTEGER,
                    FOREIGN KEY (role_id) REFERENCES sys_roles (role_id),
                    FOREIGN KEY (permission_id) REFERENCES sys_permissions (permission_id),
                    PRIMARY KEY (role_id, permission_id)
                );

            -- Employee Management (emp_)
            CREATE TABLE IF NOT EXISTS emp_employees (
                employee_id INTEGER PRIMARY KEY AUTOINCREMENT CHECK (employee_id >= 1001),
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Set the sequence start
            INSERT OR IGNORE INTO sqlite_sequence (name, seq) 
            VALUES ('emp_employees', 1000);

                CREATE TABLE IF NOT EXISTS emp_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER NOT NULL,
                    pin TEXT NOT NULL,
                    active BOOLEAN DEFAULT 1,
                    last_login TIMESTAMP,
                    FOREIGN KEY (employee_id) REFERENCES emp_employees(employee_id),
                    UNIQUE(employee_id)
                );

                CREATE TABLE IF NOT EXISTS emp_user_permissions (
                    user_id INTEGER,
                    permission_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES emp_users(id),
                    FOREIGN KEY (permission_id) REFERENCES sys_permissions(permission_id),
                    PRIMARY KEY (user_id, permission_id)
                );

                -- Inventory Management (inv_)
                CREATE TABLE IF NOT EXISTS inv_categories (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT
                );

                CREATE TABLE IF NOT EXISTS inv_units (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    abbreviation TEXT
                );

                CREATE TABLE IF NOT EXISTS inv_items (
                    id INTEGER PRIMARY KEY,
                    code TEXT UNIQUE,
                    name TEXT NOT NULL,
                    category_id INTEGER,
                    unit_id INTEGER,
                    min_stock REAL,
                    is_ingredient BOOLEAN DEFAULT 0,
                    is_for_sale BOOLEAN DEFAULT 1,
                    active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (category_id) REFERENCES inv_categories(id),
                    FOREIGN KEY (unit_id) REFERENCES inv_units(id)
                );

                CREATE TABLE IF NOT EXISTS inv_stock (
                    id INTEGER PRIMARY KEY,
                    item_id INTEGER,
                    quantity REAL,
                    last_updated TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES inv_items(id)
                );

                -- Recipe Management (rec_)
                CREATE TABLE IF NOT EXISTS rec_recipes (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    selling_price REAL NOT NULL,
                    active BOOLEAN DEFAULT 1
                );

                CREATE TABLE IF NOT EXISTS rec_recipe_items (
                    recipe_id INTEGER,
                    item_id INTEGER,
                    quantity REAL NOT NULL,
                    FOREIGN KEY (recipe_id) REFERENCES rec_recipes(id),
                    FOREIGN KEY (item_id) REFERENCES inv_items(id),
                    PRIMARY KEY (recipe_id, item_id)
                );

                -- Sales Management (pos_)
                CREATE TABLE IF NOT EXISTS pos_orders (
                    id INTEGER PRIMARY KEY,
                    order_number TEXT UNIQUE,
                    employee_id INTEGER,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_amount REAL,
                    payment_method TEXT,
                    status TEXT,
                    FOREIGN KEY (employee_id) REFERENCES emp_employees(employee_id)
                );

                CREATE TABLE IF NOT EXISTS pos_order_items (
                    order_id INTEGER,
                    item_id INTEGER,
                    recipe_id INTEGER,
                    quantity INTEGER,
                    unit_price REAL,
                    total_price REAL,
                    FOREIGN KEY (order_id) REFERENCES pos_orders(id),
                    FOREIGN KEY (item_id) REFERENCES inv_items(id),
                    FOREIGN KEY (recipe_id) REFERENCES rec_recipes(id)
                );

                -- Purchase Management (pur_)
                CREATE TABLE IF NOT EXISTS pur_suppliers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    contact_person TEXT,
                    phone TEXT,
                    email TEXT,
                    address TEXT,
                    active BOOLEAN DEFAULT 1
                );

                CREATE TABLE IF NOT EXISTS pur_purchases (
                    id INTEGER PRIMARY KEY,
                    supplier_id INTEGER,
                    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_amount REAL,
                    status TEXT,
                    FOREIGN KEY (supplier_id) REFERENCES pur_suppliers(id)
                );

                CREATE TABLE IF NOT EXISTS pur_purchase_items (
                    purchase_id INTEGER,
                    item_id INTEGER,
                    quantity REAL,
                    unit_price REAL,
                    total_price REAL,
                    FOREIGN KEY (purchase_id) REFERENCES pur_purchases(id),
                    FOREIGN KEY (item_id) REFERENCES inv_items(id)
                );
            ''')

    def user_exists(self, employee_id):
      with sqlite3.connect(self.db_path) as conn:
          cursor = conn.cursor()
          cursor.execute('SELECT 1 FROM emp_users WHERE employee_id = ? AND active = 1', (employee_id,))
          return cursor.fetchone() is not None

    def authenticate_user(self, employee_id, pin):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT u.id, e.first_name, e.last_name 
                FROM emp_users u
                JOIN emp_employees e ON u.employee_id = e.employee_id
                WHERE u.employee_id = ? AND u.pin = ? AND u.active = 1
            ''', (employee_id, pin))
            return cursor.fetchone() is not None