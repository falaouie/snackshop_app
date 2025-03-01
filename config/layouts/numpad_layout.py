"""
Layout configuration for the Numpad component.
Provides dimensions and spacing specific to the Numpad UI.
"""
from config.screen_config import screen_config
from config.size_categories import SizeCategory

class NumpadLayoutConfig:
    """Layout configuration for numpad dimensions and layout"""
    _instance = None
    
    # Define size configurations for different screen sizes
    CONFIGS = {
        SizeCategory.SMALL: {
            'button_size': 60,
            'display_height': 45,
            'spacing': 6,
            'font_size': 18,
            'width': 300,
            'main_margin_left': 10,
            'main_margin_top': 10,
            'main_margin_right': 10,
            'main_margin_bottom': 10,
            'grid_margin_left': 5,
            'grid_margin_top': 5,
            'grid_margin_right': 5,
            'grid_margin_bottom': 5,
        },
        
        SizeCategory.MEDIUM: {
            'button_size': 45,
            'display_height': 45,
            'spacing': 5,
            'font_size': 18,
            'width': 250,
            'main_margin_left': 10,
            'main_margin_top': 10,
            'main_margin_right': 10,
            'main_margin_bottom': 10,
            'grid_margin_left': 5,
            'grid_margin_top': 5,
            'grid_margin_right': 5,
            'grid_margin_bottom': 5,
        },
        
        SizeCategory.LARGE: {
            'button_size': 60,
            'display_height': 50,
            'spacing': 8,
            'font_size': 36,
            'width': 300,
            'main_margin_left': 10,
            'main_margin_top': 10,
            'main_margin_right': 10,
            'main_margin_bottom': 10,
            'grid_margin_left': 5,
            'grid_margin_top': 5,
            'grid_margin_right': 5,
            'grid_margin_bottom': 5,
        }
    }
    
    def __init__(self, screen_config_instance=None):
        self.screen_config = screen_config_instance or screen_config
        self.current_config = None
    
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
        """Get button dimensions from configuration"""
        config = self._get_current_config()
        return {
            'button_size': config['button_size'],
            'display_height': config['display_height'],
            'width': config['width']
        }
    
    def get_layout(self):
        """Get layout configuration with detailed margin control"""
        config = self._get_current_config()
        return {
            'main_margins': [
                config['main_margin_left'],
                config['main_margin_top'],
                config['main_margin_right'],
                config['main_margin_bottom']
            ],
            'grid_margins': [
                config['grid_margin_left'],
                config['grid_margin_top'],
                config['grid_margin_right'],
                config['grid_margin_bottom']
            ],
            'grid_spacing': config['spacing']
        }

# Create singleton instance
numpad_layout_config = NumpadLayoutConfig()