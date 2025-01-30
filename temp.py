class DigitBox(QLabel):
    def __init__(self, is_pin=False):
        super().__init__()
        self.is_pin = is_pin  # Whether to mask input (for PIN)
        # Get sizes from config
        digit_width = screen_config.get_size('digit_input_width')
        digit_height = screen_config.get_size('digit_input_height')
        self.setFixedSize(digit_width, digit_height)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(styles.AuthStyles.DIGIT_BOX_EMPTY)

class UserInput(QWidget):
    input_changed = pyqtSignal(list)  # Signal when input changes
    
    def __init__(self, is_pin=False):
        super().__init__()
        self.is_pin = is_pin  # Whether this is a PIN input
        self.digits = ["", "", "", ""]  # Track input digits
        self.current_position = 0       # Current digit being edited
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QHBoxLayout()
        # Get margin and spacing from config
        digit_margin = screen_config.get_size('container_margin')
        digit_spacing = screen_config.get_size('section_spacing')
        layout.setContentsMargins(0, digit_margin//2, 0, digit_margin//2)
        layout.setSpacing(digit_spacing)