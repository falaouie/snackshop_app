from PyQt5.QtWidgets import QApplication, QMainWindow, QToolButton, QMenu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the settings button
        self.settings_button = QToolButton(self)
        self.settings_button.setText("⋮")  # Unicode for vertical dots
        self.settings_button.setStyleSheet("font-size: 18px; border: none;")  # Adjust styling
        self.settings_button.setPopupMode(QToolButton.InstantPopup)

        # Create a menu
        menu = QMenu(self)
        menu.addAction("Option 1")
        menu.addAction("Option 2")
        self.settings_button.setMenu(menu)

        # Set position
        self.settings_button.setGeometry(50, 50, 30, 30)

        self.setGeometry(100, 100, 300, 200)

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
