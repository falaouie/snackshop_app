"""
Layout configuration for the AuthTopBar component.
Provides dimensions and styling specific to the Authentication TopBar UI.
"""
from config.screen_config import screen_config
from config.size_categories import SizeCategory

class AuthTopBarLayoutConfig:
    """Layout configuration for authentication top bar dimensions and styling"""
    _instance = None
    
    # Define size configurations for different screen sizes
    CONFIGS = {
        SizeCategory.SMALL: {
            # Main container
            'height': 100,
            'padding_left': 5,
            'padding_right': 5,
            'padding_top': 0,
            'padding_bottom': 0,
            # 'section_spacing': 10,  # Added section spacing
            
            # Exit button
            'exit_button_icon_size': 100,
            'exit_button_padding': 5,
            
            # Logo
            'logo_width': 200,
            'logo_height': 100
        },
        
        SizeCategory.MEDIUM: {
            # Main container
            'height': 150,
            'padding_left': 5,
            'padding_right': 5,
            'padding_top': 0,
            'padding_bottom': 0,
            # 'section_spacing': 15,  # Added section spacing
            
            # Exit button
            'exit_button_icon_size': 125,
            'exit_button_padding': 5,
            
            # Logo
            'logo_width': 300,
            'logo_height': 150
        },
        
        SizeCategory.LARGE: {
            # Main container
            'height': 200,
            'padding_left': 5,
            'padding_right': 5,
            'padding_top': 0,
            'padding_bottom': 0,
            # 'section_spacing': 20,  # Added section spacing
            
            # Exit button
            'exit_button_icon_size': 150,
            'exit_button_padding': 5,
            
            # Logo
            'logo_width': 400,
            'logo_height': 200
        }
    }
    
    def __init__(self, screen_config_instance=None):
        """Initialize with screen configuration"""
        self.screen_config = screen_config_instance or screen_config
    
    def _get_current_config(self):
        """Get the current configuration based on screen size category"""
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
        
    def get_auth_top_bar_container_dimensions(self):
        """Get container dimensions and spacing"""
        config = self._get_current_config()
        return {
            'height': config['height'],
            'padding_left': config['padding_left'],
            'padding_right': config['padding_right'],
            'padding_top': config['padding_top'],
            'padding_bottom': config['padding_bottom'],
            # 'section_spacing': config['section_spacing']  # Added section spacing
        }
    
    def get_exit_button_config(self):
        """Get exit button configuration"""
        config = self._get_current_config()
        return {
            'icon_size': config['exit_button_icon_size'],
            'padding': config['exit_button_padding']
        }
    
    def get_logo_size_config(self):
        """Get logo configuration"""
        config = self._get_current_config()
        return {
            'logo_width': config['logo_width'],
            'logo_height': config['logo_height']
        }

# Create singleton instance
auth_top_bar_layout_config = AuthTopBarLayoutConfig()