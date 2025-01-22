import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton
from PyQt5.QtCore import Qt

class UserIDWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Sign In')
        self.setGeometry(100, 100, 300, 400)

        # Central layout with spacing
        layout = QVBoxLayout()
        layout.setSpacing(20)  # Vertical spacing between major sections
        
        # Title
        title_label = QLabel('User ID')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16pt;")  # Larger title font
        layout.addWidget(title_label)
        
        # User ID Input Buttons
        self.user_id_buttons = []
        user_id_layout = QGridLayout()
        user_id_layout.setHorizontalSpacing(15)  # Horizontal spacing between ID buttons
        for i in range(4):
            btn = QPushButton(' ')
            btn.setFixedSize(60, 40)
            btn.setEnabled(False)
            btn.setStyleSheet("color: black; font-size: 14pt;")  # Larger font for input display
            btn.setObjectName(f"user_id_btn_{i}")
            self.user_id_buttons.append(btn)
            user_id_layout.addWidget(btn, 0, i)
        
        layout.addLayout(user_id_layout)
        
        # Numeric keypad
        keypad_layout = QGridLayout()
        keypad_layout.setHorizontalSpacing(30)  # Horizontal spacing between keypad buttons
        keypad_layout.setVerticalSpacing(25)    # Vertical spacing between keypad buttons
        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('Clear', 3, 0), ('0', 3, 1), ('Sign In', 3, 2),
        ]
        
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFixedSize(80, 50)  # Keeping the same size
            button.setObjectName(f"keypad_btn_{text}")
            # Different font sizes for numbers vs text buttons
            if text.isdigit():
                button.setStyleSheet("background-color: lightgray; font-size: 16pt; font-weight: bold;")
            else:
                button.setStyleSheet("background-color: lightgray; font-size: 12pt;")
            button.clicked.connect(self.on_button_click)
            keypad_layout.addWidget(button, row, col)
        
        layout.addLayout(keypad_layout)
        self.setLayout(layout)

        # Center the window
        self.setFixedSize(self.sizeHint())
        self.move(self.screen().geometry().center() - self.rect().center())

        self.current_index = 0

        # Find Sign In button by objectName
        self.sign_in_button = self.findChild(QPushButton, "keypad_btn_Sign In")
        if self.sign_in_button:
            self.sign_in_button.setEnabled(False)
            self.sign_in_button.setStyleSheet("background-color: lightgray; font-size: 12pt;")
            self.sign_in_button.setFixedSize(80, 50)

    # [Previous methods remain the same]
    def on_button_click(self):
        sender = self.sender()
        text = sender.text()

        if text == 'Clear':
            self.clear_one_user_id()
        elif text == 'Sign In':
            user_id = ''.join([btn.text().strip() for btn in self.user_id_buttons])
            self.open_password_window(user_id)
        else:
            self.add_digit(text)
            self.check_sign_in_enable()

    def add_digit(self, digit):
        if self.current_index < 4:
            self.user_id_buttons[self.current_index].setText(digit)
            self.current_index += 1

    def clear_one_user_id(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.user_id_buttons[self.current_index].setText(' ')
        self.check_sign_in_enable()

    def open_password_window(self, user_id):
        self.password_window = PasswordWindow(user_id, self)
        self.password_window.show()
        self.close()

    def reset(self):
        self.clear_user_id()

    def clear_user_id(self):
        for btn in self.user_id_buttons:
            btn.setText(' ')
        self.current_index = 0
        self.check_sign_in_enable()

    def check_sign_in_enable(self):
        if self.current_index == 4:
            self.sign_in_button.setEnabled(True)
            self.sign_in_button.setStyleSheet("background-color: lightgreen; font-size: 12pt;")
        else:
            self.sign_in_button.setEnabled(False)
            self.sign_in_button.setStyleSheet("background-color: lightgray; font-size: 12pt;")
            self.sign_in_button.setFixedSize(80, 50)

class PasswordWindow(QWidget):
    def __init__(self, user_id, parent):
        super().__init__()
        self.user_id = user_id
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sign In')
        self.setGeometry(100, 100, 300, 400)

        # Central layout with spacing
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Display User ID as Title
        title_label = QLabel(f'User ID: {self.user_id}')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16pt;")  # Larger title font
        layout.addWidget(title_label)
        
        # Password Input Buttons
        self.password_buttons = []
        password_layout = QGridLayout()
        password_layout.setHorizontalSpacing(15)
        for i in range(4):
            btn = QPushButton(' ')
            btn.setFixedSize(60, 40)
            btn.setEnabled(False)
            btn.setStyleSheet("color: black; font-size: 14pt;")  # Larger font for input display
            btn.setObjectName(f"password_btn_{i}")
            self.password_buttons.append(btn)
            password_layout.addWidget(btn, 0, i)
        
        layout.addLayout(password_layout)
        
        # Numeric keypad
        keypad_layout = QGridLayout()
        keypad_layout.setHorizontalSpacing(30)
        keypad_layout.setVerticalSpacing(25)
        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('Clear', 3, 0), ('0', 3, 1), ('Cancel', 3, 2),
            ('Sign In', 4, 1)
        ]
        
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFixedSize(80, 50)
            button.setObjectName(f"keypad_btn_{text}")
            # Different font sizes for numbers vs text buttons
            if text.isdigit():
                button.setStyleSheet("background-color: lightgray; font-size: 16pt; font-weight: bold;")
            else:
                button.setStyleSheet("background-color: lightgray; font-size: 12pt;")
            button.clicked.connect(self.on_button_click)
            keypad_layout.addWidget(button, row, col)
        
        layout.addLayout(keypad_layout)
        self.setLayout(layout)

        # Center the window
        self.setFixedSize(self.sizeHint())
        self.move(self.screen().geometry().center() - self.rect().center())

        self.current_index = 0

        # Find Sign In button by objectName
        self.sign_in_button = self.findChild(QPushButton, "keypad_btn_Sign In")
        if self.sign_in_button:
            self.sign_in_button.setEnabled(False)
            self.sign_in_button.setStyleSheet("background-color: lightgray; font-size: 12pt;")
            self.sign_in_button.setFixedSize(80, 50)

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()

        if text == 'Clear':
            self.clear_one_password()
        elif text == 'Cancel':
            self.close()
            self.parent.reset()
            self.parent.show()
        elif text == 'Sign In':
            print("Password Sign In pressed")
        else:
            self.add_digit(text)
            self.check_sign_in_enable()

    def add_digit(self, digit):
        if self.current_index < 4:
            self.password_buttons[self.current_index].setText('*')
            self.current_index += 1

    def clear_one_password(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.password_buttons[self.current_index].setText(' ')
        self.check_sign_in_enable()

    def clear_password(self):
        for btn in self.password_buttons:
            btn.setText(' ')
        self.current_index = 0
        self.check_sign_in_enable()

    def check_sign_in_enable(self):
        if self.current_index == 4:
            self.sign_in_button.setEnabled(True)
            self.sign_in_button.setStyleSheet("background-color: lightgreen; font-size: 12pt;")
        else:
            self.sign_in_button.setEnabled(False)
            self.sign_in_button.setStyleSheet("background-color: lightgray; font-size: 12pt;")
            self.sign_in_button.setFixedSize(80, 50)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserIDWindow()
    window.show()
    sys.exit(app.exec_())