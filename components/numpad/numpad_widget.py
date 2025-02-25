from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFrame, 
                             QPushButton, QGridLayout, QLineEdit)
from PyQt5.QtCore import Qt, pyqtSignal
from .types import NumpadMode, NumpadState
from .manager import NumpadManager
from styles.numpad import NumpadStyles, NumpadConfig

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

        # Get the configuration
        self.config = NumpadConfig.get_instance()
        self.dimensions = self.config.get_dimensions()
        self.layout = self.config.get_layout()

        self._setup_ui()
        
    def _setup_ui(self):
        """Initialize the numpad UI"""
        # Get the configuration
        self.config = NumpadConfig.get_instance()
        self.dimensions = self.config.get_dimensions()
        self.layout_config = self.config.get_layout()
        
        # Apply container style
        self.setStyleSheet(NumpadStyles.CONTAINER)
        
        # Main layout
        layout = QVBoxLayout(self)
        margins = self.layout_config['main_margins']
        layout.setContentsMargins(*margins)
        layout.setSpacing(self.layout_config['grid_spacing'])
        
        # Create display
        self.display = self._create_display()
        layout.addWidget(self.display)
        
        # Create number grid
        self.grid_container = QFrame()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setContentsMargins(*self.layout_config['grid_margins'])
        self.grid_layout.setSpacing(self.layout_config['grid_spacing'])
        
        self._create_number_grid()
        layout.addWidget(self.grid_container)

    def bind_to_input(self, input_widget, mode: NumpadMode):
        """
        Bind numpad to an input widget with specific mode.
        Future implementation will handle input field binding.
        """
        self._state = NumpadState.INPUT_BOUND
        self._mode = mode
        self._bound_input = input_widget
        # Additional binding logic will go here

    def unbind_input(self):
        """
        Unbind from input and return to standalone mode.
        """
        self._state = NumpadState.STANDALONE
        self._mode = NumpadMode.DEFAULT
        self._bound_input = None
        self.clear()

    def _create_display(self):
        """Create the number display"""
        display = QLineEdit()
        display.setAlignment(Qt.AlignRight)
        display.setReadOnly(True)
        display.setText("0")
        
        # Use the centralized style
        display.setStyleSheet(NumpadStyles.get_display_style(self.config))
        
        return display

    def _create_number_grid(self):
        """Create the number button grid"""
        # Use the centralized style
        button_style = NumpadStyles.get_number_button_style(self.config)
        
        # Create number buttons (1-9)
        numbers = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['.', '0', '⌫']
        ]
        
        for i, row in enumerate(numbers):
            for j, num in enumerate(row):
                btn = QPushButton(num)
                btn.setStyleSheet(button_style)
                if num == '⌫':
                    btn.clicked.connect(self._on_backspace)
                elif num == '.':
                    btn.clicked.connect(lambda _, n=num: self._on_number_click(n))
                else:
                    btn.clicked.connect(lambda _, n=num: self._on_number_click(n))
                self.grid_layout.addWidget(btn, i, j)

    def _on_number_click(self, number: str) -> None:
        """Handle number button clicks"""
        # Basic input handling (same for all modes initially)
        current_value = self._current_value
        
        if number == '.':
            if '.' in current_value:
                return
            if current_value == "":
                new_value = "0."
            else:
                new_value = current_value + "."
        else:
            if current_value == "0" and number != ".":
                current_value = ""
            new_value = current_value + number

        # Update value
        self._current_value = new_value
        self._update_display()
        
        # Emit value based on state
        if self._state == NumpadState.STANDALONE:
            self.value_changed.emit(new_value)
        else:
            # Future: Handle input-bound validation and updates
            pass

    def _on_backspace(self) -> None:
        """Handle backspace button click"""
        if len(self._current_value) > 1:
            self._current_value = self._current_value[:-1]
        else:
            self._current_value = "0"
        self._update_display()
        
        if self._state == NumpadState.STANDALONE:
            self.value_changed.emit(self._current_value)

    def _update_display(self) -> None:
        """Update the display with current value"""
        self.display.setText(self._current_value)

    def clear(self) -> None:
        """Clear the current value"""
        self._current_value = "0"
        self._update_display()
        if self._state == NumpadState.STANDALONE:
            self.value_changed.emit(self._current_value)

    def get_value(self) -> str:
        """Get the current numeric value"""
        return self._current_value

    def keyPressEvent(self, event):
        """Handle keyboard input"""
        if event.key() >= Qt.Key_0 and event.key() <= Qt.Key_9:
            self._on_number_click(event.text())
        elif event.key() == Qt.Key_Period:
            self._on_number_click('.')
        elif event.key() in [Qt.Key_Backspace, Qt.Key_Delete]:
            self._on_backspace()
        elif event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            self.value_committed.emit(self._current_value)
        else:
            super().keyPressEvent(event)