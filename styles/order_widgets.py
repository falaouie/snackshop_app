# styles/order_widgets.py
"""
Styles for order-related widgets

This module uses a configuration-based styling approach where:
1. Size and style values come from config/layouts/order_layout.py
2. All styles are accessed through methods rather than constants
3. Styles adjust automatically based on screen size
"""

from config.layouts.order_list_layout import order_layout_config 

class OrderWidgetStyles:
    """Styles for order list and related components"""
    
    # Main container style
    @staticmethod
    def get_container_style(width):
        """Get container style with width from layout config"""
        return f"""
            QFrame {{
                background: white;
                border: 1px solid #DEDEDE;
                width: {width}px;
            }}
        """
    
    # Order header style
    @staticmethod
    def get_order_header_style():
        """Get the order header style with proper margins"""
        font_size = order_layout_config.get_styling()['font_size']
        return f"""
            QFrame {{
                background: #F8F9FA;
                border: none;
            }}
            QLabel {{
                color: #2196F3;
                font-size: {font_size}px;
                font-weight: 500;
            }}
        """
    
    # header menu button style
    @staticmethod
    def get_header_menu_button_style():
        """Get header menu button style with proper sizing"""
        font_size = order_layout_config.get_styling()['font_size'] + 4  # Slightly larger
        return f"""
            QToolButton {{
                border: none;
                color: #2196F3;
                font-size: {font_size}px;
                font-weight: bold;
                padding-left: 5px;
                padding-right: 5px;
            }}
            QToolButton:hover {{
                background: #EEEEEE;
                border-radius: 4px;
            }}
        """
    
    # Order item styles
    @staticmethod
    def get_order_item_style():
        """Get order item style with config values"""
        return """
            QFrame {
                background: white;
                padding: 2px;
            }
            QLabel {
                color: #333;
            }
        """

    @staticmethod
    def get_order_item_selected_style():
        """Get selected order item style with config values"""
        return """
            QFrame {
                background: #E3F2FD;
                border: 1px solid #2196F3;
                border-radius: 4px;
            }
        """
    
    # Quantity summary style
    @staticmethod
    def get_quantity_summary_style():
        """Get quantity summary style with config values"""
        font_size = order_layout_config.get_styling()['font_size'] - 1  # Slightly smaller font
        return f"""
            QFrame {{
                background: white;
                border-top: 1px solid #DEDEDE;
            }}
            QLabel {{
                color: #666;
                font-size: {font_size}px;
            }}
        """
    
    @staticmethod
    def get_scroll_area_style():
        """Get scroll area style with proper sizing from config"""
        scroll_config = order_layout_config.get_scrollbar_config()
        return f"""
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                border: none;
                background: #F8F9FA;
                width: {scroll_config['width']}px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: #DEDEDE;
                border-radius: {scroll_config['border_radius']}px;
                min-height: {scroll_config['handle_min_height']}px;
            }}
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
        """

    @staticmethod
    def get_order_list_widget_style():
        """Get order list widget style with configuration"""
        list_config = order_layout_config.get_list_layout()
        content_margin = list_config['content_margin']
        spacing = list_config['spacing']
        return f"""
            QWidget {{
                background: white;
            }}
            QFrame {{
                background: red;
                border: none;
            }}
        """

    @staticmethod
    def get_menu_style():
        """Get menu style with proper configuration"""
        menu_config = order_layout_config.get_menu_config()
        return f"""
            QMenu {{
                background-color: white;
                border: 1px solid #DEDEDE;
                border-radius: {menu_config['border_radius']}px;
                padding: {menu_config['padding']}px;
            }}
            QMenu::item {{
                padding: {menu_config['item_padding_v']}px {menu_config['item_padding_h']}px;
                border-radius: {menu_config['border_radius']}px;
                color: #333;
                font-size: {menu_config['font_size']}px;
            }}
            QMenu::item:selected {{
                background-color: #F0F0F0;
                color: #2196F3;
            }}
            QMenu::separator {{
                height: {menu_config['separator_height']}px;
                background: #DEDEDE;
                margin: {menu_config['separator_margin']}px 0px;
            }}
        """
    
    @staticmethod
    def get_message_box_style():
        """Get message box style with proper configuration"""
        msgbox_config = order_layout_config.get_message_box_config()
        return f"""
            QMessageBox {{
                background-color: white;
                border: 1px solid #DEDEDE;
                border-radius: {msgbox_config['button_border_radius']}px;
            }}
            QMessageBox QLabel {{
                color: #333;
                font-size: {msgbox_config['font_size']}px;
                padding: {msgbox_config['padding']}px;
            }}
            QPushButton {{
                background-color: white;
                border: 1px solid #DEDEDE;
                border-radius: {msgbox_config['button_border_radius']}px;
                min-width: {msgbox_config['button_min_width']}px;
                padding: {msgbox_config['button_padding_v']}px {msgbox_config['button_padding_h']}px;
                margin: {msgbox_config['button_margin']}px;
                color: #333;
            }}
            QPushButton:hover {{
                background-color: #F0F0F0;
                border-color: #2196F3;
                color: #2196F3;
            }}
            QPushButton:default {{
                border-color: #2196F3;
                color: #2196F3;
            }}
        """
