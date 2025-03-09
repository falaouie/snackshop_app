from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class ViewManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ViewManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.main_window = None
        self.auth_container = None
    
    def initialize(self, main_window: QMainWindow):
        """Initialize with main window reference"""
        self.main_window = main_window
        
    def switch_to_pin_view(self, user_id: str):
        """Switch to PIN entry view"""
        if self.auth_container:
            self.auth_container.show()
            self.auth_container.switch_to_pin_view(user_id)
    
    def switch_to_user_id_view(self):
        """Switch back to user ID entry view"""
        if self.auth_container:
            self.auth_container.show()
            self.auth_container.switch_to_user_id_view()
    
    def switch_to_pos_view(self, user_id: str, user_name : str):
        """Switch to POS view"""
        if self.main_window:
            # Hide the auth container
            if self.auth_container:
                self.auth_container.hide()
            
            # Import here to avoid circular import
            from .pos.pos_view import POSView
            
            # Create and show POS view
            pos_view = POSView(user_id, user_name, self.main_window)
            self.main_window.setCentralWidget(pos_view)
            pos_view.show()
    
    def switch_back_to_pin_view_from_pos(self, user_id: str):
        """Switch from POS view back to PIN view"""
        if self.main_window:
            # Create central widget to hold everything
            central_widget = QWidget()
            self.main_window.setCentralWidget(central_widget)
            main_layout = QVBoxLayout(central_widget)
            main_layout.setContentsMargins(20, 20, 20, 20)
            
            # Add top bar
            from components.common import AuthTopBar
            auth_top_bar = AuthTopBar(central_widget)
            main_layout.addWidget(auth_top_bar)
            
            main_layout.addStretch()
            
            # Center container horizontally with auth container
            center_layout = QHBoxLayout()
            center_layout.addStretch()
            
            # Import here to avoid circular import
            from .auth.auth_container import AuthenticationContainer
            
            self.auth_container = AuthenticationContainer()
            self.auth_container.setFocusPolicy(Qt.StrongFocus)
            self.auth_container.switch_to_pin_view(user_id)
            center_layout.addWidget(self.auth_container)
            
            center_layout.addStretch()
            main_layout.addLayout(center_layout)
            main_layout.addStretch()
            
            # Set focus
            self.auth_container.setFocus()
            if hasattr(self.auth_container, 'pin_view'):
                self.auth_container.pin_view.setFocus()
    
    @classmethod
    def get_instance(cls):
        """Get singleton instance"""
        if cls._instance is None:
            cls._instance = ViewManager()
        return cls._instance