from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtCore import Qt
from views.auth.user_id_view import UserIDView
from views.auth.pin_view import PinView
from styles.auth_styles import AuthStyles
from config.layouts import AuthLayoutConfig

class AuthenticationContainer(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.valid_user_id = "1001"  # Hardcoded valid user ID
        
        # Set style
        self.setStyleSheet(AuthStyles.get_auth_container_style())

        # Get config instance
        self.config = AuthLayoutConfig.get_instance()

        self._setup_ui()
        self.setFocusPolicy(Qt.StrongFocus)  # Enable keyboard focus

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        # Get container dimensions
        container_dims = self.config.get_auth_layout()

        # Explicitly set fixed width and height from config
        width =  container_dims['container_width']
        height = container_dims['container_height']
        self.setFixedSize(width, height)

        # layout.setContentsMargins(0, 0, 0, 0)
        layout.setContentsMargins(
            container_dims['container_margin'],
            container_dims['container_margin'],
            container_dims['container_margin'],
            container_dims['container_margin']
        )
        
        # User ID View
        self.user_id_view = UserIDView(self)
        layout.addWidget(self.user_id_view)

    def switch_to_pin_view(self, user_id):
        """Switch to PIN entry view"""
        if hasattr(self, 'user_id_view'):
            self.user_id_view.hide()
        
        if not hasattr(self, 'pin_view'):
            self.pin_view = PinView(user_id, self)
        self.pin_view.show()
        self.pin_view.setFocus()

    def switch_to_user_id_view(self):
        """Switch back to user ID entry view"""
        if hasattr(self, 'pin_view'):
            self.pin_view.hide()
        self.user_id_view.show()
        self.user_id_view.clear_all()
        self.user_id_view.setFocus()

    def keyPressEvent(self, event):
        """Delegate keyboard events to active view"""
        if hasattr(self, 'user_id_view') and self.user_id_view.isVisible():
            self.user_id_view.keyPressEvent(event)
        elif hasattr(self, 'pin_view') and self.pin_view.isVisible():
            self.pin_view.keyPressEvent(event)
        else:
            super().keyPressEvent(event)