# styles/order_widgets.py
"""Styles for order-related widgets"""

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
    
    # Order list widget style
    ORDER_LIST_WIDGET = """
        QWidget {
            background: white;
        }
        QFrame {
            background: white;
            border: none;
        }
    """
    
    # Order header style
    ORDER_HEADER = """
        QFrame {
            background: #F8F9FA;
            border: none;
        }
        QLabel {
            color: #2196F3;
            font-size: 16px;
            font-weight: 500;
        }
    """
    
    # Header menu button style
    HEADER_MENU_BUTTON = """
        QToolButton {
            border: none;
            color: #2196F3;
            font-size: 20px;
            font-weight: bold;
            padding-left: 5px;
            padding-right: 5px;
        }
        QToolButton:hover {
            background: #EEEEEE;
            border-radius: 4px;
        }
    """
    
    # Order item styles
    ORDER_ITEM = """
        QFrame {
            background: white;
            border-bottom: 1px solid #EEEEEE;
            padding: 2px;
        }
        QLabel {
            color: #333;
        }
    """
    
    ORDER_ITEM_SELECTED = """
        QFrame {
            background: #E3F2FD;
            border: 1px solid #2196F3;
            border-radius: 4px;
        }
    """
    
    # Quantity summary style
    QUANTITY_SUMMARY = """
        QFrame {
            background: white;
            border-top: 1px solid #DEDEDE;
        }
        QLabel {
            color: #666;
            font-size: 13px;
        }
    """
    
    # Message box style
    MESSAGE_BOX = """
        QMessageBox {
            background-color: white;
            border: 1px solid #DEDEDE;
            border-radius: 4px;
        }
        QMessageBox QLabel {
            color: #333;
            font-size: 14px;
            padding: 10px;
        }
        QPushButton {
            background-color: white;
            border: 1px solid #DEDEDE;
            border-radius: 4px;
            min-width: 80px;
            padding: 6px 12px;
            margin: 4px;
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
    
    # Scroll area style
    SCROLL_AREA = """
        QScrollArea {
            border: none;
            background: transparent;
        }
        QScrollBar:vertical {
            border: none;
            background: #F8F9FA;
            width: 8px;
            margin: 0;
        }
        QScrollBar::handle:vertical {
            background: #DEDEDE;
            border-radius: 4px;
            min-height: 20px;
        }
        QScrollBar::add-line:vertical, 
        QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
    """
    
    # Menu style
    MENU = """
        QMenu {
            background-color: white;
            border: 1px solid #DEDEDE;
            border-radius: 4px;
            padding: 5px;
        }
        QMenu::item {
            padding: 8px 20px;
            border-radius: 4px;
            color: #333;
        }
        QMenu::item:selected {
            background-color: #F0F0F0;
            color: #2196F3;
        }
        QMenu::separator {
            height: 1px;
            background: #DEDEDE;
            margin: 5px 0px;
        }
    """