import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow
from config.screen_config import screen_config

# Add the project root directory to Python path
sys.path.append(str(Path(__file__).parent))

from views.main_window import MainWindow

def main():
    # Create the application instance
    app = QApplication(sys.argv)
    
    # Initialize screen configuration
    screen_config.initialize()

    # Create and show the main window
    window = MainWindow()
    # window.showMaximized()
    window.showFullScreen()
    # Start the event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()