import sys
from PyQt5.QtWidgets import QApplication
from config.screen_config import screen_config
import styles

def main():
    # Create the application instance
    app = QApplication(sys.argv)

    # Trigger screen configuration early
    screen_config.get_screen_dimensions()
    
    # Initialize styles and layouts
    styles.init_styles(screen_config)
    
    # Import MainWindow after QApplication exists
    from views.main_window import MainWindow
    
    window = MainWindow()
    window.showFullScreen()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()