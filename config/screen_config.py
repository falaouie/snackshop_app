from PyQt5.QtWidgets import QApplication
from config.size_categories import SizeCategory

class ScreenConfig:
    """Handles screen detection and provides appropriate sizes for UI elements"""

    def __init__(self):
        self._current_config = None
        self._size_category = None
        self._width = None
        self._height = None
        self._initialized = False

    def _ensure_initialized(self):
        """Ensure configuration is initialized before use"""
        if not self._initialized:
            self._initialize()
        
    def _initialize(self):
        """Initialize screen configuration after QApplication is created"""
        if QApplication.instance():
            screen = QApplication.primaryScreen()
            if screen:
                geometry = screen.geometry()
                self._width = geometry.width()
                self._height = geometry.height()
                print(f"Screen dimensions - Width: {self._width}, Height: {self._height}")
                self._set_size_config()
            else:
                print("Warning: No screen detected, falling back to MEDIUM configuration")
                # Import here to avoid circular import
                from styles.layouts import LayoutSizes
                self._current_config = LayoutSizes.MEDIUM
                self._size_category = SizeCategory.MEDIUM
                self._width = 1280  # Default medium width
                self._height = 768  # Default medium height
        else:
            print("Warning: QApplication not created, falling back to MEDIUM configuration")
            # Import here to avoid circular import
            from styles.layouts import LayoutSizes
            self._current_config = LayoutSizes.MEDIUM
            self._size_category = SizeCategory.MEDIUM
            self._width = 1280  # Default medium width
            self._height = 768  # Default medium height
        
        self._initialized = True

    def _set_size_config(self):
        """Determine which size configuration to use based on screen resolution"""
        # Import here to avoid circular import
        from styles.layouts import LayoutSizes
        
        if self._width >= 1920 and self._height >= 1080:
            self._current_config = LayoutSizes.LARGE
            self._size_category = SizeCategory.LARGE
            print("Using LARGE screen configuration")
        elif self._width >= 1024 and self._height >= 768:
            self._current_config = LayoutSizes.MEDIUM
            self._size_category = SizeCategory.MEDIUM
            print("Using MEDIUM screen configuration")
        else:
            self._current_config = LayoutSizes.SMALL
            self._size_category = SizeCategory.SMALL
            print("Using SMALL screen configuration")

    def get_size_category(self):
        """Get the current size category (SMALL, MEDIUM, LARGE)"""
        self._ensure_initialized()
        return self._size_category

    def get_size(self, element_name):
        """Get the size for a specific element based on current screen configuration"""
        self._ensure_initialized()
        return self._current_config.get(element_name)
    
    def get_screen_dimensions(self):
        """Get the screen dimensions"""
        self._ensure_initialized()
        return self._width, self._height

# Create a singleton instance
screen_config = ScreenConfig()