from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtSvg import QSvgRenderer
from styles import AuthStyles
from utilities.utils import ApplicationUtils
from config.layouts.auth_top_bar_layout import AuthTopBarLayoutConfig

class AuthTopBar(QFrame):
    """
    Authentication screen top bar widget.
    
    Signals:
        exit_clicked: Emitted when exit button is clicked
    """
    
    # Define signals
    exit_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Initialize the authentication top bar widget.
        
        Args:
            parent (QWidget, optional): Parent widget
        """
        super().__init__(parent)
        
        # Set style
        self.setStyleSheet(AuthStyles.get_auth_top_bar_container_style())

        # Get config instance
        self.config = AuthTopBarLayoutConfig.get_instance()
        
        # Explicitly set fixed height from config
        height = self.config.get_size('height')
        self.setFixedHeight(height)

        # App utils for handling application operations
        self.app_utils = ApplicationUtils()
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize the main UI structure"""
        # Get container dimensions
        container_dims = self.config.get_auth_top_bar_container_dimensions()
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            container_dims['padding_left'],
            container_dims['padding_top'],
            container_dims['padding_right'],
            container_dims['padding_bottom']
        )
        # layout.setSpacing(container_dims.get('section_spacing', 0))

        # Create logo section
        logo_label = self._create_logo()
        layout.addWidget(logo_label)
        
        # Add spacer
        layout.addStretch(1)
        
        # Create exit button section
        exit_btn = self._create_exit_button()
        layout.addWidget(exit_btn)
    
    def _create_logo(self):
        """Create and return the logo section"""
        logo_label = QLabel()
        logo_config = self.config.get_logo_size_config()
        
        # Load and scale logo
        pixmap = QPixmap("assets/images/silver_system_logo.png")
        scaled_pixmap = pixmap.scaled(
            QSize(
                logo_config['logo_width'], 
                logo_config['logo_height']
            ),
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        logo_label.setPixmap(scaled_pixmap)

        # Set style
        logo_label.setStyleSheet(AuthStyles.get_logo_label_style())
        
        return logo_label
    
    def _create_exit_button(self):
        """Create and return the exit button"""
        exit_btn = QPushButton()
        exit_config = self.config.get_exit_button_config()
        
        # Load SVG icon
        icon_size = exit_config['icon_size']
        renderer = QSvgRenderer("assets/images/exit_app.svg")
        pixmap = QPixmap(icon_size, icon_size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        # Set icon and style
        exit_btn.setIcon(QIcon(pixmap))
        exit_btn.setIconSize(QSize(icon_size, icon_size))
        exit_btn.setStyleSheet(AuthStyles.get_exit_button_style())
        
        # Connect signal
        exit_btn.clicked.connect(self._handle_exit)
        
        return exit_btn
    
    def _handle_exit(self):
        """Handle exit button click"""
        # Emit signal first (for any listeners)
        self.exit_clicked.emit()
        
        # Close application
        self.app_utils.close_application()