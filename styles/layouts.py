"""Layout configurations and utilities"""

class LayoutSizes:
    """Layout sizes for different screen configurations"""
    SMALL = {
        # POS view configs
        'pos_top_bar_height': 50,
        'pos_order_panel_width': 300,
        'pos_bottom_bar_height': 70,
        'pos_center_panel_width': 120,  # Your current fixed width
        'pos_intermediate_container_height': 350,  # Your current fixed height

        # search input
        'pos_search_input_width': 250,
        'pos_search_input_height': 35,

        # Payment button configurations
        'payment_button_width': 120,
        'payment_button_height': 45,
        'payment_button_font_size': 16,
        'payment_button_padding': 8,

        # Horizontal button configurations
        'horizontal_button_width': 90,
        'horizontal_button_height': 35,
        'horizontal_button_font_size': 13,
        'horizontal_button_padding': 4,

        # Transaction button configurations
        'transaction_button_width': 100,
        'transaction_button_height': 40,
        'transaction_button_font_size': 13,
        'transaction_button_padding': 5,
        
        # Order type button configurations
        'order_type_button_width': 100,
        'order_type_button_height': 36,
        'order_type_button_font_size': 13,
        'order_type_button_padding': 8,

        # Product Grid & catg buttons Related
        'pos_product_button_width': 120,
        'pos_product_button_height': 50,
        'pos_category_button_width': 100,
        'pos_category_button_height': 35,
        'pos_action_button_width': 120,
        'pos_action_button_height': 45,

        # Product button styling
        'product_button_font_size': 14,
        'product_button_padding': 5,
        'product_button_radius': 4,

        # Category button styling
        'category_button_font_size': 13,
        'category_button_padding': 5,
        'category_button_radius': 4,

        # Auth container sizes
        'auth_container_width': 350,
        'auth_container_height': 400,
        'auth_label_width': 250,
        'auth_label_height': 60,

        # Auth Label Related
        'label_font_size': 18,
        'auth_label_width': 250,
        'auth_label_height': 40,

        # digit box
        'digit_input_width': 40,
        'digit_input_height': 40,
        'digit_padding': 5,
        'digit_font_size': 14,

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

        # General button properties
        'button_border_radius': 4,
        'button_padding': 8,
        
        # Logo dimensions
        'logo_width': 200,
        'logo_height': 100,

        # Global spacing and margins
        'container_margin': 10,
        'section_spacing': 15,
        'label_padding': 0,
    }

    MEDIUM = {
        # POS view configs
        'pos_top_bar_height': 60,
        'pos_order_panel_width': 350,
        'pos_bottom_bar_height': 80,
        'pos_center_panel_width': 120,  # Your current fixed width
        'pos_intermediate_container_height': 350,  # Your current fixed height

        # search input
        'pos_search_input_width': 300,
        'pos_search_input_height': 40,

        # Payment button configurations
        'payment_button_width': 120,  # SMALL value example
        'payment_button_height': 45,
        'payment_button_font_size': 16,
        'payment_button_padding': 8,

        # Transaction button configurations
        'transaction_button_width': 100,
        'transaction_button_height': 40,
        'transaction_button_font_size': 13,
        'transaction_button_padding': 5,

        # Horizontal button configurations
        'horizontal_button_width': 90,
        'horizontal_button_height': 35,
        'horizontal_button_font_size': 13,
        'horizontal_button_padding': 4,

        # Order type button configurations
        'order_type_button_width': 100,
        'order_type_button_height': 36,
        'order_type_button_font_size': 13,
        'order_type_button_padding': 8,

        # Product Grid Related
        'pos_product_button_width': 140,
        'pos_product_button_height': 60,
        'pos_category_button_width': 120,
        'pos_category_button_height': 40,
        'pos_action_button_width': 140,
        'pos_action_button_height': 50,

        # Product button styling
        'product_button_font_size': 14,
        'product_button_padding': 5,
        'product_button_radius': 4,

        # Category button styling
        'category_button_font_size': 13,
        'category_button_padding': 5,
        'category_button_radius': 4,
                
        # Auth container sizes
        'auth_container_width': 450,
        'auth_container_height': 500,
        'auth_label_width': 300,
        'auth_label_height': 60,

        # Auth Label Related
        'label_font_size': 20,
        'auth_label_width': 300,
        'auth_label_height': 60,

        # digit box
        'digit_input_width': 45,
        'digit_input_height': 45,
        'digit_padding': 8,
        'digit_font_size': 16,

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

        # General button properties
        'button_border_radius': 6,
        'button_padding': 10,
        
        # Logo dimensions
        'logo_width': 300,
        'logo_height': 125,

        # Global spacing and margins
        'container_margin': 15,
        'section_spacing': 20,
        'label_padding': 10,
    }

    LARGE = {
        # POS view configs
        'pos_top_bar_height': 70,
        'pos_order_panel_width': 400,
        'pos_bottom_bar_height': 90,
        'pos_center_panel_width': 180,
        'pos_intermediate_container_height': 450,

        # search input
        'pos_search_input_width': 600,
        'pos_search_input_height': 30,

        # Payment button configurations
        'payment_button_width': 120,  # SMALL value example
        'payment_button_height': 45,
        'payment_button_font_size': 16,
        'payment_button_padding': 8,

        # Transaction button configurations
        'transaction_button_width': 100,
        'transaction_button_height': 40,
        'transaction_button_font_size': 13,
        'transaction_button_padding': 5,

        # Horizontal button configurations
        'horizontal_button_width': 90,
        'horizontal_button_height': 35,
        'horizontal_button_font_size': 13,
        'horizontal_button_padding': 4,

        # Order type button configurations
        'order_type_button_width': 100,
        'order_type_button_height': 50,
        'order_type_button_font_size': 13,
        'order_type_button_padding': 8,

        # Product Grid Related
        'pos_product_button_width': 160,
        'pos_product_button_height': 70,
        'pos_category_button_width': 140,
        'pos_category_button_height': 45,
        'pos_action_button_width': 160,
        'pos_action_button_height': 55,

        # Product button styling
        'product_button_font_size': 14,
        'product_button_padding': 5,
        'product_button_radius': 4,

        # Category button styling
        'category_button_font_size': 13,
        'category_button_padding': 5,
        'category_button_radius': 4,
        
        # Auth container sizes
        'auth_container_width': 500,
        'auth_container_height': 600,
        'auth_label_width': 400,
        'auth_label_height': 60,

        # Auth Label Related
        'label_font_size': 18,
        'auth_label_width': 400,
        'auth_label_height': 60,

        # digit box
        'digit_input_width': 60,
        'digit_input_height': 60,
        'digit_padding': 5,
        'digit_font_size': 16,

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

        # General button properties
        'button_border_radius': 8,
        'button_padding': 12,
        
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
            'bottom_bar_height': self.screen_config.get_size('pos_bottom_bar_height'),
            'center_panel_width': self.screen_config.get_size('pos_center_panel_width'),
            'intermediate_container_height': self.screen_config.get_size('pos_intermediate_container_height'),
            'search_input': {
                'width': self.screen_config.get_size('pos_search_input_width'),
                'height': self.screen_config.get_size('pos_search_input_height')
            }
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
    
    def get_digit_box_config(self):
        """Get digit box configurations"""
        return {
            'width': self.screen_config.get_size('digit_input_width'),
            'height': self.screen_config.get_size('digit_input_height'),
            'padding': self.screen_config.get_size('digit_padding'),
            'font_size': self.screen_config.get_size('digit_font_size')
        }
    
    def get_button_config(self, button_type):
        """Get button configurations based on type"""
        return {
            'payment': {
                'width': self.screen_config.get_size('payment_button_width'),
                'height': self.screen_config.get_size('payment_button_height'),
                'font_size': self.screen_config.get_size('payment_button_font_size'),
                'padding': self.screen_config.get_size('payment_button_padding'),
                'border_radius': self.screen_config.get_size('button_border_radius'), 
            },
            'transaction': {
                'width': self.screen_config.get_size('transaction_button_width'),
                'height': self.screen_config.get_size('transaction_button_height'),
                'font_size': self.screen_config.get_size('transaction_button_font_size'),
                'padding': self.screen_config.get_size('transaction_button_padding'),
                'border_radius': self.screen_config.get_size('button_border_radius'), 
            },
            'horizontal': {
                'width': self.screen_config.get_size('horizontal_button_width'),
                'height': self.screen_config.get_size('horizontal_button_height'),
                'font_size': self.screen_config.get_size('horizontal_button_font_size'),
                'padding': self.screen_config.get_size('horizontal_button_padding'),
                'border_radius': self.screen_config.get_size('button_border_radius'), 
            },
            'order_type': {
                'width': self.screen_config.get_size('order_type_button_width'),
                'height': self.screen_config.get_size('order_type_button_height'),
                'font_size': self.screen_config.get_size('order_type_button_font_size'),
                'padding': self.screen_config.get_size('order_type_button_padding'),
                'border_radius': self.screen_config.get_size('button_border_radius'), 
            }
            
        }[button_type]

    def get_product_grid_config(self):
        """Get product grid related button configurations"""
        return {
            'product_button': {
                'width': self.screen_config.get_size('pos_product_button_width'),
                'height': self.screen_config.get_size('pos_product_button_height'),
                'font_size': self.screen_config.get_size('product_button_font_size'),
                'padding': self.screen_config.get_size('product_button_padding'),
                'radius': self.screen_config.get_size('product_button_radius')
            },
            'category_button': {
                'width': self.screen_config.get_size('pos_category_button_width'),
                'height': self.screen_config.get_size('pos_category_button_height'),
                'font_size': self.screen_config.get_size('category_button_font_size'),
                'padding': self.screen_config.get_size('category_button_padding'),
                'radius': self.screen_config.get_size('category_button_radius')
            }
        }

# Function to initialize the layout config
def init_layout_config(screen_config):
    """Initialize the layout configuration with screen config"""
    if not LayoutConfig._instance:
        LayoutConfig(screen_config)
    return LayoutConfig._instance

# Create a global instance (will be initialized later)
layout_config = LayoutConfig()