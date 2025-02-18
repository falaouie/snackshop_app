from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtSvg import QSvgRenderer
from styles.app import AppStyles
from styles.layouts import layout_config
from utilities.utils import ApplicationUtils

class TopBar:
    def __init__(self, parent=None):
        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._setup_ui()
    
    def _setup_ui(self):
        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("assets/images/silver_system_logo.png")
        auth_layout = layout_config.get_instance().get_auth_layout()
        scaled_pixmap = pixmap.scaled(
            QSize(auth_layout['logo_width'], 
                 auth_layout['logo_height']),
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setStyleSheet(AppStyles.LOGO_CONTAINER)
        self._layout.addWidget(logo_label)
        self._layout.addStretch()
        
        # Exit button
        exit_btn = QPushButton()
        renderer = QSvgRenderer("assets/images/exit_app.svg")
        pixmap = QPixmap(150, 150)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        exit_btn.setIcon(QIcon(pixmap))
        exit_btn.setIconSize(QSize(150, 150))
        exit_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                padding: 0px;
            }
        """)
        app_utils = ApplicationUtils()
        exit_btn.clicked.connect(app_utils.close_application)
        self._layout.addWidget(exit_btn)
    
    def layout(self):
        """Get the layout containing the top bar"""
        return self._layout