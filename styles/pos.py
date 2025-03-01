class POSStyles:
    """POS view specific styles"""
    screen_config = None
    
    @classmethod
    def init_screen_config(cls, config):
        cls.screen_config = config
    
    # Top bar styles
    @classmethod
    def TOP_BAR(cls, height):
        return f"""
            QFrame {{
                background: #F0F0F0;
                border-bottom: 1px solid #DEDEDE;
                height: {height}px;
            }}
        """
    
    EMPLOYEE_ZONE = """
        QFrame {
            background: transparent;
            border: none;
        }
    """
    
    EMPLOYEE_ID = """
        QLabel {
            color: #333;
            font-weight: 500;
        }
    """
    
    DATE_TIME_ZONE = """
        QFrame {
            background: transparent;
            border: none;
        }
    """
    
    DATE_LABEL = """
        QLabel {
            color: #666;
        }
    """
    
    TIME_LABEL = """
        QLabel {
            color: #333;
            font-weight: 500;
            padding-left: 4px;
        }
    """
    
    # Search input styles
    @classmethod
    def SEARCH_INPUT(cls, width, height):
        return f"""
            QLineEdit {{
                border: 1px solid #DEDEDE;
                border-radius: 20px;
                padding: 8px 40px;
                font-size: 14px;
                color: #333;
                background: white;
                width: {width}px;
                height: {height}px;
            }}
            QLineEdit:focus {{
                border-color: #2196F3;
                outline: none;
            }}
        """
    
    @classmethod
    def ORDER_TYPE_CONTAINER(cls):
        """Style for the container holding order type buttons"""
        return """
            QWidget {
                background: white;
                border-bottom: 1px solid #DEDEDE;
            }
        """
    
    @classmethod
    def CATEGORY_CONTAINER(cls):
        """Style for the container holding category buttons"""
        return """
            QWidget {
                background: white;
                border-bottom: 1px solid #DEDEDE;
            }
        """
    
    # center panel and intermediate container styles
    @classmethod
    def CENTER_PANEL(cls):
        """Style for the center panel holding transaction buttons"""
        return """
            QFrame, QWidget {
                background: white;
                border: px solid #DEDEDE;
            }
        """

    @classmethod
    def INTERMEDIATE_CONTAINER(cls):
        """Style for the intermediate container holding numpad and payment sections"""
        return """
            QFrame {
                background: white;
                border-top: 1px solid #DEDEDE;
            }
        """
    
    @classmethod
    def PRODUCTS_FRAME(cls):
        """Style for the main products frame"""
        return """
            QFrame {
                background: #F8F9FA;
            }
        """

    @classmethod
    def LEFT_CONTAINER(cls):
        """Style for the left container holding order type and order list"""
        return """
            QWidget {
                background: white;
            }
        """

    @classmethod
    def PAYMENT_CONTAINER(cls):
        """Style for the payment section container"""
        return """
            QFrame {
                background: white;
                border-left: 1px solid #DEDEDE;
                padding: 10px;
            }
        """

    SPLITTER = """
        QSplitter {
            background: transparent;
        }
        QSplitter::handle {
            background: #DEDEDE;
            width: 1px;
        }
        QSplitter::handle:hover {
            background: #2196F3;
        }
    """

    # Product button styles
    @classmethod
    def get_product_button_style(cls):
        if not cls.screen_config:
            return ""
            
        return f"""
            QPushButton {{
                background: white;
                border: 1px solid #DEDEDE;
                border-radius: {cls.screen_config.get_size('button_border_radius')}px;
                padding: {cls.screen_config.get_size('button_padding')}px;
                color: #333;
                font-size: 14px;
                width: {cls.screen_config.get_size('pos_product_button_width')}px;
                height: {cls.screen_config.get_size('pos_product_button_height')}px;
            }}
            QPushButton:hover {{
                background: #F8F9FA;
                border-color: #2196F3;
            }}
            QPushButton:pressed {{
                background: #F1F1F1;
            }}
        """
    
    # Bottom bar styles
    @classmethod
    def BOTTOM_BAR(cls, height):
        return f"""
            QFrame {{
                background: #F8F9FA;
                border-top: 1px solid #DEDEDE;
                height: {height}px;
                margin-bottom: 10px;
            }}
        """
    
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
    
    LOCK_BUTTON = """
        QPushButton {
            background: transparent;
            border: none;
            padding: 0px;
        }
    """
    
    TOTALS_FRAME = """
        QFrame {
            background: white;
            border: 1px solid #DEDEDE;
            border-radius: 5px;
        }
    """