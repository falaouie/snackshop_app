def __init__(self, user_id, parent=None):
    super().__init__(parent)
    self.user_id = user_id
    self._setup_ui()
    
    # Set up timer for updating window title
    self.window_title_timer = QTimer()
    self.window_title_timer.timeout.connect(self._update_window_title)
    self.window_title_timer.start(1000)  # Update every second
    self._update_window_title()  # Initial update

def _update_window_title(self):
    if self.window():  # Check if we have a parent window
        current_time = QDateTime.currentDateTime().toString('dd-MM-yyyy hh:mm:ss')
        title = f"Snack Shop POS - Cashier: {self.user_id} - {current_time}"
        self.window().setWindowTitle(title)