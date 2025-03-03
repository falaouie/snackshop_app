# styles/order_widgets.py
"""
Styles for order-related widgets

This module follows a clean separation of concerns where:
1. Stylesheets handle only visual appearance (colors, borders)
2. Widget methods handle sizing and font properties
3. Config values are used directly by the widget, not in the stylesheet
"""

class OrderWidgetStyles:
    """Styles for order list and related components"""
    
    # Order header style
    @staticmethod
    def get_order_header_style():
        """Get the order header style"""
        return """
            QFrame {
                background: #F8F9FA;
                border: none;
            }
            QLabel {
                color: #2196F3;
                font-weight: 500;
            }
        """
    
    # header menu button style
    @staticmethod
    def get_header_menu_button_style():
        """Get header menu button style"""
        return """
            QToolButton {
                border: none;
                color: #2196F3;
                font-weight: bold;
            }
            QToolButton:hover {
                background: #EEEEEE;
                border-radius: 4px;
            }
        """
    
    # Order item styles
    @staticmethod
    def get_order_item_style():
        """Get order item style"""
        return """
            QFrame {
                background: white;
            }
            QLabel {
                color: #333;
            }
        """

    @staticmethod
    def get_order_item_selected_style():
        """Get selected order item style"""
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
        """Get quantity summary style"""
        return """
            QFrame {
                background: white;
                border-top: 1px solid #DEDEDE;
            }
            QLabel {
                color: #666;
            }
        """
    
    @staticmethod
    def get_scroll_area_style():
        """Get scroll area style"""
        return """
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #F8F9FA;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #DEDEDE;
            }
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """

    @staticmethod
    def get_order_list_widget_style():
        """Get order list widget style"""
        return """
            QWidget {
                background: white;
            }
            QFrame {
                background: white;
                border: none;
            }
        """

    @staticmethod
    def get_menu_style():
        """Get menu style"""
        return """
            QMenu {
                background-color: white;
                border: 1px solid #DEDEDE;
            }
            QMenu::item {
                color: #333;
            }
            QMenu::item:selected {
                background-color: #F0F0F0;
                color: #2196F3;
            }
            QMenu::separator {
                background: #DEDEDE;
            }
        """
    
    @staticmethod
    def get_message_box_style():
        """Get message box style"""
        return """
            QMessageBox {
                background-color: white;
                border: 1px solid #DEDEDE;
            }
            QMessageBox QLabel {
                color: #333;
            }
            QPushButton {
                background-color: white;
                border: 1px solid #DEDEDE;
                color: #333;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
                border-color: #2196F3;
                color: #2196F3;
            }
            QPushButton:default {
                border-color: #2196F3;
                color: #2196F3;
            }
        """

    # NEW: Add quantity dialog styles
    @staticmethod
    def get_quantity_dialog_style():
        """Get quantity dialog style"""
        return """
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                border: 1px solid #DEDEDE;
                background: white;
            }
            QPushButton:hover {
                background: #F5F5F5;
                border-color: #2196F3;
            }
        """

    # NEW: Add order container style
    @staticmethod
    def get_order_container_style():
        """Get order container style"""
        return """
            QFrame {
                background: white;
                border: none;
            }
        """