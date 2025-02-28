from PyQt5.QtWidgets import QVBoxLayout, QFrame, QPushButton, QGridLayout, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal
from .types import NumpadMode, NumpadState
from .manager import NumpadManager

# Import from both locations for transitional period
from styles.numpad import NumpadStyles
from config.layouts.numpad_layout import numpad_layout_config

class NumpadWidget(QFrame):
    """
    Numpad widget that can operate in both standalone and input-bound modes.
    
    Signals:
        value_changed(str): Emitted when input value changes
        value_committed(str): Emitted when value is committed (e.g., Enter pressed)
    """
    value_changed = pyqtSignal(str)
    value_committed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = NumpadManager()
        self._current_value = "0"
        self._state = NumpadState.STANDALONE
        self._mode = NumpadMode.DEFAULT
        self._bound_input = None

        # Use the new layout configuration
        self.layout_config_instance = numpad_layout_config
        self.dimensions = self.layout_config_instance.get_dimensions()
        self.layout_config = self.layout_config_instance.get_layout()

        self._setup_ui()
        
    # Rest of the class stays the same...
    
    # Update style methods to use the new config
    def _create_display(self):
        """Create the number display"""
        display = QLineEdit()
        display.setAlignment(Qt.AlignRight)
        display.setReadOnly(True)
        display.setText("0")
        
        # Use the centralized style
        display.setStyleSheet(NumpadStyles.get_display_style(self.layout_config_instance))
        
        return display

    def _create_number_grid(self):
        """Create the number button grid"""
        # Use the centralized style
        button_style = NumpadStyles.get_number_button_style(self.layout_config_instance)
        
        # Rest of the method stays the same...