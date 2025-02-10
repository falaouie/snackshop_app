class SearchLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_view = parent
        
        # Load search icon (left)
        search_icon = QSvgRenderer("assets/images/search.svg")
        self.search_pixmap = QPixmap(20, 20)
        self.search_pixmap.fill(Qt.transparent)
        painter = QPainter(self.search_pixmap)
        search_icon.render(painter)
        painter.end()
        
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DEDEDE;
                border-radius: 20px;
                padding: 8px 40px 8px 40px;
                font-size: 14px;
                color: #333;
                min-width: 300px;
                max-width: 400px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                outline: none;
            }
        """)
        
        # Install event filter for physical keyboard
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        """Handle physical keyboard input"""
        if obj == self and event.type() == event.KeyPress:
            # Process physical keyboard input regardless of virtual keyboard state
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                # Handle enter key if needed
                return True
            return False  # Allow other key events to be processed normally
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.drawPixmap(12, (self.height() - 20) // 2, self.search_pixmap)

    def mousePressEvent(self, event):
        """Handle mouse clicks on the search input"""
        super().mousePressEvent(event)
        self.setFocus()  # Ensure input has focus

class VirtualKeyboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_input = None
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._setup_ui()
        self.hide()

    def _on_key_press(self, key):
        """Handle virtual keyboard key presses"""
        if self.search_input:
            # Get current cursor position
            cursor_pos = self.search_input.cursorPosition()
            current_text = self.search_input.text()
            
            # Insert the key at cursor position
            new_text = current_text[:cursor_pos] + key + current_text[cursor_pos:]
            self.search_input.setText(new_text)
            
            # Move cursor after inserted character
            self.search_input.setCursorPosition(cursor_pos + 1)
            self.search_input.setFocus()  # Maintain focus on input

    def _on_backspace(self):
        """Handle virtual keyboard backspace"""
        if self.search_input:
            cursor_pos = self.search_input.cursorPosition()
            current_text = self.search_input.text()
            
            if cursor_pos > 0:
                # Remove character before cursor
                new_text = current_text[:cursor_pos-1] + current_text[cursor_pos:]
                self.search_input.setText(new_text)
                self.search_input.setCursorPosition(cursor_pos - 1)
            
            self.search_input.setFocus()

    def set_search_input(self, search_input):
        """Set the input field and ensure it has focus"""
        self.search_input = search_input
        if self.search_input:
            self.search_input.setFocus()

class POSView(QWidget):
    def _setup_ui(self):
        # ... existing setup code ...

        # Create search input with keyboard handling
        self.search_input = SearchLineEdit(self)
        self.search_input.textChanged.connect(self._filter_products)
        self.search_input.setPlaceholderText("Search products...")
        self.search_input.setFixedHeight(40)
        
        # Create keyboard toggle button
        keyboard_btn = QPushButton()
        keyboard_btn.setIcon(QIcon("assets/images/keyboard.svg"))
        keyboard_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background: #F8F9FA;
                border-radius: 12px;
            }
        """)
        keyboard_btn.setIconSize(QSize(70, 40))
        keyboard_btn.clicked.connect(self._toggle_keyboard)

    def _toggle_keyboard(self):
        """Toggle virtual keyboard visibility while maintaining input focus"""
        if not self.keyboard_visible:
            self.virtual_keyboard.set_search_input(self.search_input)
            self.virtual_keyboard.show()
            self.keyboard_visible = True
        else:
            self.virtual_keyboard.hide()
            self.keyboard_visible = False
        
        self.search_input.setFocus()  # Maintain focus on input field