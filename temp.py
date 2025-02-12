def __init__(self, parent=None):
    super().__init__(parent)
    # ... existing initialization code ...
    
    # Add this line to track if we're filtering events
    self.is_filtering = False

def show(self):
    """Override show to handle positioning and setup event filter"""
    if self.parent():
        main_window = self.parent().window()
        if main_window:
            keyboard_width = self.sizeHint().width()
            keyboard_height = self.sizeHint().height()
            x = (main_window.width() - keyboard_width) // 2
            y = main_window.height() - keyboard_height - 20
            self.move(x, y)
            
            # Install event filter if not already filtering
            if not self.is_filtering:
                QApplication.instance().installEventFilter(self)
                self.is_filtering = True
                
    super().show()

def hide(self):
    """Override hide to cleanup event filter"""
    if self.is_filtering:
        QApplication.instance().removeEventFilter(self)
        self.is_filtering = False
    
    if self.is_minimized:
        self._on_restore()
    super().hide()

def eventFilter(self, watched, event):
    """Handle clicks outside the keyboard"""
    if event.type() == QEvent.MouseButtonPress:
        # Get click position in global coordinates
        click_pos = event.globalPos()
        
        # Convert keyboard geometry to global coordinates
        keyboard_rect = self.rect()
        global_rect = QRect(self.mapToGlobal(keyboard_rect.topLeft()),
                          self.mapToGlobal(keyboard_rect.bottomRight()))
        
        # Check if click is outside keyboard
        if not global_rect.contains(click_pos):
            # Don't minimize if clicking in an input field
            widget_under_mouse = QApplication.instance().widgetAt(click_pos)
            if widget_under_mouse and isinstance(widget_under_mouse, KeyboardEnabledInput):
                return False
                
            # Minimize keyboard if visible and not already minimized
            if self.isVisible() and not self.is_minimized:
                self._on_minimize()
                return True  # Event handled
                
    return False  # Let other widgets handle the event