# config/layouts/search_layout.py
from config.screen_config import screen_config
from config.size_categories import SizeCategory

class SearchLayoutConfig:
    """Layout configuration for search input dimensions and styling"""
    _instance = None
    
    # Define size configurations for different screen sizes
    CONFIGS = {
        SizeCategory.SMALL: {
            'width': 250,
            'height': 35,
            'font_size': 13,
            'padding': 8,
            'border_radius': 4,
            'icon_size': 20,
            'icon_margin_left': 12
        },
        
        SizeCategory.MEDIUM: {
            'width': 300,
            'height': 30,
            'font_size': 14,
            'padding': 8,
            'border_radius': 4,
            'icon_size': 20,
            'icon_margin_left': 12
        },
        
        SizeCategory.LARGE: {
            'width': 600,
            'height': 40,
            'font_size': 18,
            'padding': 10,
            'border_radius': 15,
            'icon_size': 22,
            'icon_margin_left': 15
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
        """Get search input dimensions"""
        config = self._get_current_config()
        return {
            'width': config['width'],
            'height': config['height']
        }
    
    def get_styling(self):
        """Get styling parameters"""
        config = self._get_current_config()
        return {
            'font_size': config['font_size'],
            'padding': config['padding'],
            'border_radius': config['border_radius'],
            'icon_size': config['icon_size'],
            'icon_margin_left': config['icon_margin_left']
        }

# Create singleton instance
search_layout_config = SearchLayoutConfig()