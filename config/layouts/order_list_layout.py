"""
Layout configuration for the Order List component.
Provides dimensions and styling specific to the Order UI.
"""
from config.screen_config import screen_config
from config.size_categories import SizeCategory

class OrderLayoutConfig:
    """Layout configuration for order list dimensions and styling"""
    _instance = None
    
    # Define size configurations for different screen sizes
    CONFIGS = {
        SizeCategory.SMALL: {
            'order_list_panel_width': 300,
            'header_margin_left': 10,
            'header_margin_top': 5,
            'header_margin_right': 0,
            'header_margin_bottom': 5,
            'item_margin_left': 5,
            'item_margin_top': 2,
            'item_margin_right': 5,
            'item_margin_bottom': 2,
            'quantity_label_width': 30,
            'total_label_width': 60,
            'summary_margin_left': 15,
            'summary_margin_top': 8,
            'summary_margin_right': 15,
            'summary_margin_bottom': 8,
            'font_size': 13,

            # scroll area configs
            'scrollbar_width': 8,
            'scrollbar_handle_min_height': 20,
            'scrollbar_border_radius': 4,
            
            # Order list widget configs
            'list_content_margin': 5,
            'list_spacing': 5,
            
            # Menu configs
            'menu_padding': 5,
            'menu_item_padding_h': 20,
            'menu_item_padding_v': 8,
            'menu_border_radius': 4,
            'menu_font_size': 13,
            'menu_separator_height': 1,
            'menu_separator_margin': 5,
            
            # Message box configs
            'msgbox_button_min_width': 80,
            'msgbox_button_padding_h': 12,
            'msgbox_button_padding_v': 6,
            'msgbox_button_margin': 4,
            'msgbox_button_border_radius': 4,
            'msgbox_font_size': 14,
            'msgbox_padding': 10,
        },
        
        SizeCategory.MEDIUM: {
            'order_list_panel_width': 350,
            'header_margin_left': 5,
            'header_margin_top': 5,
            'header_margin_right': 5,
            'header_margin_bottom': 5,
            'item_margin_left': 2,
            'item_margin_top': 2,
            'item_margin_right': 2,
            'item_margin_bottom': 2,
            'quantity_label_width': 30,
            'total_label_width': 60,
            'summary_margin_left': 15,
            'summary_margin_top': 8,
            'summary_margin_right': 15,
            'summary_margin_bottom': 8,
            'font_size': 14,

            # scroll area configs
            'scrollbar_width': 8,
            'scrollbar_handle_min_height': 20,
            'scrollbar_border_radius': 4,
            
            # Order list widget configs
            'list_content_margin': 5,
            'list_spacing': 5,
            
            # Menu configs
            'menu_padding': 5,
            'menu_item_padding_h': 20,
            'menu_item_padding_v': 8,
            'menu_border_radius': 4,
            'menu_font_size': 14,
            'menu_separator_height': 1,
            'menu_separator_margin': 5,
            
            # Message box configs
            'msgbox_button_min_width': 80,
            'msgbox_button_padding_h': 12,
            'msgbox_button_padding_v': 6,
            'msgbox_button_margin': 4,
            'msgbox_button_border_radius': 4,
            'msgbox_font_size': 15,
            'msgbox_padding': 10,
        },
        
        SizeCategory.LARGE: {
            'order_list_panel_width': 400,
            'header_margin_left': 5,
            'header_margin_top': 5,
            'header_margin_right': 0,
            'header_margin_bottom': 5,
            'item_margin_left': 5,
            'item_margin_top': 2,
            'item_margin_right': 5,
            'item_margin_bottom': 2,
            'quantity_label_width': 30,
            'total_label_width': 160,
            'summary_margin_left': 15,
            'summary_margin_top': 8,
            'summary_margin_right': 15,
            'summary_margin_bottom': 8,
            'font_size': 14,

            # scroll area configs
            'scrollbar_width': 10,
            'scrollbar_handle_min_height': 25,
            'scrollbar_border_radius': 5,
            
            # Order list widget configs
            'list_content_margin': 6,
            'list_spacing': 6,
            
            # Menu configs
            'menu_padding': 6,
            'menu_item_padding_h': 25,
            'menu_item_padding_v': 10,
            'menu_border_radius': 5,
            'menu_font_size': 16,
            'menu_separator_height': 1,
            'menu_separator_margin': 6,
            
            # Message box configs
            'msgbox_button_min_width': 100,
            'msgbox_button_padding_h': 15,
            'msgbox_button_padding_v': 8,
            'msgbox_button_margin': 5,
            'msgbox_button_border_radius': 5,
            'msgbox_font_size': 16,
            'msgbox_padding': 12,
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
        
    def get_panel_dimensions(self):
        """Get order panel dimensions"""
        config = self._get_current_config()
        return {
            'width': config['order_list_panel_width']
        }
    
    def get_header_margins(self):
        """Get header margins"""
        config = self._get_current_config()
        return [
            config['header_margin_left'],
            config['header_margin_top'],
            config['header_margin_right'],
            config['header_margin_bottom']
        ]
    
    def get_item_margins(self):
        """Get item margins"""
        config = self._get_current_config()
        return [
            config['item_margin_left'],
            config['item_margin_top'],
            config['item_margin_right'],
            config['item_margin_bottom']
        ]
    
    def get_summary_margins(self):
        """Get summary margins"""
        config = self._get_current_config()
        return [
            config['summary_margin_left'],
            config['summary_margin_top'],
            config['summary_margin_right'],
            config['summary_margin_bottom']
        ]
    
    def get_label_widths(self):
        """Get label widths"""
        config = self._get_current_config()
        return {
            'quantity': config['quantity_label_width'],
            'total': config['total_label_width']
        }
    
    def get_styling(self):
        """Get styling parameters"""
        config = self._get_current_config()
        return {
            'font_size': config['font_size']
        }
    
    # accessor methods for scroll area
    def get_scrollbar_config(self):
        """Get scrollbar configuration"""
        config = self._get_current_config()
        return {
            'width': config['scrollbar_width'],
            'handle_min_height': config['scrollbar_handle_min_height'],
            'border_radius': config['scrollbar_border_radius']
        }
    
    # accessor methods for list widget
    def get_list_layout(self):
        """Get list widget layout configuration"""
        config = self._get_current_config()
        return {
            'content_margin': config['list_content_margin'],
            'spacing': config['list_spacing']
        }
    
    # accessor methods for menu
    def get_menu_config(self):
        """Get menu configuration"""
        config = self._get_current_config()
        return {
            'padding': config['menu_padding'],
            'item_padding_h': config['menu_item_padding_h'],
            'item_padding_v': config['menu_item_padding_v'],
            'border_radius': config['menu_border_radius'],
            'font_size': config['menu_font_size'],
            'separator_height': config['menu_separator_height'],
            'separator_margin': config['menu_separator_margin']
        }
    
    # accessor methods for message box
    def get_message_box_config(self):
        """Get message box configuration"""
        config = self._get_current_config()
        return {
            'button_min_width': config['msgbox_button_min_width'],
            'button_padding_h': config['msgbox_button_padding_h'],
            'button_padding_v': config['msgbox_button_padding_v'],
            'button_margin': config['msgbox_button_margin'],
            'button_border_radius': config['msgbox_button_border_radius'],
            'font_size': config['msgbox_font_size'],
            'padding': config['msgbox_padding']
        }

# Create singleton instance
order_layout_config = OrderLayoutConfig()