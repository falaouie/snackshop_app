from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QFrame, QGridLayout, QLineEdit)
from PyQt5.QtCore import Qt, pyqtSignal
from .manager import NumpadManager
from .styles import NumpadStyles, NumpadConfig
from .types import NumpadMode, NumpadState

class NumpadWidget(QFrame):
    """
    Numpad widget with multiple modes and states
    
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
        
        # Set initial state
        self.current_mode = NumpadMode.QTY
        self.current_state = NumpadState.STANDALONE

        # Add internal value tracking
        self._current_value = "0"  # Stores actual value without formatting

        self._setup_ui()
        
    def _setup_ui(self):
        """Initialize the numpad UI"""
        self.setStyleSheet(NumpadStyles.CONTAINER)
        
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(*self.layout_config['main_margins'])
        main_layout.setSpacing(self.dimensions['spacing'])
        
        # Add mode buttons (left side)
        mode_container = self._create_mode_buttons()
        main_layout.addWidget(mode_container)
        
        # Create right side container (display + numpad)
        right_container = QFrame()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(self.dimensions['spacing'])
        
        # Add display
        self.display = self._create_display()
        right_layout.addWidget(self.display)
        
        # Add number grid
        number_grid = self._create_number_grid()
        right_layout.addWidget(number_grid)
        
        main_layout.addWidget(right_container)

    def _create_mode_buttons(self):
        """Create the mode selection buttons"""
        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # Create mode buttons
        self.mode_buttons = {}
        for mode in NumpadMode:
            btn = QPushButton(mode.name)
            btn.setCheckable(True)
            btn.setStyleSheet(NumpadStyles.MODE_BUTTON)
            btn.clicked.connect(lambda checked, m=mode: self._on_mode_change(m))
            layout.addWidget(btn)
            self.mode_buttons[mode] = btn
        
        # Set initial mode
        self.mode_buttons[NumpadMode.QTY].setChecked(True)
        
        layout.addStretch()
        return container

    def _create_display(self):
        """Create the number display"""
        display = QLineEdit()
        display.setAlignment(Qt.AlignRight)
        display.setReadOnly(True)
        display.setText("0")
        display.setStyleSheet(NumpadStyles.DISPLAY)
        return display

    def _create_number_grid(self):
        """Create the number button grid"""
        container = QFrame()
        layout = QGridLayout(container)
        layout.setContentsMargins(*self.layout_config['grid_margins'])
        layout.setSpacing(self.layout_config['grid_spacing'])
        
        # Create number buttons
        numbers = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['0', '.', 'C']
        ]
        
        # Store buttons that might need updating
        self.dynamic_buttons = {}
        
        for i, row in enumerate(numbers):
            for j, num in enumerate(row):
                btn = QPushButton(num)
                btn.setStyleSheet(NumpadStyles.NUMBER_BUTTON)
                
                if num == '.':
                    # Store reference to decimal/triple zero button
                    self.dynamic_buttons['decimal'] = btn
                    # Don't connect yet - will be connected based on mode
                elif num == 'C':
                    btn.clicked.connect(self._on_clear)
                else:
                    btn.clicked.connect(lambda checked, n=num: self._on_number_click(n))
                
                layout.addWidget(btn, i, j)

        # Create Enter button that spans the rightmost column
        enter_btn = QPushButton('Enter')
        enter_btn.setStyleSheet(NumpadStyles.ENTER_BUTTON)
        enter_btn.clicked.connect(self._on_enter)
        layout.addWidget(enter_btn, 0, 3, 4, 1)  # Span 4 rows

        # Initialize dynamic button state
        self._update_dynamic_buttons()

        return container
    
    def _update_dynamic_buttons(self):
        """Update dynamic buttons based on current mode"""
        if not hasattr(self, 'dynamic_buttons'):
            return
            
        decimal_btn = self.dynamic_buttons.get('decimal')
        if not decimal_btn:
            return
            
        # Disconnect any existing connections
        try:
            decimal_btn.clicked.disconnect()
        except:
            pass
            
        if self.current_mode == NumpadMode.LBP:
            # Set up for LBP mode
            decimal_btn.setText('000')
            decimal_btn.clicked.connect(lambda: self._on_number_click('000'))
        else:
            # Set up for other modes
            decimal_btn.setText('.')
            decimal_btn.clicked.connect(lambda: self._on_number_click('.'))

    def _on_number_click(self, number: str) -> None:
        """
        Handle number button clicks
        
        Args:
            number: The number, decimal point, or '000' that was clicked
        """
        # Get the actual (unformatted) current value
        current_value = self._current_value
        
        # Special handling for '000' in LBP mode
        if number == '000' and self.current_mode == NumpadMode.LBP:
            if current_value == "0":
                return
            new_value = current_value + "000"
        else:
            # Handle initial state and zero
            if current_value == "0" and number != ".":
                current_value = ""
                
            # Handle decimal point
            if number == ".":
                if "." in current_value:  # Prevent multiple decimal points
                    return
                if not current_value:  # If empty, add leading zero
                    current_value = "0"
                    
            new_value = current_value + number

        # Validate input based on current mode
        if self.manager.validate_input(new_value, self.current_mode):
            self._current_value = new_value
            self._update_display()

    def _on_clear(self) -> None:
        """Handle clear button click"""
        self._current_value = "0"
        self._update_display()

    def _on_enter(self) -> None:
        """
        Handle enter button click
        Emits the value_entered signal with unformatted value and mode
        """
        # Use the unformatted value when emitting
        formatted_value = self.manager.format_value(self._current_value, self.current_mode)
        self.value_entered.emit(formatted_value, self.current_mode)
        self._on_clear()  # Reset display after emitting

    def _on_mode_change(self, mode: NumpadMode) -> None:
        """
        Handle mode button clicks
        
        Args:
            mode: The NumpadMode that was selected
        """
        # Update selected button states
        for m, btn in self.mode_buttons.items():
            btn.setChecked(m == mode)
            
        self.current_mode = mode
        self._update_dynamic_buttons()
        self._on_clear()  # Reset display on mode change
        self.mode_changed.emit(mode)

    def set_state(self, state: NumpadState) -> None:
        """
        Set the numpad state (standalone vs input-bound)
        Future: Will handle switching between standalone and input-bound modes
        
        Args:
            state: The NumpadState to set
        """
        self.current_state = state
        # Future: Update UI based on state
        # - Show/hide relevant mode buttons
        # - Adjust validation rules
        # - Update event handling

    def enable_modes(self, modes: list) -> None:
        """
        Enable specific modes and disable others
        Future: Will be used for input-bound state to show only relevant modes
        
        Args:
            modes: List of NumpadMode to enable
        """
        for mode, btn in self.mode_buttons.items():
            btn.setEnabled(mode in modes)
            if mode not in modes and btn.isChecked():
                # If current mode is disabled, switch to first enabled mode
                self._on_mode_change(modes[0])

    def get_value(self) -> str:
        """
        Get the current unformatted value
        
        Returns:
            str: The current value without formatting
        """
        return self._current_value

    def reset(self) -> None:
        """Reset the numpad to initial state"""
        self._on_clear()
        self._on_mode_change(NumpadMode.QTY)

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
                # Convert to float and format with 2 decimal places and thousands separator
                num_value = float(clean_value)
                # Split into integer and decimal parts
                int_part = int(num_value)
                dec_part = round((num_value - int_part) * 100)
                
                # Format integer part with commas
                formatted_int = "{:,}".format(int_part)
                # Ensure decimal part is two digits
                formatted_dec = f"{dec_part:02d}"
                
                return f"{formatted_int}.{formatted_dec}"
                
            elif self.current_mode == NumpadMode.LBP:
                # Remove any decimal portion and format with commas
                num_value = int(float(clean_value))
                return "{:,}".format(num_value)
                
            else:
                # For QTY and WGT modes, return as is
                return clean_value
                
        except ValueError:
            return "0"
        
    def _update_display(self) -> None:
        """Update the display with formatted value"""
        formatted_value = self._format_display_value(self._current_value)
        self.display.setText(formatted_value)