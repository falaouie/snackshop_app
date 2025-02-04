from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget,
                             QPushButton, QFrame, QScrollArea, QGridLayout, QSizePolicy)
from PyQt5.QtCore import Qt

class POSView(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self._setup_ui()

    def _setup_ui(self):
        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- 1. Top Horizontal Bar (Fixed Position & Size) ---
        top_bar = QFrame()
        # top_bar.setFixedSize(800,60)
        # top_bar.setFixedSize(800, 60)
        top_bar.setFixedHeight(60)
        top_bar.setStyleSheet("background-color: lightgray;")
        

        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(0, 0, 0, 0)  # Remove extra margins
        top_layout.addWidget(QLabel("Top Bar (Fixed Height 60)"))

        # --- 2. Main Content Section ---
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)  # Remove extra spacing

        # Left Scrollable Section (Fixed Size)
        left_scroll = QScrollArea()
        left_scroll.setFixedSize(240, 420)
        left_scroll.setWidgetResizable(True)
        

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        left_layout.addWidget(QLabel("Left section FixedSize W 240, H 420"))
        left_layout.addStretch()
        # for i in range(10):
        #     left_layout.addWidget(QPushButton(f"Item {i+1}"))

        left_widget.setLayout(left_layout)
        left_scroll.setWidget(left_widget)

        # Right Grid Section (Fixed Size)
        center_frame = QFrame()
        # center_frame.setFixedSize(560, 420)
        center_frame.setFixedHeight(420)
        center_frame.setStyleSheet("background-color: lightyellow;")
        
        grid_layout = QGridLayout(center_frame)

        # for row in range(9):
        #     for col in range(3):
        #         btn = QPushButton(f"Btn {row},{col}")
        #         btn.setFixedSize(100, 50)
        #         grid_layout.addWidget(btn, row, col)
        
        grid_layout.addWidget(QLabel("center frame Fixed Height 420"))
        grid_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        center_frame.setLayout(grid_layout)

        # Add Left and Right Sections to Content Layout
        content_layout.addWidget(left_scroll)
        content_layout.addWidget(center_frame)
        
        # --- 3. Bottom Horizontal Section ---
        bottom_bar = QFrame()
        # self.setFixedSize(800, 120)
        self.setFixedHeight(120)
        # bottom_bar.setStyleSheet("background-color: red;")

        bottom_layout = QHBoxLayout(bottom_bar)
        # bottom_layout.addWidget(QPushButton("Bottom Left"))
        # bottom_layout.addWidget(QPushButton("Bottom Right"))
        bottom_layout.setContentsMargins(0, 0, 0, 0)  # Remove extra margins

        bottom_left = QLabel("Bottom Left FixedWidth:240", alignment=Qt.AlignCenter)
        bottom_left.setStyleSheet("background-color: lightblue;")
        bottom_left.setFixedWidth(240)
        bottom_right = QLabel("Bottom Right Fixed Height 120", alignment=Qt.AlignCenter)
        bottom_right.setStyleSheet("background-color: yellow;")
        # bottom_right.setFixedHeight(100)
        bottom_layout.setSpacing(0)
        bottom_layout.addWidget(bottom_left)
        bottom_layout.addWidget(bottom_right)
        # Add Everything to Main Layout
        main_layout.addWidget(top_bar)
        main_layout.addLayout(content_layout)
        main_layout.addWidget(bottom_bar)

        self.setLayout(main_layout)
        # self.setFixedSize(800, 600)  # Set fixed window size
        self.setFixedHeight(600)
