"""
Layout configuration for the AuthTopBar component.
Provides dimensions and styling specific to the Authentication TopBar UI.
"""
from config.screen_config import screen_config
from config.size_categories import SizeCategory

class AuthLayoutConfig:
    """Layout configuration for authentication top bar dimensions and styling"""
    _instance = None
    
    # Define size configurations for different screen sizes
    CONFIGS = {
        SizeCategory.SMALL: {
            # Auth Top Bar container
            'auth_top_bar_height': 100,
            'auth_top_bar_padding_left': 5,
            'auth_top_bar_padding_right': 5,
            'auth_top_bar_padding_top': 0,
            'auth_top_bar_padding_bottom': 0,
            
            # Exit button
            'exit_button_icon_size': 100,
            'exit_button_padding': 5,
            
            # Logo
            'logo_width': 200,
            'logo_height': 100,

            # Auth container
            'auth_container_width': 350,
            'auth_container_height': 400,
            'auth_container_margin': 5,
            
            # Specific spacing controls
            'label_top_margin': 20,             # label's top margin
            'label_to_input_spacing': 5,        # Space between label and input field
            'input_to_keypad_spacing': 10,      # Space between input field and keypad
            'keypad_buttons_spacing': 5,        # Space between keypad buttons
            'keypad_to_action_spacing': 10,     # Space between keypad and action buttons
            
            # Auth label
            'auth_label_width': 300,
            'auth_label_height': 50,
            'auth_label_padding': 5,
            'auth_font_size': 18,

            # Keypad
            'keypad_button_width': 100,
            'keypad_button_height': 60,
            'keypad_font_size': 24,
            'keypad_padding': 5,

            # Action Buttons
            'action_button_width': 150,
            'action_button_height': 60,
            'signin_button_width': 200,
            'signin_button_height': 60,
            'action_buttons_spacing': 5,        # Space between action buttons
        },
        
        SizeCategory.MEDIUM: {
            # Auth Top Bar container
            'auth_top_bar_height': 150,
            'auth_top_bar_padding_left': 5,
            'auth_top_bar_padding_right': 5,
            'auth_top_bar_padding_top': 0,
            'auth_top_bar_padding_bottom': 0,
            
            # Exit button
            'exit_button_icon_size': 125,
            'exit_button_padding': 5,
            
            # Logo
            'logo_width': 300,
            'logo_height': 150,

            # Auth container
            'auth_container_width': 350,
            'auth_container_height': 400,
            'auth_container_margin': 5,
            
            # Specific spacing controls
            'label_top_margin': 20,          # New parameter for label's top margin
            'label_to_input_spacing': 5,
            'input_to_keypad_spacing': 10,
            'keypad_buttons_spacing': 5,
            'keypad_to_action_spacing': 10,
            
            # Auth label
            'auth_label_width': 300,
            'auth_label_height': 60,
            'auth_label_padding': 5,
            'auth_font_size': 16,

            # Keypad
            'keypad_button_width': 100,
            'keypad_button_height': 60,
            'keypad_font_size': 24,
            'keypad_padding': 5,

            # Action Buttons
            'action_button_width': 150,
            'action_button_height': 60,
            'signin_button_width': 200,
            'signin_button_height': 60,
            'action_buttons_spacing': 5,
        },
        
        SizeCategory.LARGE: {
            # Auth Top Bar container
            'auth_top_bar_height': 200,
            'auth_top_bar_padding_left': 5,
            'auth_top_bar_padding_right': 5,
            'auth_top_bar_padding_top': 0,
            'auth_top_bar_padding_bottom': 0,
            
            # Exit button
            'exit_button_icon_size': 150,
            'exit_button_padding': 5,
            
            # Logo
            'logo_width': 400,
            'logo_height': 200,

            # Auth container
            'auth_container_width': 500,
            'auth_container_height': 600,
            'auth_container_margin': 5,
            
            # Specific spacing controls
            'label_top_margin': 20,             # label's top margin
            'label_to_input_spacing': 25,
            'input_to_keypad_spacing': 25,
            'keypad_buttons_spacing': 25,
            'keypad_to_action_spacing': 25,
            
            # Auth label
            'auth_label_width': 300,
            'auth_label_height': 40,  # Reduced height
            'auth_label_padding': 5,
            'auth_font_size': 24,

            # Keypad
            'keypad_button_width': 100,
            'keypad_button_height': 60,
            'keypad_font_size': 24,
            'keypad_padding': 5,

            # Action Buttons
            'action_button_width': 150,
            'action_button_height': 60,
            'signin_button_width': 200,
            'signin_button_height': 60,
            'action_buttons_spacing': 8,
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
            'height': config['auth_top_bar_height'],
            'padding_left': config['auth_top_bar_padding_left'],
            'padding_right': config['auth_top_bar_padding_right'],
            'padding_top': config['auth_top_bar_padding_top'],
            'padding_bottom': config['auth_top_bar_padding_bottom'],
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
    
    def get_auth_layout(self):
        """Get authentication view layout configuration"""
        config = self._get_current_config()
        return {
            'container_width': config['auth_container_width'],
            'container_height': config['auth_container_height'],
            'label_width': config['auth_label_width'],
            'label_height': config['auth_label_height'],
            'logo_width': config['logo_width'],
            'logo_height': config['logo_height'],
            'container_margin': config['auth_container_margin'],
            'label_top_margin': config['label_top_margin'],
            'label_to_input_spacing': config['label_to_input_spacing'],
            'input_to_keypad_spacing': config['input_to_keypad_spacing'],
            'keypad_to_action_spacing': config['keypad_to_action_spacing'],
            'label_padding': config['auth_label_padding'],
            'font_size': config['auth_font_size']
        }
    
    def get_keypad_config(self):
        """Get keypad basic configurations"""
        config = self._get_current_config()
        return {
            'button_width': config['keypad_button_width'],
            'button_height': config['keypad_button_height'],
            'font_size': config['keypad_font_size'],
            'padding': config['keypad_padding'],
            'buttons_spacing': config['keypad_buttons_spacing']
        }
    
    def get_action_buttons_config(self):
        """Get action and signin button configurations"""
        config = self._get_current_config()
        return {
            'action_width': config['action_button_width'],
            'action_height': config['action_button_height'],
            'signin_width': config['signin_button_width'],
            'signin_height': config['signin_button_height'],
            'buttons_spacing': config['action_buttons_spacing']
        }