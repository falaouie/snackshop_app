from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from .auth.auth_container import AuthenticationContainer
from .auth.top_bar import TopBar
from .view_manager import ViewManager
from styles.app import AppStyles 
from config.screen_config import screen_config
# from services.data_service import DataService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snack Shop POS - Silver System")

        # self.data_service = DataService()  # Single instance
        
        self.setStyleSheet(AppStyles.WINDOW_MAIN)
        
        # Get screen dimensions from config
        screen_width, screen_height = screen_config.get_screen_dimensions()
        
        # Set window size to 80% of screen dimensions
        self.window_width = int(screen_width)
        self.window_height = int(screen_height)
        self.setFixedSize(self.window_width, self.window_height)
        
        # Center window on screen
        self.move(
            (screen_width - self.window_width) // 2,
            (screen_height - self.window_height) // 2
        )
        
        # Initialize ViewManager with this window
        ViewManager.get_instance().initialize(self)
        
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.centralWidget().setContentsMargins(0, 0, 0, 0)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add top bar
        top_bar = TopBar(central_widget)
        main_layout.addLayout(top_bar.layout())
        
        # Add vertical spacer to push content down
        main_layout.addStretch()
        
        # Center container horizontally
        center_layout = QHBoxLayout()
        center_layout.addStretch()  # Push container right
        
        # Add authentication container
        self.auth_container = AuthenticationContainer()
        ViewManager.get_instance().auth_container = self.auth_container
        center_layout.addWidget(self.auth_container)
        
        center_layout.addStretch()  # Push container left
        main_layout.addLayout(center_layout)
        
        # Add vertical spacer to push content up
        main_layout.addStretch()
        
        self.auth_container.setFocus()