from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize
from .auth_view import AuthenticationContainer
from . import styles
from config.screen_config import screen_config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snack Shop POS")
        self.setStyleSheet(styles.AppStyles.WINDOW_MAIN)
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Top bar with logo
        top_bar = QHBoxLayout()
        
        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("assets/images/silver_system_logo.png")
        scaled_pixmap = pixmap.scaled(
            QSize(screen_config.get_size('logo_width'), 
                screen_config.get_size('logo_height')),
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setStyleSheet(styles.AppStyles.LOGO_CONTAINER)
        top_bar.addWidget(logo_label)
        top_bar.addStretch()  # Push logo to left
        
        main_layout.addLayout(top_bar)
        
        # Add vertical spacer to push content down
        main_layout.addStretch()
        
        # Center container horizontally
        center_layout = QHBoxLayout()
        center_layout.addStretch()  # Push container right
        
        # Add authentication container
        self.auth_container = AuthenticationContainer()
        center_layout.addWidget(self.auth_container)
        
        center_layout.addStretch()  # Push container left
        main_layout.addLayout(center_layout)
        
        # Add vertical spacer to push content up
        main_layout.addStretch()
        
        self.auth_container.setFocus()