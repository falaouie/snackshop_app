"""
Layout configuration for the TopBar component.
Provides dimensions and styling specific to the TopBar UI.
"""
from config.screen_config import screen_config
from config.size_categories import SizeCategory

class TopBarLayoutConfig:
    """Layout configuration for top bar dimensions and styling"""
    _instance = None
    
    # Define size configurations for different screen sizes
    CONFIGS = {
        SizeCategory.SMALL: {
            # Main container
            'height': 50,
            'padding_left': 15,
            'padding_right': 15,
            'padding_top': 0,
            'padding_bottom': 0,
            'section_spacing': 10,
            
            # Employee section
            'employee_icon_size': 40,
            'employee_id_font_size': 13,
            'employee_section_spacing': 8,
            
            # DateTime section
            'datetime_container_padding': 10,
            'datetime_container_spacing': 2,
            'date_font_size': 12,
            'time_font_size': 14,
            
            # Lock button
            'lock_button_icon_size': 40,
            'lock_button_padding': 5,
            
            # Center section (for search or other components)
            'center_section_min_width': 200,
            'center_section_spacing': 10
        },
        
        SizeCategory.MEDIUM: {
            # Main container
            'height': 60,
            'padding_left': 20,
            'padding_right': 20,
            'padding_top': 0,
            'padding_bottom': 0,
            'section_spacing': 15,
            
            # Employee section
            'employee_icon_size': 45,
            'employee_id_font_size': 14,
            'employee_section_spacing': 10,
            
            # DateTime section
            'datetime_container_padding': 10,
            'datetime_container_spacing': 3,
            'date_font_size': 13,
            'time_font_size': 15,
            
            # Lock button
            'lock_button_icon_size': 50,
            'lock_button_padding': 8,
            
            # Center section (for search or other components)
            'center_section_min_width': 300,
            'center_section_spacing': 15
        },
        
        SizeCategory.LARGE: {
            # Main container
            'height': 70,
            'padding_left': 25,
            'padding_right': 25,
            'padding_top': 0,
            'padding_bottom': 0,
            'section_spacing': 20,
            
            # Employee section
            'employee_icon_size': 50,
            'employee_id_font_size': 16,
            'employee_section_spacing': 12,
            
            # DateTime section
            'datetime_container_padding': 15,
            'datetime_container_spacing': 4,
            'date_font_size': 14,
            'time_font_size': 26,
            
            # Lock button
            'lock_button_icon_size': 55,
            'lock_button_padding': 10,
            
            # Center section (for search or other components)
            'center_section_min_width': 400,
            'center_section_spacing': 20
        }
    }
    
    def __init__(self, screen_config_instance=None):
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
        
    def get_container_dimensions(self):
        """Get container dimensions and spacing"""
        config = self._get_current_config()
        return {
            'height': config['height'],
            'padding_left': config['padding_left'],
            'padding_right': config['padding_right'],
            'padding_top': config['padding_top'],
            'padding_bottom': config['padding_bottom'],
            'section_spacing': config['section_spacing']
        }
    
    def get_employee_section_config(self):
        """Get employee section configuration"""
        config = self._get_current_config()
        return {
            'icon_size': config['employee_icon_size'],
            'font_size': config['employee_id_font_size'],
            'spacing': config['employee_section_spacing']
        }
    
    def get_datetime_config(self):
        """Get datetime section configuration"""
        config = self._get_current_config()
        return {
            'container_padding': config['datetime_container_padding'],
            'container_spacing': config['datetime_container_spacing'],
            'date_font_size': config['date_font_size'],
            'time_font_size': config['time_font_size']
        }
    
    def get_lock_button_config(self):
        """Get lock button configuration"""
        config = self._get_current_config()
        return {
            'icon_size': config['lock_button_icon_size'],
            'padding': config['lock_button_padding']
        }
    
    def get_center_section_config(self):
        """Get center section configuration"""
        config = self._get_current_config()
        return {
            'min_width': config['center_section_min_width'],
            'spacing': config['center_section_spacing']
        }

# Create singleton instance
top_bar_layout_config = TopBarLayoutConfig()