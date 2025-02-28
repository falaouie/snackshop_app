"""
Layout configuration for the Virtual Keyboard component.
Provides dimensions and styling specific to the Keyboard UI.
"""
from config.screen_config import screen_config
from config.size_categories import SizeCategory

class KeyboardLayoutConfig:
    """Layout configuration for virtual keyboard dimensions and styling"""
    _instance = None
    
    # Define size configurations for different screen sizes
    CONFIGS = {
        SizeCategory.SMALL: {
            'key_width': 45,
            'key_height': 45,
            'space_width': 250,
            'space_height': 40,
            'enter_width': 120,
            'enter_height': 40,
            'handle_height': 35,
            'control_button_size': 35,
            'font_size': 16,
            'padding': 6,
            'spacing': 4,
            'main_margin_left': 10,
            'main_margin_top': 5,
            'main_margin_right': 10,
            'main_margin_bottom': 10,
            'main_spacing': 5,
            'handle_margin_left': 5,
            'handle_margin_top': 0,
            'handle_margin_right': 5,
            'handle_margin_bottom': 0,
            'handle_spacing': 8
        },
        
        SizeCategory.MEDIUM: {
            'key_width': 50,
            'key_height': 50,
            'space_width': 320,
            'space_height': 45,
            'enter_width': 150,
            'enter_height': 45,
            'handle_height': 40,
            'control_button_size': 40,
            'font_size': 18,
            'padding': 8,
            'spacing': 5,
            'main_margin_left': 10,
            'main_margin_top': 5,
            'main_margin_right': 10,
            'main_margin_bottom': 10,
            'main_spacing': 5,
            'handle_margin_left': 5,
            'handle_margin_top': 0,
            'handle_margin_right': 5,
            'handle_margin_bottom': 0,
            'handle_spacing': 8
        },
        
        SizeCategory.LARGE: {
            'key_width': 60,
            'key_height': 60,
            'space_width': 600,
            'space_height': 55,
            'enter_width': 180,
            'enter_height': 55,
            'handle_height': 45,
            'control_button_size': 45,
            'font_size': 22,
            'padding': 10,
            'spacing': 8,
            'main_margin_left': 10,
            'main_margin_top': 5,
            'main_margin_right': 10,
            'main_margin_bottom': 10,
            'main_spacing': 5,
            'handle_margin_left': 5,
            'handle_margin_top': 0,
            'handle_margin_right': 5,
            'handle_margin_bottom': 0,
            'handle_spacing': 8
        }
    }
    
    def __init__(self, screen_config_instance=None):
        self.screen_config = screen_config_instance or screen_config
    
    def _get_current_config(self):
        """Get the current configuration based on screen size category"""
        # Always get fresh size category from screen_config
        size_category = self.screen_config.get_size_category()
        return self.CONFIGS[size_category]
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of the config"""
        if not cls._instance:
            cls._instance = cls(screen_config)
        return cls._instance
    
    def get_size(self, key):
        """Get a specific size value"""
        return self._get_current_config().get(key)
        
    def get_dimensions(self):
        """Get keyboard button and key dimensions"""
        config = self._get_current_config()
        return {
            'key_width': config['key_width'],
            'key_height': config['key_height'],
            'space_width': config['space_width'],
            'space_height': config['space_height'],
            'enter_width': config['enter_width'],
            'enter_height': config['enter_height'],
            'handle_height': config['handle_height'],
            'control_button_size': config['control_button_size']
        }
    
    def get_layout(self):
        """Get layout configuration with margins and spacing"""
        config = self._get_current_config()
        return {
            'main_margins': [
                config['main_margin_left'],
                config['main_margin_top'],
                config['main_margin_right'],
                config['main_margin_bottom']
            ],
            'main_spacing': config['main_spacing'],
            'handle_margins': [
                config['handle_margin_left'],
                config['handle_margin_top'],
                config['handle_margin_right'],
                config['handle_margin_bottom']
            ],
            'handle_spacing': config['handle_spacing'],
            'spacing': config['spacing']
        }
    
    def get_styling(self):
        """Get styling parameters"""
        config = self._get_current_config()
        return {
            'font_size': config['font_size'],
            'padding': config['padding']
        }

# Create singleton instance
keyboard_layout_config = KeyboardLayoutConfig()