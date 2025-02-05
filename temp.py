from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer

class YourClass:
    def __init__(self):
        self.top_bar = QFrame()
        self.top_bar.setStyleSheet(styles.POSStyles.TOP_BAR)
        self.top_bar.setFixedHeight(80)
        
        layout = QHBoxLayout(self.top_bar)
        layout.setContentsMargins(0, 0, 0, 0)  # left, top, right, and bottom
        
        # Logo and Info group
        left_group = QHBoxLayout()
        
        # Logo
        # logo_label = QLabel()
        # pixmap = QPixmap("assets/images/silver_system_logo.png")
        # scaled_pixmap = pixmap.scaled(QSize(150, 100), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # logo_label.setPixmap(scaled_pixmap)
        # left_group.addWidget(logo_label)
        
        # Vertical layout for emp_info and time_label
        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0, 0, 0, 0)  # left, top, right, and bottom
        vertical_layout.setSpacing(0)  # No space between emp_info and time_label
        
        # Emp Info
        emp_info = QLabel(f"Emp ID: {self.user_id}")
        emp_info.setStyleSheet(styles.POSStyles.TOP_BAR_TEXT)
        emp_info.setContentsMargins(10, 5, 10, 5)  # left, top, right, and bottom
        emp_info.setFixedHeight(20)
        vertical_layout.addWidget(emp_info)
        
        # Date/Time
        self.time_label = QLabel()
        self.time_label.setStyleSheet(styles.POSStyles.TOP_BAR_TEXT)
        self.time_label.setContentsMargins(10, 5, 10, 5)  # left, top, right, and bottom
        self.time_label.setFixedHeight(20)
        vertical_layout.addWidget(self.time_label)
        
        # Add the vertical layout to the left_group
        left_group.addLayout(vertical_layout)
        
        # Add left_group to the main layout
        layout.addLayout(left_group)
        
        # Timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)
        self._update_time()
    
    def _update_time(self):
        # Update the time_label with the current time
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.time_label.setText(current_time)