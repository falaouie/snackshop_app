from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from . import styles

class DigitBox(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(40, 40)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        """)
        
    def update_digit(self, value):
        if value:
            self.setText(value)
            self.setStyleSheet("""
                border: 2px solid #3498db;
                background-color: #f8f8f8;
                font-size: 16px;
            """)
        else:
            self.clear()
            self.setStyleSheet("""
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
            """)

class UserIDInput(QWidget):
    input_changed = pyqtSignal(list)  # Signal when input changes
    
    def __init__(self):
        super().__init__()
        self.digits = ["", "", "", ""]  # Track input digits
        self.current_position = 0       # Current digit being edited
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(10)
        
        self.digit_boxes = []
        for _ in range(4):
            box = DigitBox()
            self.digit_boxes.append(box)
            layout.addWidget(box)
            
        self.setLayout(layout)
        
    def add_digit(self, digit):
        if self.current_position < 4:
            self.digits[self.current_position] = digit
            self.digit_boxes[self.current_position].update_digit(digit)
            self.current_position += 1
            self.input_changed.emit(self.digits)
            
    def remove_digit(self):
        if self.current_position > 0:
            self.current_position -= 1
            self.digits[self.current_position] = ""
            self.digit_boxes[self.current_position].update_digit("")
            self.input_changed.emit(self.digits)
            
    def clear_all(self):
        self.digits = ["", "", "", ""]
        self.current_position = 0
        for box in self.digit_boxes:
            box.update_digit("")
        self.input_changed.emit(self.digits)
        
    def has_digits(self):
        """Check if any digits are entered"""
        return any(self.digits)
        
    def is_complete(self):
        """Check if all 4 digits are entered"""
        return all(self.digits)