import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                            QGridLayout, QPushButton, QMainWindow, QFrame)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QPalette, QColor, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Set up the main window to be fullscreen
        self.setWindowState(Qt.WindowMaximized)
        
        # Create and set the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Set dark background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(40, 40, 40, 200))  # Dark gray background
        self.setPalette(palette)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignCenter)
        
        # Create and add the floating authentication container
        self.auth_container = AuthenticationContainer(self)
        self.main_layout.addWidget(self.auth_container)

class AuthenticationContainer(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
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
    
    def switch_to_pin_view(self, user_id):
        # Clear existing layout
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
        
        # Create and add PinView
        self.pin_view = PinView(user_id, self)
        self.layout.addWidget(self.pin_view)
        self.current_view = "pin"
    
    def switch_to_user_id_view(self):
        self.setup_user_id_view()
        self.current_view = "userid"

class UserIDView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_container = parent
        self.initUI()
        self.setup_keyboard_input()

    def setup_keyboard_input(self):
        # Install event filter to handle keyboard input
        self.installEventFilter(self)

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
        title_label = QLabel('User ID')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16pt;")

        # Add the widgets to the layout
        layout = QVBoxLayout()
        layout.addWidget(logo_label)  # Add the logo first
        layout.addWidget(title_label)  # Add the title text
        
        # User ID Input Buttons
        self.user_id_buttons = []
        user_id_layout = QGridLayout()
        user_id_layout.setHorizontalSpacing(15)
        for i in range(4):
            btn = QPushButton(' ')
            btn.setFixedSize(50, 50)
            btn.setEnabled(False)
            btn.setStyleSheet("color: black; font-size: 14pt;")
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
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                    QPushButton:disabled {
                        background-color: #cccccc;
                        color: #888888;
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
                    QPushButton:hover {
                        background-color: #d0d0d0;
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
            self.parent_container.switch_to_pin_view(user_id)
        else:
            self.add_digit(text)
            self.check_next_enable()

    def add_digit(self, digit):
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
        self.initUI()
        self.setup_keyboard_input()

    def setup_keyboard_input(self):
        # Install event filter to handle keyboard input
        self.installEventFilter(self)

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
        title_label = QLabel(f'PIN for User ID: {self.user_id}')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16pt;")

        # Add the widgets to the layout
        layout = QVBoxLayout()
        layout.addWidget(logo_label)  # Add the logo first
        layout.addWidget(title_label)  # Add the title text
        
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
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                    QPushButton:disabled {
                        background-color: #cccccc;
                        color: #888888;
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
                    QPushButton:hover {
                        background-color: #d0d0d0;
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
            print("Signing in...")  # Placeholder for sign in logic
        else:
            self.add_digit(text)
            self.check_sign_in_enable()

    def add_digit(self, digit):
        if self.current_index < 4:
            self.pin_buttons[self.current_index].setText('*')
            self.current_index += 1

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