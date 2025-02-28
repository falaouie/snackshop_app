# Basic search widget without keyboard dependencies
class SearchWidget(QLineEdit):
    search_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_config = search_layout_config
        
        self._setup_ui()
        self._setup_search_icon()
        self.textChanged.connect(self._on_text_changed)
    
    # Standard search widget methods...

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