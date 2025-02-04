from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class POSView(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Snack Shop POS")
        self.setGeometry(100, 100, 800, 600)  # Adjust window size
        
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        # Top Bar
        top_bar = QLabel("Top Bar (Fixed Height 60)")
        top_bar.setFixedHeight(60)
        top_bar.setStyleSheet("background-color: #E3F2FD; font-size: 16px; padding: 10px; font-weight: bold;")
        top_bar.setAlignment(Qt.AlignCenter)
        
        # Middle Layout (Left + Center)
        middle_layout = QHBoxLayout()
        
        left_section = QLabel("Left Section (Fixed W: 240, H: 420)")
        left_section.setFixedSize(240, 420)
        left_section.setStyleSheet("background-color: #F5F5F5; font-size: 14px; padding: 10px;")
        left_section.setAlignment(Qt.AlignCenter)
        
        center_section = QLabel("Center Frame (Fixed Height 420)")
        center_section.setFixedHeight(420)
        center_section.setStyleSheet("background-color: #FFFDE7; font-size: 14px; padding: 10px;")
        center_section.setAlignment(Qt.AlignCenter)
        
        middle_layout.addWidget(left_section)
        middle_layout.addWidget(center_section)
        
        # Bottom Layout (Left + Right)
        bottom_layout = QHBoxLayout()
        
        bottom_left = QLabel("Bottom Left (Fixed Width: 240)")
        bottom_left.setFixedWidth(240)
        bottom_left.setStyleSheet("background-color: #F1F1F1; font-size: 14px; padding: 10px;")
        bottom_left.setAlignment(Qt.AlignCenter)
        
        bottom_right = QLabel("Bottom Right (Fixed Height 120)")
        bottom_right.setFixedHeight(120)
        bottom_right.setStyleSheet("background-color: #FFFFFF; font-size: 14px; padding: 10px; border-top: 1px solid #DDDDDD;")
        bottom_right.setAlignment(Qt.AlignCenter)
        
        bottom_layout.addWidget(bottom_left)
        bottom_layout.addWidget(bottom_right)
        
        # Add widgets to main layout
        main_layout.addWidget(top_bar)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(bottom_layout)
        
        central_widget.setLayout(main_layout)
