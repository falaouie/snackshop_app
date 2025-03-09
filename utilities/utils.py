from PyQt5.QtWidgets import QApplication

class ApplicationUtils:
    @staticmethod
    def close_application():
        """Closes the application."""
        print("Closing Application ....")
        QApplication.quit()