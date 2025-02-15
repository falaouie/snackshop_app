"""Layout configurations and utilities"""

class LayoutSizes:
    """Layout sizes for different screen configurations"""
    SMALL = {
        'pos_top_bar_height': 50,
        'pos_order_panel_width': 300,
        'pos_bottom_bar_height': 70,
    }

    MEDIUM = {
        'pos_top_bar_height': 60,
        'pos_order_panel_width': 350,
        'pos_bottom_bar_height': 80,
    }

    LARGE = {
        'pos_top_bar_height': 70,
        'pos_order_panel_width': 400,
        'pos_bottom_bar_height': 90,
    }

class LayoutConfig:
    """Layout configuration for different screen sections"""
    _instance = None
    
    def __init__(self, screen_config=None):
        if screen_config:
            self.screen_config = screen_config
            LayoutConfig._instance = self
    
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            raise RuntimeError("LayoutConfig not initialized. Call init_layout_config first.")
        return cls._instance
    
    def get_pos_layout(self):
        """Get POS view layout configuration"""
        return {
            'top_bar_height': self.screen_config.get_size('pos_top_bar_height'),
            'order_panel_width': self.screen_config.get_size('pos_order_panel_width'),
            'bottom_bar_height': self.screen_config.get_size('pos_bottom_bar_height')
        }
    
    def get_section_spacing(self):
        """Get spacing between major sections"""
        return self.screen_config.get_size('section_spacing')
    
    def get_container_margin(self):
        """Get standard container margins"""
        return self.screen_config.get_size('container_margin')

# Function to initialize the layout config
def init_layout_config(screen_config):
    """Initialize the layout configuration with screen config"""
    if not LayoutConfig._instance:
        LayoutConfig(screen_config)
    return LayoutConfig._instance

# Create a global instance (will be initialized later)
layout_config = LayoutConfig()