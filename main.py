import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication

# Add the project root directory to Python path
sys.path.append(str(Path(__file__).parent))

from views.main_window import MainWindow

def main():
    # Create the application instance
    app = QApplication(sys.argv)
    
    # Create and show the main window
    window = MainWindow()
    window.showMaximized()
    
    # Start the event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()