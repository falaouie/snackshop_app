from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from styles import ButtonStyles
from styles.layouts import layout_config
from button_definitions.types import HorizontalButtonType
from button_definitions.horizontal import HorizontalButtonConfig

class HorizontalButtonsWidget(QFrame):
    """Widget for horizontal action buttons in order panel"""
    
    # Signals
    action_triggered = pyqtSignal(str)  # Emits the triggered action type
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_config = layout_config.get_instance()
        self.horizontal_buttons = {}  # Store buttons for reference
        self.active_action = None  # Track active action if needed
        
        self.setStyleSheet("""
            QFrame {
                background: white;
                border-left: 1px solid #DEDEDE;
                border-top: 1px solid #DEDEDE;
            }
        """)
        self._setup_ui()

    def _setup_ui(self):
        """Initialize the UI"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 10, 0, 10)
        main_layout.setSpacing(8)
        
        self._create_buttons(main_layout)

    def _create_buttons(self, layout):
        """Create horizontal action buttons"""
        button_config = self.layout_config.get_button_config('horizontal')
        
        for button_type in HorizontalButtonType:
            config = HorizontalButtonConfig.get_config(button_type)
            if config:  # Only create button if config exists
                btn = QPushButton(config['text'])
                btn.setStyleSheet(ButtonStyles.get_horizontal_button_style(button_type))
                btn.setFixedSize(
                    button_config['width'],
                    button_config['height']
                )
                
                # Connect button handlers
                btn.clicked.connect(
                    lambda checked, type=button_type.value: self._handle_action_triggered(type)
                )
                
                # Connect specific action if defined
                if config.get('action'):
                    btn.clicked.connect(getattr(self, config['action']))
                
                # Store button reference
                self.horizontal_buttons[button_type.value] = btn
                layout.addWidget(btn)

    def _handle_action_triggered(self, action_type):
        """Handle button action trigger"""
        self.active_action = action_type
        self.action_triggered.emit(action_type)

    # Action handlers
    def hold_order(self):
        """Handle hold order action"""
        print("Horizontal Hold button clicked")

    def void_order(self):
        """Handle void order action"""
        print("Horizontal Void button clicked")

    def no_sale(self):
        """Handle no sale action"""
        print("Horizontal No Sale button clicked")