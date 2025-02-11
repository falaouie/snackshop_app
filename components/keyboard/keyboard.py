from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QGridLayout, QLineEdit)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer

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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keyboard_manager = KeyboardManager()
        self.keyboard_manager.register_input(self)
    
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
        self._setup_ui()
        self.hide()

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)

        # Handle bar
        self.handle_height = 40
        self.handle_styles = """
            QFrame {
                background: #444444;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
        """
        
        self.drag_handle = QFrame()
        self.drag_handle.setFixedHeight(self.handle_height)
        self.drag_handle.setStyleSheet(self.handle_styles)
        
        # Handle layout
        self.handle_layout = QHBoxLayout(self.drag_handle)
        self.handle_layout.setContentsMargins(10, 0, 10, 0)
        self.handle_layout.setSpacing(8)

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
        self.control_button_styles = """
            QPushButton {
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 20px;
                font-weight: bold;
                width: 40px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """

        self.minimize_btn = QPushButton("−")
        self.restore_btn = QPushButton("□")
        self.minimize_btn.setFixedSize(40, 40)
        self.restore_btn.setFixedSize(40, 40)
        self.minimize_btn.setStyleSheet(self.control_button_styles)
        self.restore_btn.setStyleSheet(self.control_button_styles)
        
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

        # Create bottom row widget and add to main layout
        self.bottom_row_widget = self._create_bottom_row()
        self.main_layout.addWidget(self.bottom_row_widget)

        self.setStyleSheet("""
            VirtualKeyboard {
                background: darkgrey;
                border-radius: 10px;
                padding: 10px;
            }
        """)

    def _create_qwerty_section(self):
        qwerty_widget = QWidget()
        main_layout = QVBoxLayout(qwerty_widget)
        main_layout.setSpacing(10)

        qwerty_rows = [
            list('QWERTYUIOP'),
            list('ASDFGHJKL'),
            list('ZXCVBNM')
        ]

        self.key_button_styles = """
            QPushButton {
                background: white;
                border: 1px solid #DEDEDE;
                border-radius: 10px;
                padding: 8px;
                color: #333;
                font-size: 18px;
            }
            QPushButton:hover {
                background: #F8F9FA;
                border-color: #2196F3;
            }
        """

        for letters in qwerty_rows:
            # Create a container for each row
            row_container = QWidget()
            row_layout = QHBoxLayout(row_container)
            
            # If it's the second row (ASDFGHJKL), add extra margin
            if len(letters) == 9:  # Second row
                row_layout.setContentsMargins(30, 0, 25, 0)  # Left and right margins
            elif len(letters) == 7:  # Third row (ZXCVBNM)
                row_layout.setContentsMargins(50, 0, 50, 0)
                
            # Add buttons
            for letter in letters:
                btn = QPushButton(letter)
                btn.setFixedSize(50, 50)
                btn.setStyleSheet(self.key_button_styles)
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
                btn = QPushButton(key)
                btn.setFixedSize(50, 50)
                btn.setStyleSheet(self.key_button_styles)
                
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

        space_btn = QPushButton(' ')
        space_btn.setFixedSize(600, 45)
        space_btn.setStyleSheet("""
            QPushButton {
                background: white;
                border: 1px solid #DEDEDE;
                border-radius: 8px;
                color: #333;
                font-size: 14px;
                min-width: 300px;
                margin-left: 70px;
                margin-right: 50px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background: #F8F9FA;
                border-color: #2196F3;
            }
        """)
        space_btn.clicked.connect(lambda: self._on_key_press(' '))
        bottom_row_layout.addWidget(space_btn, 70)

        enter_btn = QPushButton('↵  ENTER')
        enter_btn.setFixedSize(175, 45)
        enter_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
                margin-right: 15px;
            }
            QPushButton:hover {
                background: #1E88E5;
            }
        """)
        enter_btn.clicked.connect(self._on_enter)
        bottom_row_layout.addWidget(enter_btn, 30)

        return bottom_row_widget

    def _on_minimize(self):
        # Store current dimensions before hiding components
        current_width = self.width()
        
        self.keyboard_container.hide()
        self.bottom_row_widget.hide()
        self.minimize_btn.hide()
        self.restore_btn.show()
        self.is_minimized = True
        
        self.adjustSize()  # Let it adjust size based on visible components
        self.setFixedWidth(current_width)  # Force the original width
        
        # Get main window and reposition
        main_window = self.parent().window()
        if main_window:
            # Calculate position to maintain bottom center with margin
            x = (main_window.width() - current_width) // 2
            y = main_window.height() - self.height() - 20  # 20px margin from bottom
            self.move(x, y)

    def _on_restore(self):
        # Store current width before showing components
        current_width = self.width()
        
        self.keyboard_container.show()
        self.bottom_row_widget.show()
        self.restore_btn.hide()
        self.minimize_btn.show()
        self.is_minimized = False
        
        # Get main window and reposition
        main_window = self.parent().window()
        if main_window:
            # Calculate position to maintain bottom center with margin
            keyboard_width = self.sizeHint().width()
            keyboard_height = self.sizeHint().height()
            x = (main_window.width() - keyboard_width) // 2
            y = main_window.height() - keyboard_height - 20  # 20px margin from bottom
            self.move(x, y)

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
            # If minimized, restore before hiding to ensure next show is in full mode
            if self.is_minimized:
                self._on_restore()
            self.hide()
            if self.parent():
                self.parent().keyboard_visible = False

    def set_input(self, input_widget):
        """Set the current input widget"""
        self.current_input = input_widget
        if self.current_input:
            self.current_input.setFocus()

    def show(self):
        """Override show to handle positioning"""
        if self.parent():
            # Get main window
            main_window = self.parent().window()
            if main_window:
                # Calculate keyboard position
                keyboard_width = self.sizeHint().width()
                keyboard_height = self.sizeHint().height()
                x = (main_window.width() - keyboard_width) // 2
                y = main_window.height() - keyboard_height - 20
                self.move(x, y)
        super().show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.pos().y() <= self.handle_height:
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
        # Always restore before hiding to ensure next show is in full mode
        if self.is_minimized:
            self._on_restore()
        super().hide()