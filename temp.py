from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt
from .styles import KeyboardEnabledInputStyles

class KeyboardEnabledInput(QLineEdit):
    def __init__(self, parent=None, style_type='base'):
        super().__init__(parent)
        self.keyboard_manager = KeyboardManager()
        self.keyboard_manager.register_input(self)
        
        # Apply appropriate style based on input type
        if style_type == 'search':
            self.setStyleSheet(KeyboardEnabledInputStyles.SEARCH_INPUT)
        else:
            self.setStyleSheet(KeyboardEnabledInputStyles.BASE_INPUT)
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.keyboard_manager.show_keyboard(self)
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.keyboard_manager.show_keyboard(self)
        
    def __del__(self):
        self.keyboard_manager.unregister_input(self)

class SearchLineEdit(KeyboardEnabledInput):
    def __init__(self, parent=None):
        super().__init__(parent, style_type='search')
        self.parent_view = parent
        
        # Load search icon
        search_icon = QSvgRenderer("assets/images/search.svg")
        self.search_pixmap = QPixmap(20, 20)
        self.search_pixmap.fill(Qt.transparent)
        painter = QPainter(self.search_pixmap)
        search_icon.render(painter)
        painter.end()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.drawPixmap(12, (self.height() - 20) // 2, self.search_pixmap)