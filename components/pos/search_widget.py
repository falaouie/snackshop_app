from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtSvg import QSvgRenderer
from components.keyboard import KeyboardEnabledInput, KeyboardType
from styles import POSStyles
from styles.layouts import layout_config

class SearchWidget(KeyboardEnabledInput):
    """Widget for handling product search with virtual keyboard support"""
    
    # Signal when search text changes
    search_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent, style_type='search', keyboard_type=KeyboardType.FULL)
        self.parent_view = parent
        self.layout_config = layout_config.get_instance()
        
        self._setup_ui()
        self._setup_search_icon()
        
        # Connect text changed signal to emit our custom signal
        self.textChanged.connect(self._on_text_changed)

    def _setup_ui(self):
        """Initialize the search widget UI"""
        self.setPlaceholderText("Search products...")
        pos_layout = self.layout_config.get_pos_layout()
        self.setStyleSheet(POSStyles.SEARCH_INPUT(
            pos_layout['search_input']['width'],
            pos_layout['search_input']['height']
        ))

    def _setup_search_icon(self):
        """Setup the search icon"""
        # Load search icon
        search_icon = QSvgRenderer("assets/images/search.svg")
        self.search_pixmap = QPixmap(20, 20)
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
        painter.drawPixmap(12, (self.height() - 20) // 2, self.search_pixmap)

    def clear_search(self):
        """Clear the search input"""
        self.clear()