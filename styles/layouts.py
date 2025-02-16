"""Layout configurations and utilities"""

class LayoutSizes:
    """Layout sizes for different screen configurations"""
    SMALL = {
        # Existing POS configs
        'pos_top_bar_height': 50,
        'pos_order_panel_width': 300,
        'pos_bottom_bar_height': 70,
        
        # Auth container sizes
        'auth_container_width': 350,
        'auth_container_height': 400,
        'auth_label_width': 250,
        'auth_label_height': 60,

        # Auth Label Related
        'label_font_size': 18,
        'auth_label_width': 250,
        'auth_label_height': 40,

        # Keypad Basic
        'keypad_spacing': 10,
        'keypad_button_width': 60,
        'keypad_button_height': 40,
        'keypad_font_size': 16,
        'keypad_padding': 8,

        # Action Buttons
        'action_button_width': 60,
        'action_button_height': 40,
        'signin_button_width': 120,
        'signin_button_height': 40,
        
        # Logo dimensions
        'logo_width': 200,
        'logo_height': 100,

        # Global spacing and margins
        'container_margin': 10,
        'section_spacing': 15,
        'label_padding': 0,
    }

    MEDIUM = {
        # Existing POS configs
        'pos_top_bar_height': 60,
        'pos_order_panel_width': 350,
        'pos_bottom_bar_height': 80,
        
        # Auth container sizes
        'auth_container_width': 450,
        'auth_container_height': 500,
        'auth_label_width': 300,
        'auth_label_height': 60,

        # Auth Label Related
        'label_font_size': 20,
        'auth_label_width': 300,
        'auth_label_height': 60,

        # Keypad Basic
        'keypad_spacing': 15,
        'keypad_button_width': 55,
        'keypad_button_height': 55,
        'keypad_font_size': 20,
        'keypad_padding': 10,

        # Action Buttons
        'action_button_width': 80,
        'action_button_height': 50,
        'signin_button_width': 160,
        'signin_button_height': 50,
        
        # Logo dimensions
        'logo_width': 300,
        'logo_height': 125,

        # Global spacing and margins
        'container_margin': 15,
        'section_spacing': 20,
        'label_padding': 10,
    }

    LARGE = {
        # Existing POS configs
        'pos_top_bar_height': 70,
        'pos_order_panel_width': 400,
        'pos_bottom_bar_height': 90,
        
        # Auth container sizes
        'auth_container_width': 500,
        'auth_container_height': 600,
        'auth_label_width': 400,
        'auth_label_height': 60,

        # Auth Label Related
        'label_font_size': 18,
        'auth_label_width': 400,
        'auth_label_height': 60,

        # Keypad Basic
        'keypad_spacing': 10,
        'keypad_button_width': 100,
        'keypad_button_height': 60,
        'keypad_font_size': 24,
        'keypad_padding': 5,

        # Action Buttons
        'action_button_width': 150,
        'action_button_height': 60,
        'signin_button_width': 200,
        'signin_button_height': 60,
        
        # Logo dimensions
        'logo_width': 300,
        'logo_height': 150,

        # Global spacing and margins
        'container_margin': 15,
        'section_spacing': 10,
        'label_padding': 5,
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
    
    def get_auth_layout(self):
        """Get authentication view layout configuration"""
        return {
            'container_width': self.screen_config.get_size('auth_container_width'),
            'container_height': self.screen_config.get_size('auth_container_height'),
            'label_width': self.screen_config.get_size('auth_label_width'),
            'label_height': self.screen_config.get_size('auth_label_height'),
            'logo_width': self.screen_config.get_size('logo_width'),
            'logo_height': self.screen_config.get_size('logo_height')
        }

    def get_spacing_config(self):
        """Get global spacing and margin configurations"""
        return {
            'container_margin': self.screen_config.get_size('container_margin'),
            'section_spacing': self.screen_config.get_size('section_spacing'),
            'label_padding': self.screen_config.get_size('label_padding')
        }
    
    def get_label_config(self):
        """Get authentication label configurations"""
        return {
            'font_size': self.screen_config.get_size('label_font_size'),
            'width': self.screen_config.get_size('auth_label_width'),
            'height': self.screen_config.get_size('auth_label_height')
        }
    
    def get_keypad_config(self):
        """Get keypad basic configurations"""
        return {
            'spacing': self.screen_config.get_size('keypad_spacing'),
            'button_width': self.screen_config.get_size('keypad_button_width'),
            'button_height': self.screen_config.get_size('keypad_button_height'),
            'font_size': self.screen_config.get_size('keypad_font_size'),
            'padding': self.screen_config.get_size('keypad_padding')
        }
    
    # def get_section_spacing(self):
    #     """Get spacing between major sections"""
    #     return self.screen_config.get_size('section_spacing')
    
    def get_action_buttons_config(self):
        """Get action and signin button configurations"""
        return {
            'action_width': self.screen_config.get_size('action_button_width'),
            'action_height': self.screen_config.get_size('action_button_height'),
            'signin_width': self.screen_config.get_size('signin_button_width'),
            'signin_height': self.screen_config.get_size('signin_button_height')
        }
    
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