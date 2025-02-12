from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QGridLayout, QLineEdit)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from .styles import KeyboardStyles, KeyboardConfig, KeyboardEnabledInputStyles

class KeyboardManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KeyboardManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the keyboard manager"""
        self.current_input = None
        self.keyboard = None
        self.registered_inputs = set()
        
    def register_keyboard(self, keyboard):
        """Register the virtual keyboard instance"""
        self.keyboard = keyboard
        
    def register_input(self, input_widget):
        """Register an input widget to use the virtual keyboard"""
        self.registered_inputs.add(input_widget)
        
    def unregister_input(self, input_widget):
        """Unregister an input widget"""
        if input_widget in self.registered_inputs:
            self.registered_inputs.remove(input_widget)
            
    def set_current_input(self, input_widget):
        """Set the currently focused input widget"""
        if input_widget in self.registered_inputs:
            self.current_input = input_widget
            return True
        return False
    
    def show_keyboard(self, input_widget):
        """Show keyboard for a specific input widget"""
        if self.keyboard and input_widget in self.registered_inputs:
            self.current_input = input_widget
            self.keyboard.set_input(input_widget)
            self.keyboard.show()
            return True
        return False
    
    def hide_keyboard(self):
        """Hide the virtual keyboard"""
        if self.keyboard:
            self.keyboard.hide()
            
    def get_current_input(self):
        """Get the currently focused input widget"""
        return self.current_input

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

class VirtualKeyboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = KeyboardManager()
        self.manager.register_keyboard(self)
        self.current_input = None
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.dragging = False
        self.drag_position = None
        self.is_minimized = False
        
        # Load configuration
        self.config = KeyboardConfig()
        self.dimensions = self.config.get_dimensions()
        self.layout_config = self.config.get_layout()
        
        self._setup_ui()
        self.hide()

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(*self.layout_config['main_margins'])
        self.main_layout.setSpacing(self.layout_config['main_spacing'])

        # Handle bar
        self.drag_handle = QFrame()
        self.drag_handle.setFixedHeight(self.dimensions['handle_height'])
        self.drag_handle.setStyleSheet(KeyboardStyles.HANDLE_BAR)
        
        # Handle layout
        self.handle_layout = QHBoxLayout(self.drag_handle)
        self.handle_layout.setContentsMargins(*self.layout_config['handle_margins'])
        self.handle_layout.setSpacing(self.layout_config['handle_spacing'])

        # Drag icon
        drag_icon = QLabel()
        renderer = QSvgRenderer("assets/images/drag_icon.svg")
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        drag_icon.setPixmap(pixmap)
        drag_icon.setStyleSheet("padding: 8px;")
        
        self.handle_layout.addWidget(drag_icon)
        self.handle_layout.addStretch()

        # Control buttons
        self.minimize_btn = QPushButton("−")
        self.restore_btn = QPushButton("□")
        self.minimize_btn.setFixedSize(self.dimensions['control_button_size'], 
                                     self.dimensions['control_button_size'])
        self.restore_btn.setFixedSize(self.dimensions['control_button_size'], 
                                    self.dimensions['control_button_size'])
        self.minimize_btn.setStyleSheet(KeyboardStyles.CONTROL_BUTTONS)
        self.restore_btn.setStyleSheet(KeyboardStyles.CONTROL_BUTTONS)
        
        self.minimize_btn.clicked.connect(self._on_minimize)
        self.restore_btn.clicked.connect(self._on_restore)
        
        self.handle_layout.addWidget(self.minimize_btn)
        self.handle_layout.addWidget(self.restore_btn)
        self.restore_btn.hide()

        self.main_layout.addWidget(self.drag_handle)

        # Keyboard container
        self.keyboard_container = QWidget()
        keyboard_layout = QHBoxLayout(self.keyboard_container)
        keyboard_layout.setSpacing(5)

        # QWERTY Section
        qwerty_widget = self._create_qwerty_section()
        keyboard_layout.addWidget(qwerty_widget, stretch=7)

        # Numpad Section
        numpad_widget = self._create_numpad_section()
        keyboard_layout.addWidget(numpad_widget, stretch=3)

        self.main_layout.addWidget(self.keyboard_container)

        # Bottom row
        self.bottom_row_widget = self._create_bottom_row()
        self.main_layout.addWidget(self.bottom_row_widget)

        # Apply base styles
        self.setStyleSheet(KeyboardStyles.KEYBOARD_BASE)

    def _create_qwerty_section(self):
        qwerty_widget = QWidget()
        main_layout = QVBoxLayout(qwerty_widget)
        main_layout.setSpacing(10)

        qwerty_rows = [
            list('QWERTYUIOP'),
            list('ASDFGHJKL'),
            list('ZXCVBNM')
        ]

        for letters in qwerty_rows:
            row_container = QWidget()
            row_layout = QHBoxLayout(row_container)
            
            if len(letters) == 9:  # Second row
                row_layout.setContentsMargins(30, 0, 25, 0)
            elif len(letters) == 7:  # Third row
                row_layout.setContentsMargins(50, 0, 50, 0)
                
            for letter in letters:
                btn = self._create_key_button(letter)
                btn.clicked.connect(lambda checked, l=letter: self._on_key_press(l))
                row_layout.addWidget(btn)
                
            main_layout.addWidget(row_container)

        return qwerty_widget

    def _create_numpad_section(self):
        numpad_widget = QWidget()
        numpad_layout = QGridLayout(numpad_widget)
        numpad_layout.setSpacing(10)

        numpad_keys = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['CL', '0', '⌫']
        ]

        for row, keys in enumerate(numpad_keys):
            for col, key in enumerate(keys):
                btn = self._create_key_button(key)
                
                if key == '⌫':
                    btn.clicked.connect(self._on_backspace)
                elif key == 'CL':
                    btn.clicked.connect(self._on_clear)
                else:
                    btn.clicked.connect(lambda checked, k=key: self._on_key_press(k))
                
                numpad_layout.addWidget(btn, row, col)

        return numpad_widget

    def _create_bottom_row(self):
        bottom_row_widget = QWidget()
        bottom_row_layout = QHBoxLayout(bottom_row_widget)
        bottom_row_layout.setSpacing(5)

        # Space button
        space_btn = self._create_space_button()
        space_btn.clicked.connect(lambda: self._on_key_press(' '))
        bottom_row_layout.addWidget(space_btn, 70)

        # Enter button
        enter_btn = self._create_enter_button()
        enter_btn.clicked.connect(self._on_enter)
        bottom_row_layout.addWidget(enter_btn, 30)

        return bottom_row_widget

    def _create_key_button(self, text, size=None):
        """Create a standard keyboard key button"""
        btn = QPushButton(text)
        if size:
            btn.setFixedSize(*size)
        else:
            btn.setFixedSize(self.dimensions['key_width'], 
                           self.dimensions['key_height'])
        btn.setStyleSheet(KeyboardStyles.KEY_BUTTONS)
        return btn

    def _create_space_button(self):
        """Create the space bar button"""
        btn = QPushButton(' ')
        btn.setFixedSize(self.dimensions['space_width'], 
                        self.dimensions['space_height'])
        btn.setStyleSheet(KeyboardStyles.SPACE_KEY)
        return btn

    def _create_enter_button(self):
        """Create the enter button"""
        btn = QPushButton('↵  ENTER')
        btn.setFixedSize(self.dimensions['enter_width'], 
                        self.dimensions['enter_height'])
        btn.setStyleSheet(KeyboardStyles.ENTER_KEY)
        return btn

    # Event handlers (no changes needed)
    def _on_key_press(self, key):
        if self.current_input:
            cursor_pos = self.current_input.cursorPosition()
            current_text = self.current_input.text()
            new_text = current_text[:cursor_pos] + key + current_text[cursor_pos:]
            self.current_input.setText(new_text)
            self.current_input.setCursorPosition(cursor_pos + 1)
            self.current_input.setFocus()

    def _on_backspace(self):
        if self.current_input:
            cursor_pos = self.current_input.cursorPosition()
            current_text = self.current_input.text()
            if cursor_pos > 0:
                new_text = current_text[:cursor_pos-1] + current_text[cursor_pos:]
                self.current_input.setText(new_text)
                self.current_input.setCursorPosition(cursor_pos - 1)
            self.current_input.setFocus()

    def _on_clear(self):
        if self.current_input:
            self.current_input.clear()
            self.current_input.setFocus()

    def _on_enter(self):
        if self.current_input:
            if self.is_minimized:
                self._on_restore()
            self.hide()
            if self.parent():
                self.parent().keyboard_visible = False

    def _on_minimize(self):
        current_width = self.width()
        
        self.keyboard_container.hide()
        self.bottom_row_widget.hide()
        self.minimize_btn.hide()
        self.restore_btn.show()
        self.is_minimized = True
        
        self.adjustSize()
        self.setFixedWidth(current_width)
        
        main_window = self.parent().window()
        if main_window:
            x = (main_window.width() - current_width) // 2
            y = main_window.height() - self.height() - 20
            self.move(x, y)

    def _on_restore(self):
        current_width = self.width()
        
        self.keyboard_container.show()
        self.bottom_row_widget.show()
        self.restore_btn.hide()
        self.minimize_btn.show()
        self.is_minimized = False
        
        main_window = self.parent().window()
        if main_window:
            keyboard_width = self.sizeHint().width()
            keyboard_height = self.sizeHint().height()
            x = (main_window.width() - keyboard_width) // 2
            y = main_window.height() - keyboard_height - 20
            self.move(x, y)

    def set_input(self, input_widget):
        """Set the current input widget"""
        self.current_input = input_widget
        if self.current_input:
            self.current_input.setFocus()

    def show(self):
        """Override show to handle positioning"""
        if self.parent():
            main_window = self.parent().window()
            if main_window:
                keyboard_width = self.sizeHint().width()
                keyboard_height = self.sizeHint().height()
                x = (main_window.width() - keyboard_width) // 2
                y = main_window.height() - keyboard_height - 20
                self.move(x, y)
        super().show()

    # Mouse event handlers for dragging (no changes needed)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.pos().y() <= self.dimensions['handle_height']:
                self.dragging = True
                self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()

    def hide(self):
        if self.is_minimized:
            self._on_restore()
        super().hide()