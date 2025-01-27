from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDesktopWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize
from .auth_window import AuthenticationContainer
from . import styles

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snack Shop POS")
        self.setStyleSheet(styles.AppStyles.WINDOW_MAIN)
        self._setup_ui()
        self._setup_window_size()

    def _setup_window_size(self):
        """Configure window size based on screen resolution"""
        # Get screen geometry
        screen = QDesktopWidget().availableGeometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()

        # Set minimum window size
        self.setMinimumSize(1024, 768)

        # If screen is larger than minimum, use 80% of screen size
        if self.screen_width > 1024 and self.screen_height > 768:
            target_width = int(self.screen_width * 0.8)
            target_height = int(self.screen_height * 0.8)
            self.resize(target_width, target_height)
        else:
            # Use minimum size for smaller screens
            self.resize(1024, 768)

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with dynamic margins
        main_layout = QVBoxLayout(central_widget)
        margin_size = self._calculate_margin_size()
        main_layout.setContentsMargins(margin_size, margin_size, margin_size, margin_size)
        
        # Top bar with logo
        top_bar = QHBoxLayout()
        
        # Logo with dynamic sizing
        logo_label = QLabel()
        pixmap = QPixmap("assets/images/silver_system_logo.png")
        logo_size = self._calculate_logo_size()
        scaled_pixmap = pixmap.scaled(
            logo_size,
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setStyleSheet(styles.AppStyles.LOGO_CONTAINER)
        top_bar.addWidget(logo_label)
        top_bar.addStretch()
        
        main_layout.addLayout(top_bar)
        main_layout.addStretch()
        
        # Center container
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        
        self.auth_container = AuthenticationContainer()
        center_layout.addWidget(self.auth_container)
        
        center_layout.addStretch()
        main_layout.addLayout(center_layout)
        
        main_layout.addStretch()
        
        self.auth_container.setFocus()

    def _calculate_margin_size(self):
        """Calculate dynamic margins based on window size"""
        base_margin = 20  # Minimum margin size
        # Increase margins proportionally for larger screens
        if hasattr(self, 'screen_width') and self.screen_width > 1024:
            return int(base_margin * (self.screen_width / 1024) * 0.8)
        return base_margin

    def _calculate_logo_size(self):
        """Calculate logo size based on window size"""
        base_width = 200  # Minimum logo width
        base_height = 100  # Minimum logo height
        
        if hasattr(self, 'screen_width') and self.screen_width > 1024:
            scale_factor = min(self.screen_width / 1024, 2.0)  # Cap scaling at 2x
            return QSize(
                int(base_width * scale_factor),
                int(base_height * scale_factor)
            )
        return QSize(base_width, base_height)

    def resizeEvent(self, event):
        """Handle window resize events"""
        super().resizeEvent(event)
        # Update margins and logo size when window is resized
        if hasattr(self, 'auth_container'):
            margin_size = self._calculate_margin_size()
            self.centralWidget().layout().setContentsMargins(
                margin_size, margin_size, margin_size, margin_size
            )