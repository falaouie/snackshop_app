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

    # ... [rest of the implementation remains the same] ...

    def _handle_action_triggered(self, action_type):
        """Handle button action trigger"""
        self.active_action = action_type
        self.action_triggered.emit(action_type)

    # Remove get_active_action method to maintain consistency with OrderTypeWidget