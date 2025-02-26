# components/keyboard/keyboard.py
# Update the following methods:

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
    
    # Set fixed size from dimensions config
    self.minimize_btn.setFixedSize(self.dimensions['control_button_size'], 
                               self.dimensions['control_button_size'])
    self.restore_btn.setFixedSize(self.dimensions['control_button_size'], 
                                self.dimensions['control_button_size'])
    self.close_btn.setFixedSize(self.dimensions['control_button_size'], 
                                self.dimensions['control_button_size'])
    
    # Use enhanced control button style from KeyboardStyles
    control_style = KeyboardStyles.get_control_button_style(self.config)
    self.minimize_btn.setStyleSheet(control_style)
    self.restore_btn.setStyleSheet(control_style)
    self.close_btn.setStyleSheet(control_style)
    
    self.minimize_btn.clicked.connect(self._on_minimize)
    self.restore_btn.clicked.connect(self._on_restore)
    self.close_btn.clicked.connect(self._on_close)
    
    self.handle_layout.addWidget(self.minimize_btn)
    self.handle_layout.addWidget(self.restore_btn)
    self.handle_layout.addWidget(self.close_btn)
    self.restore_btn.hide()

    self.main_layout.addWidget(self.drag_handle)

def _create_key_button(self, text, size=None):
    """Create a standard keyboard key button"""
    btn = QPushButton(text)
    if size:
        btn.setFixedSize(*size)
    else:
        btn.setFixedSize(self.dimensions['key_width'], 
                       self.dimensions['key_height'])
    # Use enhanced key style from KeyboardStyles
    btn.setStyleSheet(KeyboardStyles.get_key_style(self.config))
    return btn

def _create_space_button(self):
    """Create the space bar button"""
    btn = QPushButton(' ')
    btn.setFixedSize(self.dimensions['space_width'], 
                    self.dimensions['space_height'])
    # Use enhanced space key style
    btn.setStyleSheet(KeyboardStyles.get_space_key_style(self.config))
    return btn

def _create_enter_button(self):
    """Create the enter button"""
    btn = QPushButton('↵  ENTER')
    btn.setFixedSize(self.dimensions['enter_width'], 
                    self.dimensions['enter_height'])
    # Use enhanced enter key style
    btn.setStyleSheet(KeyboardStyles.get_enter_key_style(self.config))
    btn.clicked.connect(self._on_enter)
    return btn