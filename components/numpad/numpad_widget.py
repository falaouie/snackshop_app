from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QFrame, QGridLayout, QLineEdit)
from PyQt5.QtCore import Qt, pyqtSignal
from .manager import NumpadManager
from .styles import NumpadStyles, NumpadConfig
from .types import NumpadMode, NumpadState

class NumpadWidget(QFrame):
    """
    Numpad widget with quantity input functionality
    
    Signals:
        value_entered(str, NumpadMode): Emitted when a value is confirmed
        mode_changed(NumpadMode): Emitted when mode changes
    """
    
    # Signals
    value_entered = pyqtSignal(str, object)  # (value, mode)
    mode_changed = pyqtSignal(object)  # (mode)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize configurations
        self.manager = NumpadManager()
        self.manager.register_numpad(self)
        self.config = NumpadConfig()
        self.dimensions = self.config.get_dimensions()
        self.layout_config = self.config.get_layout()
        
        # Set initial state and mode
        self.current_mode = NumpadMode.QTY
        self.current_state = NumpadState.STANDALONE

        # Add internal value tracking
        self._current_value = "0"  # Stores actual value without formatting

        self._setup_ui()
        
    def _setup_ui(self):
        """Initialize the numpad UI"""
        self.setStyleSheet(NumpadStyles.CONTAINER)
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(*self.layout_config['main_margins'])
        main_layout.setSpacing(self.dimensions['spacing'])
        
        # Create display row with QTY button
        display_row = self._create_display_row()
        main_layout.addWidget(display_row)
        
        self.grid_container = QFrame()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setContentsMargins(*self.layout_config['grid_margins'])
        self.grid_layout.setSpacing(self.layout_config['grid_spacing'])
        
        # Initialize with number grid
        self._create_number_grid()
        main_layout.addWidget(self.grid_container)

    def set_currency_mode(self, mode: NumpadMode):
        """Set the currency input mode"""
        self.current_mode = mode
        self._current_value = "0"  # Reset value on mode change
        self._create_number_grid()  # Recreate grid with new mode
        self._update_display()
        self.mode_changed.emit(mode)
        
        # Update QTY button state
        self.qty_button.setChecked(mode == NumpadMode.QTY)

    def _create_display_row(self):
        """Create row containing QTY button and display"""
        container = QFrame()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self.layout_config['display_row_spacing'])
        
        # Create QTY button
        self.qty_button = QPushButton('QTY')
        self.qty_button.setCheckable(True)
        self.qty_button.setChecked(self.current_mode == NumpadMode.QTY)
        self.qty_button.setStyleSheet(NumpadStyles.QTY_BUTTON)
        self.qty_button.clicked.connect(self._on_qty_clicked)
        layout.addWidget(self.qty_button)
        
        # Create display with adjusted width
        self.display = self._create_display()
        layout.addWidget(self.display)
        
        return container
    
    def _on_qty_clicked(self):
        """Handle QTY button click"""
        self.set_currency_mode(NumpadMode.QTY)
        self.qty_button.setChecked(True)  # Ensure it stays checked in QTY mode

    def _create_display(self):
        """Create the number display"""
        display = QLineEdit()
        display.setAlignment(Qt.AlignRight)
        display.setReadOnly(True)
        display.setText("0")
        display.setStyleSheet(NumpadStyles.DISPLAY)
        
        # Calculate adjusted width
        total_width = self.dimensions['width']
        qty_button_width = self.dimensions['qty_button_size']
        spacing = self.layout_config['display_row_spacing']
        display_width = total_width - qty_button_width - spacing - (self.layout_config['main_margins'][0] * 2)
        
        display.setFixedWidth(display_width)
        return display

    def _create_number_grid(self):
        """Create the number button grid"""
        # Clear existing grid
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        # Create number buttons (1-9)
        numbers = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3']
        ]
        
        for i, row in enumerate(numbers):
            for j, num in enumerate(row):
                btn = QPushButton(num)
                btn.setStyleSheet(NumpadStyles.NUMBER_BUTTON)
                btn.clicked.connect(lambda checked, n=num: self._on_number_click(n))
                self.grid_layout.addWidget(btn, i, j)

        # Create bottom row based on mode
        self._create_bottom_row()
    
    def _create_bottom_row(self):
        """Create bottom row based on current mode"""
        # Create mode-specific left button
        if self.current_mode == NumpadMode.USD:
            left_btn = QPushButton('.')
            left_btn.clicked.connect(lambda: self._on_number_click('.'))
        elif self.current_mode == NumpadMode.LBP:
            left_btn = QPushButton('000')
            left_btn.clicked.connect(lambda: self._on_number_click('000'))
        else:  # QTY mode
            left_btn = QPushButton('C')
            left_btn.clicked.connect(self._on_clear)
        
        left_btn.setStyleSheet(NumpadStyles.NUMBER_BUTTON)
        self.grid_layout.addWidget(left_btn, 3, 0)

        # Create zero button (center)
        zero_btn = QPushButton('0')
        zero_btn.setStyleSheet(NumpadStyles.NUMBER_BUTTON)
        zero_btn.clicked.connect(lambda: self._on_number_click('0'))
        self.grid_layout.addWidget(zero_btn, 3, 1)

        # Create backspace button (right)
        backspace_btn = QPushButton('⌫')
        backspace_btn.setStyleSheet(NumpadStyles.NUMBER_BUTTON)
        backspace_btn.clicked.connect(self._on_backspace)
        self.grid_layout.addWidget(backspace_btn, 3, 2)

    def _on_number_click(self, number: str) -> None:
        """Handle number button clicks"""
        current_value = self._current_value
        
        if number == '000' and self.current_mode == NumpadMode.LBP:
            if current_value == "0":
                return
            new_value = current_value + "000"
        elif number == '.':
            if self.current_mode != NumpadMode.USD or '.' in current_value:
                return
            if current_value == "":
                new_value = "0."
            else:
                new_value = current_value + "."
        else:
            if current_value == "0" and number != ".":
                current_value = ""
            new_value = current_value + number

        # Validate using clean value
        if self.manager.validate_input(new_value, self.current_mode):
            self._current_value = new_value  # Store clean value
            self._update_display()  # Display formatted value

    def _on_clear(self) -> None:
        """Handle clear button click"""
        self._current_value = "0"
        self._update_display()

    def _on_backspace(self) -> None:
        """Handle backspace button click"""
        if len(self._current_value) > 1:
            self._current_value = self._current_value[:-1]
        else:
            self._current_value = "0"
        self._update_display()

    def _update_display(self) -> None:
        """Update the display with formatted value"""
        formatted_value = self._format_display_value(self._current_value)
        self.display.setText(formatted_value)

    def _format_display_value(self, value: str) -> str:
        """
        Format the display value based on current mode
        
        Args:
            value: The raw value to format
            
        Returns:
            str: Formatted value for display
        """
        if not value or value == ".":
            return "0"
            
        try:
            # Remove any existing formatting
            clean_value = value.replace(",", "")
            
            if self.current_mode == NumpadMode.USD:
                # Handle decimal input in progress
                if clean_value.endswith('.'):
                    # Split for proper formatting of the whole number part
                    whole_part = clean_value[:-1]
                    if whole_part:
                        formatted_whole = "{:,}".format(int(whole_part))
                        return formatted_whole + "."
                    return "0."
                
                # Format with 2 decimal places and thousands separator
                num_value = float(clean_value)
                return "{:,.2f}".format(num_value)
                
            elif self.current_mode == NumpadMode.LBP:
                # Format with thousands separator, no decimals
                num_value = int(float(clean_value))
                return "{:,}".format(num_value)
                
            else:  # QTY mode
                # Format with thousands separator, no decimals
                num_value = int(float(clean_value))
                return "{:,}".format(num_value)
                
        except ValueError:
            return "0"

    def keyPressEvent(self, event):
        """Handle keyboard input"""
        if event.key() >= Qt.Key_0 and event.key() <= Qt.Key_9:
            self._on_number_click(event.text())
        elif event.key() == Qt.Key_Period and self.current_mode == NumpadMode.USD:
            self._on_number_click('.')
        elif event.key() in [Qt.Key_Backspace, Qt.Key_Delete]:
            self._on_backspace()
        else:
            super().keyPressEvent(event)

    def focusInEvent(self, event):
        """Handle focus to enable keyboard input"""
        super().focusInEvent(event)
        self.setFocus()