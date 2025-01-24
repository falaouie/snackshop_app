import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout,
                            QGridLayout, QPushButton, QMainWindow, QFrame)
from PyQt5.QtWidgets import (QWizard, QWizardPage, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QPalette, QColor, QPixmap
from models.database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        if check_setup_required():
            wizard = SetupWizard(self)
            if wizard.exec_():
                self.save_setup_data(wizard)
        self.initUI()
        
    def initUI(self):
        self.setWindowState(Qt.WindowMaximized)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(40, 40, 40, 200))
        self.setPalette(palette)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignCenter)
        
        self.auth_container = AuthenticationContainer(self)
        self.main_layout.addWidget(self.auth_container)

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

class AuthenticationContainer(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = parent.db  # Get database instance
        self.initUI()
        
    def initUI(self):
        # Set up the container styling
        self.setObjectName("authContainer")
        self.setStyleSheet("""
            QFrame#authContainer {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #cccccc;
            }
        """)
        
        # Set fixed size for the container
        self.setFixedSize(400, 600)
        
        # Create layout for the container
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 0, 10)
        
        # Create stacked widget to handle view switching
        self.current_view = "userid"  # Track current view
        self.setup_user_id_view()

    def setup_user_id_view(self):
        # Clear existing layout
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
        
        # Create and add UserIDView
        self.user_id_view = UserIDView(self)
        self.layout.addWidget(self.user_id_view)
        # Ensure focus is set
        self.user_id_view.setFocus()
    
    def switch_to_pin_view(self, user_id):
        # Clear existing layout
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
        
        # Create and add PinView
        self.pin_view = PinView(user_id, self)
        self.layout.addWidget(self.pin_view)
        self.current_view = "pin"
        # Ensure focus is set
        self.pin_view.setFocus()
    
    def switch_to_user_id_view(self):
        self.setup_user_id_view()
        self.current_view = "userid"

    def reset_to_pin_view(self, user_id):
        # Clear existing layout
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
        
        # Create new PIN view with the same user ID
        self.pin_view = PinView(user_id, self)
        self.layout.addWidget(self.pin_view)
        self.current_view = "pin"
        # Ensure focus is set
        self.pin_view.setFocus()
    
    def reset_to_user_id_view(self):
        # Clear existing layout
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
        
        # Create new User ID view
        self.user_id_view = UserIDView(self)
        self.layout.addWidget(self.user_id_view)
        self.current_view = "userid"
        # Ensure focus is set
        self.user_id_view.setFocus()

class UserIDView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_container = parent
        self.db = parent.db  # Get database instance
        self.initUI()
        self.setup_keyboard_input()

    def setup_keyboard_input(self):
        # Install event filter to handle keyboard input
        self.installEventFilter(self)
        # Set focus to ensure keyboard events are captured
        self.setFocus()

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
            key = event.key()
            
            # Ignore space bar events
            if key == Qt.Key_Space:
                return True
            if key >= Qt.Key_0 and key <= Qt.Key_9:
                # Convert key to digit
                digit = str(key - Qt.Key_0)
                self.add_digit(digit)
                self.check_next_enable()
                return True
            elif key == Qt.Key_Backspace:
                self.clear_one_user_id()
                return True
            elif key == Qt.Key_Return or key == Qt.Key_Enter:
                if self.current_index == 4:
                    user_id = ''.join([btn.text().strip() for btn in self.user_id_buttons])
                    self.parent_container.switch_to_pin_view(user_id)
                return True
        return super().eventFilter(obj, event)
    
    def initUI(self):
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Create a QLabel for the logo
        logo_label = QLabel()
        logo_size = (350, 200)  # Desired width and height for the logo
        pixmap = QPixmap('assets/images/silver_system_logo.png')  # Load the image
        scaled_pixmap = pixmap.scaled(logo_size[0], logo_size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Scale the image
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setFixedSize(*logo_size)  # Set the fixed size for the QLabel
        logo_label.setAlignment(Qt.AlignCenter)  # Align the logo to the center
        
        # Title
        self.title_label = QLabel('User ID')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16pt;")

        # Add the widgets to the layout
        layout = QVBoxLayout()
        layout.addWidget(logo_label)  # Add the logo first
        layout.addWidget(self.title_label)  # Add the title text
        
        # User ID Input Buttons
        self.user_id_buttons = []
        user_id_layout = QGridLayout()
        user_id_layout.setHorizontalSpacing(15)
        for i in range(4):
            btn = QPushButton(' ')
            btn.setFixedSize(50, 50)
            btn.setEnabled(False)
            btn.setStyleSheet("color: black; font-size: 14pt; font-weight: bold;")
            btn.setObjectName(f"user_id_btn_{i}")
            self.user_id_buttons.append(btn)
            user_id_layout.addWidget(btn, 0, i)
        
        layout.addLayout(user_id_layout)
        
        # Numeric keypad
        keypad_layout = QGridLayout()
        keypad_layout.setHorizontalSpacing(25)
        keypad_layout.setVerticalSpacing(20)
        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('Clear', 3, 0), ('0', 3, 1), ('Next', 3, 2),
        ]
        
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFixedSize(80, 50)
            button.setObjectName(f"keypad_btn_{text}")
            
            if text.isdigit():
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #f0f0f0;
                        font-size: 16pt;
                        font-weight: bold;
                        border-radius: 5px;
                        border: 1px solid #cccccc;
                    }
                    QPushButton:disabled {
                        background-color: #cccccc;
                        color:#c3c0c0;
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #e0e0e0;
                        font-size: 12pt;
                        border-radius: 5px;
                        border: 1px solid #cccccc;
                    }
                """)
            button.clicked.connect(self.on_button_click)
            keypad_layout.addWidget(button, row, col)
        
        layout.addLayout(keypad_layout)
        self.setLayout(layout)
        
        self.current_index = 0
        self.next_button = self.findChild(QPushButton, "keypad_btn_Next")
        if self.next_button:
            self.next_button.setEnabled(False)

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()

        if text == 'Clear':
            self.clear_one_user_id()
        elif text == 'Next':
            user_id = ''.join([btn.text().strip() for btn in self.user_id_buttons])
            self.validate_user_id(user_id)
        else:
            self.add_digit(text)
            self.check_next_enable()

    def validate_user_id(self, user_id):
        if self.db.user_exists(user_id):
            self.parent_container.switch_to_pin_view(user_id)
        else:
            self.title_label.setText('Invalid User ID')
            self.title_label.setStyleSheet("font-size: 16pt; color: red;")
            for btn in self.user_id_buttons:
                btn.setText(' ')
            self.current_index = 0
            self.check_next_enable()

    def add_digit(self, digit):
        # Reset title if an error was previously shown
        if self.title_label.text() == 'Invalid User ID':
            self.title_label.setText('User ID')
            self.title_label.setStyleSheet("font-size: 16pt;")

        # Existing add_digit logic
        if self.current_index < 4:
            self.user_id_buttons[self.current_index].setText(digit)
            self.current_index += 1

    def clear_one_user_id(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.user_id_buttons[self.current_index].setText(' ')
        self.check_next_enable()

    def check_next_enable(self):
        # Disable/enable numeric buttons based on current input
        digit_buttons = [btn for btn in self.findChildren(QPushButton) if btn.text().isdigit()]
        
        if self.current_index == 4:
            self.next_button.setEnabled(True)
            self.next_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 12pt;
                    border-radius: 5px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            # Disable all digit buttons
            for btn in digit_buttons:
                btn.setEnabled(False)
        else:
            self.next_button.setEnabled(False)
            self.next_button.setStyleSheet("""
                QPushButton {
                    background-color: #e0e0e0;
                    font-size: 12pt;
                    border-radius: 5px;
                    border: 1px solid #cccccc;
                }
            """)
            # Re-enable all digit buttons
            for btn in digit_buttons:
                btn.setEnabled(True)

class PinView(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.parent_container = parent
        self.db = parent.db  # Get database instance
        self.initUI()
        self.setup_keyboard_input()

    def setup_keyboard_input(self):
        # Install event filter to handle keyboard input
        self.installEventFilter(self)
        # Set focus to ensure keyboard events are captured
        self.setFocus()

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
            key = event.key()
            
            # Ignore space bar events
            if key == Qt.Key_Space:
                return True
            if key >= Qt.Key_0 and key <= Qt.Key_9:
                # Convert key to digit
                digit = str(key - Qt.Key_0)
                self.add_digit(digit)
                self.check_sign_in_enable()
                return True
            elif key == Qt.Key_Backspace:
                self.clear_one_pin()
                return True
            elif key == Qt.Key_Return or key == Qt.Key_Enter:
                if self.current_index == 4:
                    print("Signing in...")  # Placeholder for sign in logic
                return True
            elif key == Qt.Key_Escape:
                self.parent_container.switch_to_user_id_view()
                return True
        return super().eventFilter(obj, event)
    
    def initUI(self):
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Create a QLabel for the logo
        logo_label = QLabel()
        logo_size = (350, 150)  # Desired width and height for the logo
        pixmap = QPixmap('assets/images/silver_system_logo.png')  # Load the image
        scaled_pixmap = pixmap.scaled(logo_size[0], logo_size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Scale the image
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setFixedSize(*logo_size)  # Set the fixed size for the QLabel
        logo_label.setAlignment(Qt.AlignCenter)  # Align the logo to the center

        # Title
        self.title_label = QLabel(f'PIN for User ID: {self.user_id}')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16pt;")

        # Add the widgets to the layout
        layout = QVBoxLayout()
        layout.addWidget(logo_label)  # Add the logo first
        layout.addWidget(self.title_label)  # Add the title text
        
        # Pin Input Buttons
        self.pin_buttons = []
        pin_layout = QGridLayout()
        pin_layout.setHorizontalSpacing(15)
        for i in range(4):
            btn = QPushButton(' ')
            btn.setFixedSize(40, 40)
            btn.setEnabled(False)
            btn.setStyleSheet("color: black; font-size: 14pt;")
            btn.setObjectName(f"pin_btn_{i}")
            self.pin_buttons.append(btn)
            pin_layout.addWidget(btn, 0, i)
        
        layout.addLayout(pin_layout)
        
        # Numeric keypad
        keypad_layout = QGridLayout()
        keypad_layout.setHorizontalSpacing(25)
        keypad_layout.setVerticalSpacing(20)
        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('Clear', 3, 0), ('0', 3, 1), ('Back', 3, 2),
            ('Sign In', 4, 1)
        ]
        
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFixedSize(80, 50)
            button.setObjectName(f"keypad_btn_{text}")
            
            if text.isdigit():
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #f0f0f0;
                        font-size: 16pt;
                        font-weight: bold;
                        border-radius: 5px;
                        border: 1px solid #cccccc;
                    }
                    QPushButton:disabled {
                        background-color: #cccccc;
                        color:#c3c0c0;
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton {
                        background-color:rgb(249, 246, 246);
                        font-size: 12pt;
                        border-radius: 5px;
                        border: 1px solid #cccccc;
                    }
                """)
            button.clicked.connect(self.on_button_click)
            keypad_layout.addWidget(button, row, col)
        
        layout.addLayout(keypad_layout)
        self.setLayout(layout)
        
        self.current_index = 0
        self.sign_in_button = self.findChild(QPushButton, "keypad_btn_Sign In")
        if self.sign_in_button:
            self.sign_in_button.setEnabled(False)

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()

        if text == 'Clear':
            self.clear_one_pin()
        elif text == 'Back':
            self.parent_container.switch_to_user_id_view()
        elif text == 'Sign In':
            pin = ''.join(['*' for _ in range(4)])  # Mask pin input
            self.validate_pin(pin)
        else:
            self.add_digit(text)
            self.check_sign_in_enable()

    def add_digit(self, digit):
    # Reset title if an error was previously shown
        if 'Invalid PIN' in self.title_label.text():
            self.title_label.setText(f'PIN for User ID: {self.user_id}')
            self.title_label.setStyleSheet("font-size: 16pt;")

        if self.current_index < 4:
            # Store actual digit as object data
            self.pin_buttons[self.current_index].setProperty('digit', digit)
            self.pin_buttons[self.current_index].setText('*')
            self.current_index += 1

    def validate_pin(self, pin):
        pin_digits = ''.join([btn.property('digit') for btn in self.pin_buttons if btn.text() != ' '])
        
        if self.db.authenticate_user(self.user_id, pin_digits):
            self.open_landing_page()
        else:
            self.title_label.setText(f'Invalid PIN for User ID: {self.user_id}')
            self.title_label.setStyleSheet("font-size: 16pt; color: red;")
            for btn in self.pin_buttons:
                btn.setText(' ')
                btn.setProperty('digit', '')
            self.current_index = 0
            self.check_sign_in_enable()

    def open_landing_page(self):
        # Create a landing page window
        self.landing_page = LandingPage(self.user_id, self.parent_container)
        self.landing_page.showMaximized()
        # Hide the main window instead of closing
        self.parent_container.parent().hide()

    def clear_one_pin(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.pin_buttons[self.current_index].setText(' ')
        self.check_sign_in_enable()

    def check_sign_in_enable(self):
        # Disable/enable numeric buttons based on current input
        digit_buttons = [btn for btn in self.findChildren(QPushButton) if btn.text().isdigit()]
        
        if self.current_index == 4:
            self.sign_in_button.setEnabled(True)
            self.sign_in_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 12pt;
                    border-radius: 5px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            # Disable all digit buttons
            for btn in digit_buttons:
                btn.setEnabled(False)
        else:
            self.sign_in_button.setEnabled(False)
            self.sign_in_button.setStyleSheet("""
                QPushButton {
                    background-color: #e0e0e0;
                    font-size: 12pt;
                    border-radius: 5px;
                    border: 1px solid #cccccc;
                }
            """)
            # Re-enable all digit buttons
            for btn in digit_buttons:
                btn.setEnabled(True)

class LandingPage(QMainWindow):
    def __init__(self, user_id, parent=None):
        super().__init__()
        self.user_id = user_id
        self.parent_container = parent
        self.initUI()
    
    def initUI(self):
        # Set up the main window
        self.setWindowTitle(f'Welcome - User {self.user_id}')
        
        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # Create top right buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        lock_button = QPushButton('Lock')
        lock_button.setFixedSize(100, 40)
        lock_button.clicked.connect(self.lock_session)
        button_layout.addWidget(lock_button)
        
        signout_button = QPushButton('Sign Out')
        signout_button.setFixedSize(100, 40)
        signout_button.clicked.connect(self.sign_out)
        button_layout.addWidget(signout_button)
        
        # Add button layout to main layout
        main_layout.addLayout(button_layout)
        
        # Add welcome message
        welcome_label = QLabel(f'Welcome, User {self.user_id}!\n\nThis is a dummy landing page.')
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18pt;")
        
        main_layout.addWidget(welcome_label)
        
        # Set central widget
        self.setCentralWidget(central_widget)
    
    def lock_session(self):
        # Open PIN view for the same user
        if self.parent_container:
            # Reset authentication container to PIN view
            self.parent_container.reset_to_pin_view(self.user_id)
            # Show the main window again
            self.parent_container.parent().show()
            self.close()

    def sign_out(self):
        # Return to User ID view
        if self.parent_container:
            # Reset authentication container to User ID view
            self.parent_container.reset_to_user_id_view()
            # Show the main window again
            self.parent_container.parent().show()
            self.close()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application-wide stylesheet
    app.setStyleSheet("""
        QMainWindow {
            background-color: #525252;
        }
    """)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())