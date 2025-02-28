from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtSvg import QSvgRenderer
from components.keyboard import KeyboardEnabledInput, KeyboardType, KeyboardManager
from config.layouts.search_layout import search_layout_config
from styles.components import SearchStyles

class SearchWidget(KeyboardEnabledInput):
    """Widget for handling product search with virtual keyboard support"""
    
    # Signal when search text changes
    search_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_config = search_layout_config
        
        self._setup_ui()
        self._setup_search_icon()
        self.textChanged.connect(self._on_text_changed)

    def _setup_ui(self):
        """Initialize the search widget UI"""
        self.setPlaceholderText("Search products...")
        
        # Get dimensions from the search config
        dimensions = self.search_config.get_dimensions()
        width = dimensions['width']
        height = dimensions['height']
            
        self.setStyleSheet(SearchStyles.get_input_style(width, height))

    def _setup_search_icon(self):
        """Setup the search icon"""
        # Get icon size from config
        icon_size = self.search_config.get_size('icon_size')
            
        # Load search icon
        search_icon = QSvgRenderer("assets/images/search.svg")
        self.search_pixmap = QPixmap(icon_size, icon_size)
        self.search_pixmap.fill(Qt.transparent)
        painter = QPainter(self.search_pixmap)
        search_icon.render(painter)
        painter.end()

    def _on_text_changed(self, text):
        """Handle text changes and emit search signal"""
        self.search_changed.emit(text)

    def paintEvent(self, event):
        """Override paint event to draw search icon"""
        super().paintEvent(event)
        painter = QPainter(self)
        
        # Get icon margin from config
        margin_left = self.search_config.get_size('icon_margin_left')
            
        icon_size = self.search_pixmap.width()
        painter.drawPixmap(margin_left, (self.height() - icon_size) // 2, self.search_pixmap)

    def clear_search(self):
        """Clear the search input"""
        self.clear()

# Keyboard-enabled version that uses composition
class KeyboardEnabledSearchWidget(SearchWidget):
    def __init__(self, parent=None, keyboard_type=KeyboardType.FULL):
        super().__init__(parent)
        self.keyboard_type = keyboard_type
        self.keyboard_manager = KeyboardManager()
        self.keyboard_manager.register_input(self)
    
    def show_keyboard(self):
        if self.keyboard_manager:
            self.keyboard_manager.show_keyboard(self, self.keyboard_type)
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.show_keyboard()
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.show_keyboard()
    
    def __del__(self):
        if hasattr(self, 'keyboard_manager'):
            self.keyboard_manager.unregister_input(self)