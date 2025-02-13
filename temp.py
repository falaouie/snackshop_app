# 1. Proper button creation with consistent styling
self.close_btn = QPushButton("×")  # Use proper multiplication sign
self.close_btn.setFixedSize(self.dimensions['control_button_size'], 
                          self.dimensions['control_button_size'])
self.close_btn.setStyleSheet(KeyboardStyles.CONTROL_BUTTONS)

# 2. Keep enter and close functionalities separate
def _create_enter_button(self):
    """Create the enter button"""
    btn = QPushButton('↵  ENTER')
    btn.setFixedSize(self.dimensions['enter_width'], 
                    self.dimensions['enter_height'])
    btn.setStyleSheet(KeyboardStyles.ENTER_KEY)
    btn.clicked.connect(self._on_enter)  # Keep original enter functionality
    return btn

# 3. Proper state management
def _on_minimize(self):
    """Handle minimize button press"""
    self.close_btn.show()  # Ensure close button remains visible
    # ... rest of minimize code ...

def _on_restore(self):
    """Handle restore button press"""
    self.close_btn.show()  # Ensure close button remains visible
    # ... rest of restore code ...

# 4. Clear documentation
def _on_close(self):
    """Handle close button press to hide keyboard and cleanup"""
    if self.current_input:
        if self.is_minimized:
            self._on_restore()
        self.hide()
        if self.parent():
            self.parent().keyboard_visible = False