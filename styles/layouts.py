"""Layout configurations and utilities"""

class LayoutSizes:
    """Layout sizes for different screen configurations"""
    SMALL = {
        # POS view configs
        'pos_top_bar_height': 50,
        'pos_order_panel_width': 300,
        'pos_bottom_bar_height': 70,
        'pos_center_panel_width': 100,
        'pos_order_type_container_height': 50,
        'pos_category_container_height': 50,
        'pos_intermediate_container_height': 300,
        'pos_splitter_handle_width': 1,
        'pos_order_type_button_spacing': 6,
        'pos_category_button_spacing': 6,

        # search input
        'pos_search_input_width': 250,
        'pos_search_input_height': 35,

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

        # transaction button related configs
        'transaction_container_margin_left': 10,
        'transaction_container_margin_top': 10,
        'transaction_container_margin_right': 10,
        'transaction_container_margin_bottom': 10,
        'transaction_buttons_spacing': 8,
        'transaction_button_radius': 6,
        
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

        # product grid configs
        'product_grid_main_margin_left': 0,
        'product_grid_main_margin_top': 5,
        'product_grid_main_margin_right': 0,
        'product_grid_main_margin_bottom': 0,
        'product_grid_main_spacing': 8,
        'product_grid_category_margin_left': 5,
        'product_grid_category_margin_top': 0,
        'product_grid_category_margin_right': 5,
        'product_grid_category_margin_bottom': 0,
        'product_grid_category_spacing': 8,
        'product_grid_items_margin_left': 5,
        'product_grid_items_margin_top': 5,
        'product_grid_items_margin_right': 5,
        'product_grid_items_margin_bottom': 5,
        'product_grid_items_spacing': 10,

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

         # Keyboard specific settings
        'keyboard_key_width': 45,
        'keyboard_key_height': 45,
        'keyboard_space_width': 250,
        'keyboard_space_height': 40,
        'keyboard_enter_width': 120,
        'keyboard_enter_height': 40,
        'keyboard_handle_height': 35,
        'keyboard_control_button_size': 35,
        'keyboard_font_size': 16,
        'keyboard_padding': 6,
        'keyboard_spacing': 4,

        # keyboard related configs
        'keyboard_main_margin_left': 10,
        'keyboard_main_margin_top': 5,
        'keyboard_main_margin_right': 10,
        'keyboard_main_margin_bottom': 10,
        'keyboard_handle_margin_left': 5,
        'keyboard_handle_margin_top': 0,
        'keyboard_handle_margin_right': 5,
        'keyboard_handle_margin_bottom': 0,
        'keyboard_handle_spacing': 8,

        # Numpad specific settings
        'numpad_button_size': 60,
        'numpad_display_height': 45,
        'numpad_spacing': 6,
        'numpad_font_size': 18,
        'numpad_width': 300,
        'numpad_main_margin_left': 10,
        'numpad_main_margin_top': 10,
        'numpad_main_margin_right': 10,
        'numpad_main_margin_bottom': 10,
        'numpad_grid_margin_left': 5,
        'numpad_grid_margin_top': 5,
        'numpad_grid_margin_right': 5,
        'numpad_grid_margin_bottom': 5,

        # Preset button configurations
        'preset_button_width': 140,
        'preset_button_height': 35,
        'preset_widget_width': 150,
        'preset_button_margin_left': 5,
        'preset_button_margin_top': 5,
        'preset_button_margin_right': 5,
        'preset_button_margin_bottom': 5,
        'preset_button_font_size': 14,
        'preset_button_padding': 5,
        'preset_button_radius': 4,
        'preset_button_spacing': 5,

        # Payment action button configurations
        'payment_action_button_width': 140,
        'payment_action_button_height': 40,
        'payment_action_button_font_size': 15,
        'payment_action_button_padding': 8,
        'payment_action_button_radius': 5,

        # Totals widget configurations
        'totals_label_font_size': 16,
        'totals_amount_font_size': 20,
        'totals_header_font_size': 16,
        'totals_widget_padding': 10,
        'totals_section_spacing': 15,

        # order list widget configs
        'order_header_margin_left': 10,
        'order_header_margin_top': 5,
        'order_header_margin_right': 0,
        'order_header_margin_bottom': 5,
        'order_item_margin_left': 5,
        'order_item_margin_top': 2,
        'order_item_margin_right': 5,
        'order_item_margin_bottom': 2,
        'order_quantity_label_width': 30,
        'order_total_label_width': 60,
        'order_summary_margin_left': 15,
        'order_summary_margin_top': 8,
        'order_summary_margin_right': 15,
        'order_summary_margin_bottom': 8,     
    }

    MEDIUM = {
        # POS view configs
        'pos_top_bar_height': 50,
        'pos_order_panel_width': 350,
        'pos_bottom_bar_height': 50,
        'pos_center_panel_width': 120,
        'pos_order_type_container_height': 50,
        'pos_category_container_height': 50,
        'pos_intermediate_container_height': 400,
        'pos_splitter_handle_width': 1,
        'pos_order_type_button_spacing': 5,
        'pos_category_button_spacing': 5,

        # search input
        'pos_search_input_width': 300,
        'pos_search_input_height': 30,

        # Transaction button configurations
        'transaction_button_width': 80,
        'transaction_button_height': 35,
        'transaction_button_font_size': 12,
        'transaction_button_padding': 2,
        'transaction_button_radius': 15,

        # transaction button related configs
        'transaction_container_margin_left': 5,
        'transaction_container_margin_top': 5,
        'transaction_container_margin_right': 5,
        'transaction_container_margin_bottom': 5,
        'transaction_buttons_spacing': 5,

        # Horizontal button configurations
        # 'horizontal_button_width': 90,
        # 'horizontal_button_height': 35,
        # 'horizontal_button_font_size': 13,
        # 'horizontal_button_padding': 4,

        # Order type button configurations
        'order_type_button_width': 80,
        'order_type_button_height': 35,
        'order_type_button_font_size': 12,
        'order_type_button_padding': 5,

        # Product Grid Related
        'pos_product_button_width': 120,
        'pos_product_button_height': 60,
        'pos_category_button_width': 120,
        'pos_category_button_height': 40,
        # 'pos_action_button_width': 120,
        # 'pos_action_button_height': 50,

        # Product button styling
        'product_button_font_size': 14,
        'product_button_padding': 5,
        'product_button_radius': 15,

        # product grid configs
        'product_grid_main_margin_left': 0,
        'product_grid_main_margin_top': 5,
        'product_grid_main_margin_right': 0,
        'product_grid_main_margin_bottom': 0,
        'product_grid_main_spacing': 5,
        'product_grid_category_margin_left': 5,
        'product_grid_category_margin_top': 0,
        'product_grid_category_margin_right': 5,
        'product_grid_category_margin_bottom': 0,
        'product_grid_category_spacing': 8,
        'product_grid_items_margin_left': 5,
        'product_grid_items_margin_top': 5,
        'product_grid_items_margin_right': 5,
        'product_grid_items_margin_bottom': 5,
        'product_grid_items_spacing': 5,

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

        # Keyboard specific settings
        'keyboard_key_width': 50,
        'keyboard_key_height': 50,
        'keyboard_space_width': 320,
        'keyboard_space_height': 45,
        'keyboard_enter_width': 150,
        'keyboard_enter_height': 45,
        'keyboard_handle_height': 40,
        'keyboard_control_button_size': 40,
        'keyboard_font_size': 18,
        'keyboard_padding': 8,
        'keyboard_spacing': 5,

        # keyboard related configs
        'keyboard_main_margin_left': 10,
        'keyboard_main_margin_top': 5,
        'keyboard_main_margin_right': 10,
        'keyboard_main_margin_bottom': 10,
        'keyboard_handle_margin_left': 5,
        'keyboard_handle_margin_top': 0,
        'keyboard_handle_margin_right': 5,
        'keyboard_handle_margin_bottom': 0,
        'keyboard_handle_spacing': 8,

        # Numpad specific settings
        'numpad_button_size': 45,
        'numpad_display_height': 45,
        'numpad_spacing': 5,
        'numpad_font_size': 16,
        'numpad_width': 200,
        'numpad_main_margin_left': 10,
        'numpad_main_margin_top': 10,
        'numpad_main_margin_right': 10,
        'numpad_main_margin_bottom': 10,
        'numpad_grid_margin_left': 5,
        'numpad_grid_margin_top': 5,
        'numpad_grid_margin_right': 5,
        'numpad_grid_margin_bottom': 5,

        # Preset button configurations
        'preset_button_width': 90,
        'preset_button_height': 35,
        'preset_widget_width': 100,
        'preset_button_margin_left': 5,
        'preset_button_margin_top': 5,
        'preset_button_margin_right': 5,
        'preset_button_margin_bottom': 5,
        'preset_button_font_size': 14,
        'preset_button_padding': 5,
        'preset_button_radius': 4,
        'preset_button_spacing': 5,

        # Payment action button configurations
        'payment_action_button_width': 140,
        'payment_action_button_height': 40,
        'payment_action_button_font_size': 15,
        'payment_action_button_padding': 8,
        'payment_action_button_radius': 5,

        # Totals widget configurations
        'totals_label_font_size': 16,
        'totals_amount_font_size': 20,
        'totals_header_font_size': 16,
        'totals_widget_padding': 10,
        'totals_section_spacing': 15,

        # order list widget configs
        'order_header_margin_left': 5,
        'order_header_margin_top': 5,
        'order_header_margin_right': 5,
        'order_header_margin_bottom': 5,
        'order_item_margin_left': 2,
        'order_item_margin_top': 2,
        'order_item_margin_right': 2,
        'order_item_margin_bottom': 2,
        'order_quantity_label_width': 30,
        'order_total_label_width': 60,
        'order_summary_margin_left': 15,
        'order_summary_margin_top': 8,
        'order_summary_margin_right': 15,
        'order_summary_margin_bottom': 8, 
    }

    LARGE = {
        # POS view configs
        'pos_top_bar_height': 70,
        'pos_order_panel_width': 400,
        'pos_bottom_bar_height': 90,
        'pos_center_panel_width': 140,
        'pos_order_type_container_height': 70,
        'pos_category_container_height': 70,
        'pos_intermediate_container_height': 400,
        'pos_splitter_handle_width': 1,
        'pos_order_type_button_spacing': 10,
        'pos_category_button_spacing': 10,

        # search input
        'pos_search_input_width': 600,
        'pos_search_input_height': 30,

        # Transaction button configurations
        'transaction_button_width': 100,
        'transaction_button_height': 70,
        'transaction_button_font_size': 18,
        'transaction_button_padding': 5,
        'transaction_button_radius': 25,

        # transaction button related configs
        'transaction_container_margin_left': 10,
        'transaction_container_margin_top': 10,
        'transaction_container_margin_right': 10,
        'transaction_container_margin_bottom': 10,
        'transaction_buttons_spacing': 28,

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

        # product grid configs
        'product_grid_main_margin_left': 0,
        'product_grid_main_margin_top': 5,
        'product_grid_main_margin_right': 0,
        'product_grid_main_margin_bottom': 0,
        'product_grid_main_spacing': 8,
        'product_grid_category_margin_left': 5,
        'product_grid_category_margin_top': 0,
        'product_grid_category_margin_right': 5,
        'product_grid_category_margin_bottom': 0,
        'product_grid_category_spacing': 8,
        'product_grid_items_margin_left': 5,
        'product_grid_items_margin_top': 5,
        'product_grid_items_margin_right': 5,
        'product_grid_items_margin_bottom': 5,
        'product_grid_items_spacing': 10,

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

        # Keyboard specific settings
        'keyboard_key_width': 60,
        'keyboard_key_height': 60,
        'keyboard_space_width': 600,
        'keyboard_space_height': 55,
        'keyboard_enter_width': 180,
        'keyboard_enter_height': 55,
        'keyboard_handle_height': 45,
        'keyboard_control_button_size': 45,
        'keyboard_font_size': 22,
        'keyboard_padding': 10,
        'keyboard_spacing': 8,

        # keyboard related configs
        'keyboard_main_margin_left': 10,
        'keyboard_main_margin_top': 5,
        'keyboard_main_margin_right': 10,
        'keyboard_main_margin_bottom': 10,
        'keyboard_handle_margin_left': 5,
        'keyboard_handle_margin_top': 0,
        'keyboard_handle_margin_right': 5,
        'keyboard_handle_margin_bottom': 0,
        'keyboard_handle_spacing': 8,

        # Numpad specific settings
        'numpad_button_size': 60,
        'numpad_display_height': 50,
        'numpad_spacing': 8,
        'numpad_font_size': 16,
        'numpad_width': 300,
        'numpad_main_margin_left': 10,
        'numpad_main_margin_top': 10,
        'numpad_main_margin_right': 10,
        'numpad_main_margin_bottom': 10,
        'numpad_grid_margin_left': 5,
        'numpad_grid_margin_top': 5,
        'numpad_grid_margin_right': 5,
        'numpad_grid_margin_bottom': 5,

        # Preset button configurations
        'preset_button_width': 140,
        'preset_button_height': 35,
        'preset_widget_width': 150,
        'preset_button_margin_left': 5,
        'preset_button_margin_top': 5,
        'preset_button_margin_right': 5,
        'preset_button_margin_bottom': 5,
        'preset_button_font_size': 14,
        'preset_button_padding': 5,
        'preset_button_radius': 4,
        'preset_button_spacing': 5, 

        # Payment action button configurations
        'payment_action_button_width': 140,
        'payment_action_button_height': 40,
        'payment_action_button_font_size': 15,
        'payment_action_button_padding': 8,
        'payment_action_button_radius': 5,

        # Totals widget configurations
        'totals_label_font_size': 16,
        'totals_amount_font_size': 20,
        'totals_header_font_size': 16,
        'totals_widget_padding': 10,
        'totals_section_spacing': 15,

        # order list widget configs
        'order_header_margin_left': 10,
        'order_header_margin_top': 5,
        'order_header_margin_right': 0,
        'order_header_margin_bottom': 5,
        'order_item_margin_left': 5,
        'order_item_margin_top': 2,
        'order_item_margin_right': 5,
        'order_item_margin_bottom': 2,
        'order_quantity_label_width': 30,
        'order_total_label_width': 60,
        'order_summary_margin_left': 15,
        'order_summary_margin_top': 8,
        'order_summary_margin_right': 15,
        'order_summary_margin_bottom': 8, 
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
            'order_type_container_height': self.screen_config.get_size('pos_order_type_container_height'),
            'category_container_height': self.screen_config.get_size('pos_category_container_height'),
            'intermediate_container_height': self.screen_config.get_size('pos_intermediate_container_height'),
            'splitter_handle_width': self.screen_config.get_size('pos_splitter_handle_width'),
            'order_type_button_spacing': self.screen_config.get_size('pos_order_type_button_spacing'),
            'category_button_spacing': self.screen_config.get_size('pos_category_button_spacing'),
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
    
    def get_preset_button_config(self):
        """Get preset button configurations"""
        return {
            'width': self.screen_config.get_size('preset_button_width'),
            'height': self.screen_config.get_size('preset_button_height'),
            'widget_width': self.screen_config.get_size('preset_widget_width'),
            'margin_left': self.screen_config.get_size('preset_button_margin_left'),
            'margin_top': self.screen_config.get_size('preset_button_margin_top'),
            'margin_right': self.screen_config.get_size('preset_button_margin_right'),
            'margin_bottom': self.screen_config.get_size('preset_button_margin_bottom'),
            'font_size': self.screen_config.get_size('preset_button_font_size'),
            'padding': self.screen_config.get_size('preset_button_padding'),
            'radius': self.screen_config.get_size('preset_button_radius'),
            'spacing': self.screen_config.get_size('preset_button_spacing')
        }

    def get_payment_action_button_config(self):
        """Get payment action button configurations"""
        return {
            'width': self.screen_config.get_size('payment_action_button_width'),
            'height': self.screen_config.get_size('payment_action_button_height'),
            'font_size': self.screen_config.get_size('payment_action_button_font_size'),
            'padding': self.screen_config.get_size('payment_action_button_padding'),
            'radius': self.screen_config.get_size('payment_action_button_radius')
        }

    def get_totals_widget_config(self):
        """Get totals widget configurations"""
        return {
            'label_font_size': self.screen_config.get_size('totals_label_font_size'),
            'amount_font_size': self.screen_config.get_size('totals_amount_font_size'),
            'header_font_size': self.screen_config.get_size('totals_header_font_size'),
            'padding': self.screen_config.get_size('totals_widget_padding'),
            'spacing': self.screen_config.get_size('totals_section_spacing')
        }

# Function to initialize the layout config
def init_layout_config(screen_config):
    """Initialize the layout configuration with screen config"""
    if not LayoutConfig._instance:
        LayoutConfig(screen_config)
    return LayoutConfig._instance

# Create a global instance (will be initialized later)
layout_config = LayoutConfig()