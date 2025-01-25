import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow

def main():
    # Initialize application
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainWindow()
    window.showMaximized()
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()