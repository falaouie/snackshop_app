from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from .auth_view import AuthenticationContainer
from . import styles
from config.screen_config import screen_config
from utilities.utils import close_application

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snack Shop POS")
        self.setStyleSheet(styles.AppStyles.WINDOW_MAIN)

        # Get the screen dimensions
        # screen_width, screen_height = screen_config.get_screen_dimensions()
        # Set the main window size based on the screen dimensions
        # self.setGeometry(100, 100, screen_width // 2, screen_height // 2)
        # self.setFixedSize(window_width, window_height)
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.centralWidget().setContentsMargins(0, 0, 0, 0)
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
        
        # Exit
        exit_button = QPushButton()

        # Load the pixmap and scale it
        pixmap = QPixmap("assets/images/exit_app.png")
        scaled_pixmap = pixmap.scaled(
            QSize(screen_config.get_size('logo_width'), 
                screen_config.get_size('logo_height')),
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )

        # Set the scaled pixmap as the icon for the button
        exit_button.setIcon(QIcon(scaled_pixmap))
        exit_button.setIconSize(scaled_pixmap.size())

        # Make the button flat (no border)
        exit_button.setFlat(True)

        # Set the style sheet to remove the background and border
        exit_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: transparent;
                border: none;
            }
            QPushButton:pressed {
                background: transparent;
                border: none;
            }
        """)

        # Connect the button's clicked signal to the close method
        exit_button.clicked.connect(close_application)

        top_bar.addWidget(exit_button)

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

    # def close_application(self):
    #     # Close the application
    #     QApplication.quit()