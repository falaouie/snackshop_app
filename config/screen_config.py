from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect
from styles.layouts import LayoutSizes


class ScreenConfig:
    """Handles screen detection and provides appropriate sizes for UI elements"""
    
    # Size configurations for different screen sizes
    SMALL = {
        # Logo dimensions
        'logo_width': 200,
        'logo_height': 100,

        # Auth container sizes
        'auth_container_width': 350,
        'auth_container_height': 400,

        # User id and password label
        'auth_label_width': 250,
        'auth_label_height': 60,
        
        # Input field sizes
        'digit_input_width': 40,
        'digit_input_height': 40,
        
        # General button properties
        'button_border_radius': 4,
        'button_padding': 8,
        
        # Basic button sizes
        'keypad_button_width': 60,
        'keypad_button_height': 40,
        'action_button_width': 60,
        'action_button_height': 40,
        'signin_button_width': 120,
        'signin_button_height': 40,

        # Payment button configurations
        'payment_button': {
            'width': 120,
            'height': 45,
            'font_size': 16,
            'padding': 8,
            'border_radius': 4
        },

        # Transaction button configurations
        'transaction_button': {
            'width': 100,
            'height': 40,
            'font_size': 13,
            'padding': 5,
            'border_radius': 4
        },

        # Horizontal button configurations
        'horizontal_button': {
            'width': 90,
            'height': 35,
            'font_size': 13,
            'padding': 4,
            'border_radius': 4
        },

        # Order type button configurations
        'order_type_button': {
            'width': 100,
            'height': 36,
            'font_size': 13,
            'padding': 8,
            'border_radius': 4,
            'min_width': 100
        },

        # Font sizes
        'keypad_font_size': 16,
        'label_font_size': 16,
        'digit_font_size': 14,

        # Padding
        'keypad_padding': 8,
        'label_padding': 8,
        'digit_padding': 5,
        
        # Spacing and margins
        'keypad_spacing': 10,
        'container_margin': 10,
        'section_spacing': 10,
        'button_spacing': 6,

        # POS view specific
        # 'pos_top_bar_height': 50,
        'pos_product_button_width': 120,
        'pos_product_button_height': 50,
        'pos_category_button_width': 100,
        'pos_category_button_height': 35,
        # 'pos_order_panel_width': 300,
        'pos_bottom_bar_height': 70,
        'pos_action_button_width': 120,
        'pos_action_button_height': 45,
        'pos_search_input_width': 250,
        'pos_search_input_height': 35
    }

    MEDIUM = {
        # Logo dimensions
        'logo_width': 300,
        'logo_height': 125,

        # Auth container sizes
        'auth_container_width': 400,
        'auth_container_height': 500,

        # User id and password label
        'auth_label_width': 300,
        'auth_label_height': 60,

        # Input field sizes
        'digit_input_width': 45,
        'digit_input_height': 45,

        # General button properties
        'button_border_radius': 6,
        'button_padding': 10,

        # Basic button sizes
        'keypad_button_width': 55,
        'keypad_button_height': 55,
        'action_button_width': 80,
        'action_button_height': 50,
        'signin_button_width': 160,
        'signin_button_height': 50,

        # Payment button configurations
        'payment_button': {
            'width': 140,
            'height': 50,
            'font_size': 18,
            'padding': 10,
            'border_radius': 6
        },

        # Transaction button configurations
        'transaction_button': {
            'width': 120,
            'height': 45,
            'font_size': 14,
            'padding': 6,
            'border_radius': 6
        },

        # Horizontal button configurations
        'horizontal_button': {
            'width': 110,
            'height': 40,
            'font_size': 14,
            'padding': 5,
            'border_radius': 6
        },

        # Order type button configurations
        'order_type_button': {
            'width': 120,
            'height': 40,
            'font_size': 14,
            'padding': 10,
            'border_radius': 6,
            'min_width': 120
        },

        # Font sizes
        'keypad_font_size': 20,
        'label_font_size': 18,
        'digit_font_size': 16,

        # Padding
        'keypad_padding': 10,
        'label_padding': 10,
        'digit_padding': 8,
        
        # Spacing and margins
        'keypad_spacing': 15,
        'container_margin': 15,
        'section_spacing': 15,
        'button_spacing': 8,

        # POS view specific
        # 'pos_top_bar_height': 60,
        'pos_product_button_width': 140,
        'pos_product_button_height': 60,
        'pos_category_button_width': 120,
        'pos_category_button_height': 40,
        # 'pos_order_panel_width': 350,
        'pos_bottom_bar_height': 80,
        'pos_action_button_width': 140,
        'pos_action_button_height': 50,
        'pos_search_input_width': 300,
        'pos_search_input_height': 40
    }

    LARGE = {
        # Logo dimensions
        'logo_width': 300,
        'logo_height': 150,

        # Auth container sizes
        'auth_container_width': 500,
        'auth_container_height': 600,

        # User id and password label
        'auth_label_width': 400,
        'auth_label_height': 60,

        # Input field sizes
        'digit_input_width': 60,
        'digit_input_height': 60,

        # General button properties
        'button_border_radius': 8,
        'button_padding': 12,

        # Basic button sizes
        'keypad_button_width': 100,
        'keypad_button_height': 60,
        'action_button_width': 150,
        'action_button_height': 60,
        'signin_button_width': 200,
        'signin_button_height': 60,

        # Payment button configurations
        'payment_button': {
            'width': 160,
            'height': 55,
            'font_size': 20,
            'padding': 12,
            'border_radius': 8
        },

        # Transaction button configurations
        'transaction_button': {
            'width': 140,
            'height': 50,
            'font_size': 16,
            'padding': 8,
            'border_radius': 8
        },

        # Horizontal button configurations
        'horizontal_button': {
            'width': 130,
            'height': 45,
            'font_size': 16,
            'padding': 6,
            'border_radius': 8
        },

        # Order type button configurations
        'order_type_button': {
            'width': 140,
            'height': 45,
            'font_size': 16,
            'padding': 12,
            'border_radius': 8,
            'min_width': 140
        },

        # Font sizes
        'keypad_font_size': 24,
        'label_font_size': 18,
        'digit_font_size': 16,

        # Padding
        'keypad_padding': 5,
        'label_padding': 5,
        'digit_padding': 5,

        # Spacing and margins
        'keypad_spacing': 10,
        'container_margin': 15,
        'section_spacing': 10,
        'button_spacing': 10,

        # POS view specific
        # 'pos_top_bar_height': 70,
        'pos_product_button_width': 160,
        'pos_product_button_height': 70,
        'pos_category_button_width': 140,
        'pos_category_button_height': 45,
        # 'pos_order_panel_width': 400,
        'pos_bottom_bar_height': 90,
        'pos_action_button_width': 160,
        'pos_action_button_height': 55,
        'pos_search_input_width': 600,
        'pos_search_input_height': 45
    }

    def __init__(self):
        self._current_config = None
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
                self._current_config = self.MEDIUM
                self._width = 1280  # Default medium width
                self._height = 768  # Default medium height
        else:
            print("Warning: QApplication not created, falling back to MEDIUM configuration")
            self._current_config = self.MEDIUM
            self._width = 1280  # Default medium width
            self._height = 768  # Default medium height
        
        self._initialized = True

    def _set_size_config(self):
        """Determine which size configuration to use based on screen resolution"""
        if self._width >= 1920 and self._height >= 1080:
            base_config = self.LARGE.copy()
            base_config.update(LayoutSizes.LARGE)
            self._current_config = base_config
            print("Using LARGE screen configuration")
        elif self._width >= 1280 and self._height >= 768:
            base_config = self.MEDIUM.copy()
            base_config.update(LayoutSizes.MEDIUM)
            self._current_config = base_config
            print("Using MEDIUM screen configuration")
        else:
            base_config = self.SMALL.copy()
            base_config.update(LayoutSizes.SMALL)
            self._current_config = base_config
            print("Using SMALL screen configuration")


    def get_size(self, element_name):
        """Get the size for a specific element based on current screen configuration"""
        self._ensure_initialized()
        
        # Handle nested configurations
        if '.' in element_name:
            category, property = element_name.split('.')
            return self._current_config.get(category, {}).get(property)
        
        return self._current_config.get(element_name)
    
    def get_screen_dimensions(self):
        """Get the screen dimensions"""
        self._ensure_initialized()
        return self._width, self._height

# Create a singleton instance
screen_config = ScreenConfig()