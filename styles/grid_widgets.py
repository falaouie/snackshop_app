# styles/grid_widgets.py
"""Styles for grid-related widgets"""

class GridWidgetStyles:
    """Styles for product grid and category widgets"""
    
    # Main container frame style
    CONTAINER = """
        QFrame {
            background: #F8F9FA;
        }
    """
    
    # Category frame style
    CATEGORY_FRAME = """
        QFrame {
            background: transparent;
        }
    """
    
    # Scroll area style (migrated from POSStyles)
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
    
    @staticmethod
    def get_disabled_product_button_style(base_style):
        """Get style for disabled product buttons
        
        Args:
            base_style: The base button style to extend
            
        Returns:
            str: Style with disabled state
        """
        return base_style + """
            QPushButton[disabled_by_numpad="true"] {
                background-color: #E0E0E0;
                color: #666666;
            }
        """