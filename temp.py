class POSStyles:
    """POS view specific styles"""
    screen_config = None
    
    @classmethod
    def init_screen_config(cls, config):
        cls.screen_config = config
    
    # Existing styles remain...

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

    @classmethod
    def CENTER_PANEL(cls):
        """Style for the center panel holding transaction buttons"""
        return """
            QFrame {
                background: white;
                border-left: 1px solid #DEDEDE;
                border-right: 1px solid #DEDEDE;
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