from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QGridLayout, QLineEdit, QApplication)
from PyQt5.QtCore import Qt, QEvent, QRect
from PyQt5.QtGui import QPixmap, QPainter, QDoubleValidator
from PyQt5.QtSvg import QSvgRenderer
from typing import Optional
from .manager import KeyboardManager
from styles.keyboard import KeyboardStyles, KeyboardConfig, KeyboardEnabledInputStyles
from .types import KeyboardType

class KeyboardEnabledInput(QLineEdit):
    """Input field that works with the virtual keyboard system"""
    
    def __init__(
        self, 
        parent=None, 
        style_type: str = 'base',
        keyboard_type: KeyboardType = KeyboardType.FULL,
        keyboard_manager: Optional[KeyboardManager] = None
    ):
        """
        Initialize a keyboard-enabled input field.
        
        Args:
            parent: Parent widget
            style_type: Visual style to apply ('base' or 'search')
            keyboard_type: Type of virtual keyboard to display
            keyboard_manager: Optional custom keyboard manager instance
        """
        super().__init__(parent)
        
        # Store configuration
        self.keyboard_type = keyboard_type
        self._style_type = style_type
        
        # Initialize keyboard manager
        self.keyboard_manager = keyboard_manager or KeyboardManager()
        self.keyboard_manager.register_input(self)
        
        # Apply styling based on type
        self._apply_style()
        
        # Set input properties based on keyboard type
        self._configure_input_mode()

    def _apply_style(self) -> None:
        """Apply the appropriate visual style"""
        if self._style_type == 'search':
            self.setStyleSheet(KeyboardEnabledInputStyles.SEARCH_INPUT)
        else:
            self.setStyleSheet(KeyboardEnabledInputStyles.BASE_INPUT)
    
    def _configure_input_mode(self) -> None:
        """Configure input mode and validation based on keyboard type"""
        if self.keyboard_type in [KeyboardType.NUMERIC, KeyboardType.DECIMAL, KeyboardType.PHONE]:
            # For numeric types, only allow numbers
            self.setInputMethodHints(Qt.ImhDigitsOnly)
            
            if self.keyboard_type == KeyboardType.PHONE:
                self.setInputMask("999-999-9999;_")
            elif self.keyboard_type == KeyboardType.DECIMAL:
                self.setValidator(QDoubleValidator())
        
        elif self.keyboard_type == KeyboardType.EMAIL:
            self.setInputMethodHints(Qt.ImhEmailCharactersOnly)

    def show_keyboard(self) -> None:
        """Show the virtual keyboard with appropriate configuration"""
        if self.keyboard_manager:
            # Pass keyboard type to show_keyboard for layout configuration
            self.keyboard_manager.show_keyboard(self, self.keyboard_type)
    
    def mousePressEvent(self, event) -> None:
        """Handle mouse press events to show keyboard"""
        super().mousePressEvent(event)
        self.show_keyboard()
    
    def focusInEvent(self, event) -> None:
        """Handle focus events to show keyboard"""
        super().focusInEvent(event)
        self.show_keyboard()
    
    def __del__(self) -> None:
        """Clean up by unregistering from keyboard manager"""
        if hasattr(self, 'keyboard_manager'):
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
        self.is_filtering = False
        # Load configuration
        self.config = KeyboardConfig.get_instance() 
        self.dimensions = self.config.get_dimensions()
        self.layout_config = self.config.get_layout()
        
        # Track current keyboard type
        self.current_keyboard_type = KeyboardType.FULL
        
        self._setup_ui()
        self.hide()

    def _setup_ui(self):
        """Initialize the keyboard UI"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(*self.layout_config['main_margins'])
        self.main_layout.setSpacing(self.layout_config['main_spacing'])

        # Handle bar
        self._setup_handle_bar()

        # Keyboard container
        self.keyboard_container = QWidget()
        self.main_layout.addWidget(self.keyboard_container)

        # Create initial keyboard layout
        self._update_keyboard_layout()

        # Bottom row with space and enter
        self.bottom_row_widget = self._create_bottom_row()
        self.main_layout.addWidget(self.bottom_row_widget)

        # Apply base styles
        self.setStyleSheet(KeyboardStyles.KEYBOARD_BASE)

    def _setup_handle_bar(self):
        """Setup the drag handle bar with controls"""
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
        self.close_btn = QPushButton("×")
        
        self.minimize_btn.setFixedSize(self.dimensions['control_button_size'], 
                                     self.dimensions['control_button_size'])
        self.restore_btn.setFixedSize(self.dimensions['control_button_size'], 
                                    self.dimensions['control_button_size'])
        self.close_btn.setFixedSize(self.dimensions['control_button_size'], 
                                    self.dimensions['control_button_size'])
        
        self.minimize_btn.setStyleSheet(KeyboardStyles.CONTROL_BUTTONS)
        self.restore_btn.setStyleSheet(KeyboardStyles.CONTROL_BUTTONS)
        self.close_btn.setStyleSheet(KeyboardStyles.CONTROL_BUTTONS)
        
        self.minimize_btn.clicked.connect(self._on_minimize)
        self.restore_btn.clicked.connect(self._on_restore)
        self.close_btn.clicked.connect(self._on_close)
        
        self.handle_layout.addWidget(self.minimize_btn)
        self.handle_layout.addWidget(self.restore_btn)
        self.handle_layout.addWidget(self.close_btn)
        self.restore_btn.hide()

        self.main_layout.addWidget(self.drag_handle)

    def _update_keyboard_layout(self):
        """Update the keyboard layout based on current type"""
        self._clear_keyboard_layout()
        
        if self.current_keyboard_type in [KeyboardType.NUMERIC, KeyboardType.DECIMAL, KeyboardType.PHONE]:
            self._create_numeric_keyboard()
        elif self.current_keyboard_type == KeyboardType.EMAIL:
            self._create_email_keyboard()
        elif self.current_keyboard_type == KeyboardType.SEARCH:
            self._create_full_keyboard()  # Same as full but with search-specific keys
        else:
            self._create_full_keyboard()

    def _clear_keyboard_layout(self):
        """Remove all widgets from the keyboard container"""
        if self.keyboard_container.layout():
            while self.keyboard_container.layout().count():
                item = self.keyboard_container.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

    def _create_full_keyboard(self):
        """Create standard QWERTY keyboard layout"""
        keyboard_layout = QHBoxLayout(self.keyboard_container)
        keyboard_layout.setSpacing(5)

        # QWERTY Section
        qwerty_widget = self._create_qwerty_section()
        keyboard_layout.addWidget(qwerty_widget, stretch=7)

        # Numpad Section
        numpad_widget = self._create_numpad_section()
        keyboard_layout.addWidget(numpad_widget, stretch=3)

    def _create_numeric_keyboard(self):
        """Create numeric-only keyboard layout"""
        layout = QGridLayout(self.keyboard_container)
        layout.setSpacing(10)
        
        # Add number keys (0-9)
        numbers = ['7', '8', '9', '4', '5', '6', '1', '2', '3', '0']
        positions = [(i // 3, i % 3) for i in range(len(numbers))]
        
        for number, pos in zip(numbers, positions):
            btn = self._create_key_button(number)
            btn.clicked.connect(lambda checked, n=number: self._on_key_press(n))
            layout.addWidget(btn, *pos)
        
        # Add additional keys based on keyboard type
        if self.current_keyboard_type == KeyboardType.DECIMAL:
            decimal = self._create_key_button('.')
            decimal.clicked.connect(lambda: self._on_key_press('.'))
            layout.addWidget(decimal, 3, 1)
        
        # Add backspace and clear
        backspace = self._create_key_button('⌫')
        backspace.clicked.connect(self._on_backspace)
        layout.addWidget(backspace, 3, 2)
        
        clear = self._create_key_button('CLR')
        clear.clicked.connect(self._on_clear)
        layout.addWidget(clear, 3, 0)

    def _create_qwerty_section(self):
        """Create the QWERTY section of the keyboard"""
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
        """Create the numpad section of the keyboard"""
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

    def _create_email_keyboard(self):
        """Create email-specific keyboard layout"""
        self._create_full_keyboard()
        # Add email-specific buttons (like @, .com, etc.)
        # This can be expanded based on requirements

    def _create_bottom_row(self):
        """Create the bottom row with space and enter buttons"""
        bottom_row_widget = QWidget()
        bottom_row_layout = QHBoxLayout(bottom_row_widget)
        bottom_row_layout.setSpacing(5)

        # Space button
        space_btn = self._create_space_button()
        space_btn.clicked.connect(lambda: self._on_key_press(' '))
        bottom_row_layout.addWidget(space_btn, 70)

        # Enter button
        enter_btn = self._create_enter_button()
        enter_btn.clicked.connect(self._on_close)
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
        btn.clicked.connect(self._on_enter)  # Keep original enter functionality
        return btn

    def set_input(self, input_widget, keyboard_type=KeyboardType.FULL):
        """Set the current input widget and keyboard type"""
        self.current_input = input_widget
        if keyboard_type != self.current_keyboard_type:
            self.current_keyboard_type = keyboard_type
            self._update_keyboard_layout()
        
        if self.current_input:
            self.current_input.setFocus()

    def _on_key_press(self, key):
        """Handle key press events"""
        if self.current_input:
            cursor_pos = self.current_input.cursorPosition()
            current_text = self.current_input.text()
            new_text = current_text[:cursor_pos] + key + current_text[cursor_pos:]
            self.current_input.setText(new_text)
            self.current_input.setCursorPosition(cursor_pos + 1)
            self.current_input.setFocus()

    def _on_backspace(self):
        """Handle backspace key press"""
        if self.current_input:
            cursor_pos = self.current_input.cursorPosition()
            current_text = self.current_input.text()
            if cursor_pos > 0:
                new_text = current_text[:cursor_pos-1] + current_text[cursor_pos:]
                self.current_input.setText(new_text)
                self.current_input.setCursorPosition(cursor_pos - 1)
            self.current_input.setFocus()

    def _on_clear(self):
        """Handle clear key press"""
        if self.current_input:
            self.current_input.clear()
            self.current_input.setFocus()

    def _on_close(self):
        """Handle close button press to hide keyboard and cleanup"""
        if self.current_input:
            if self.is_minimized:
                self._on_restore()
            self.hide()
            if self.parent():
                self.parent().keyboard_visible = False

    def _on_minimize(self):
        """Handle minimize button press"""
        self.close_btn.show() 
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
        """Handle restore button press"""
        # current_width = self.width()
        self.close_btn.show()
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

    def _on_enter(self):
        """Handle enter key press to complete input and emit signal"""
        if self.current_input:
            # Trigger any input completion behavior
            self.current_input.returnPressed.emit()
            
            # Update focus and cursor position
            self.current_input.setFocus()
            cursor_pos = self.current_input.cursorPosition()
            self.current_input.setCursorPosition(cursor_pos)
            
            # Hide keyboard if not minimized
            if not self.is_minimized:
                self.hide()
                if self.parent():
                    self.parent().keyboard_visible = False

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

                # Install event filter if not already filtering
                if not self.is_filtering:
                    QApplication.instance().installEventFilter(self)
                    self.is_filtering = True
        super().show()

    # Mouse event handlers for dragging
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
                    self._on_close()
                    
                return False  # Let the event propagate to handle product clicks
                    
        return False  # Let other widgets handle the event