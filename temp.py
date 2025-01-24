import sys
from PyQt5.QtWidgets import (QWizard, QWizardPage, QLineEdit, QVBoxLayout, 
                            QLabel, QMessageBox)

class SetupWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("System Setup")
        self.addPage(CompanyInfoPage())
        self.addPage(AdminUserPage())
        self.setMinimumWidth(600)

class CompanyInfoPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Company Information")
        
        layout = QVBoxLayout()
        
        self.company_name = QLineEdit()
        layout.addWidget(QLabel("Company Name *"))
        layout.addWidget(self.company_name)
        
        self.phone = QLineEdit()
        layout.addWidget(QLabel("Phone Number *"))
        layout.addWidget(self.phone)
        
        self.setLayout(layout)
        
    def validatePage(self):
        if not self.company_name.text().strip():
            QMessageBox.warning(self, "Validation", "Company name is required")
            return False
        if not self.phone.text().strip():
            QMessageBox.warning(self, "Validation", "Phone number is required")
            return False
        return True

class AdminUserPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Admin User Setup")
        
        layout = QVBoxLayout()
        
        self.first_name = QLineEdit()
        layout.addWidget(QLabel("First Name *"))
        layout.addWidget(self.first_name)
        
        self.last_name = QLineEdit()
        layout.addWidget(QLabel("Last Name *"))
        layout.addWidget(self.last_name)
        
        self.pin = QLineEdit()
        self.pin.setMaxLength(4)
        self.pin.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("PIN (4 digits) *"))
        layout.addWidget(self.pin)
        
        self.setLayout(layout)
    
    def validatePage(self):
        if not all([self.first_name.text().strip(), 
                   self.last_name.text().strip(), 
                   self.pin.text().strip()]):
            QMessageBox.warning(self, "Validation", "All fields are required")
            return False
        if not self.pin.text().isdigit() or len(self.pin.text()) != 4:
            QMessageBox.warning(self, "Validation", "PIN must be 4 digits")
            return False
        return True

def check_setup_required():
    db = Database()
    with sqlite3.connect(db.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sys_company")
        has_company = cursor.fetchone()[0] > 0
        cursor.execute("SELECT COUNT(*) FROM emp_users")
        has_admin = cursor.fetchone()[0] > 0
        return not (has_company and has_admin)

# Update MainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        if check_setup_required():
            wizard = SetupWizard(self)
            if wizard.exec_():
                self.save_setup_data(wizard)
        self.initUI()
    
    def save_setup_data(self, wizard):
        company_page = wizard.page(0)
        admin_page = wizard.page(1)
        
        with sqlite3.connect(self.db.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO sys_company (name, phone)
                VALUES (?, ?)
            """, (company_page.company_name.text(), 
                 company_page.phone.text()))
            
            cursor.execute("""
                INSERT INTO emp_employees (first_name, last_name, phone)
                VALUES (?, ?, ?)
            """, (admin_page.first_name.text(),
                 admin_page.last_name.text(),
                 company_page.phone.text()))
            
            employee_id = cursor.lastrowid
            
            cursor.execute("""
                INSERT INTO emp_users (employee_id, pin, active)
                VALUES (?, ?, 1)
            """, (employee_id, admin_page.pin.text()))