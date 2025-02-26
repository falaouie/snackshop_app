# styles/transaction_widgets.py
"""Styles for transaction-related widgets"""

class TransactionWidgetStyles:
    """Styles for transaction buttons and containers"""
    
    # Container style
    CONTAINER = """
        QFrame {
            background: transparent;
            border: none;
        }
    """
    
    @staticmethod
    def get_layout_config(layout_config):
        """Get layout configuration for transaction buttons
        
        Args:
            layout_config: Layout config instance
        
        Returns:
            dict: Configuration values for margins and spacing
        """
        return {
            'margins': [
                layout_config.screen_config.get_size('transaction_container_margin_left'),
                layout_config.screen_config.get_size('transaction_container_margin_top'),
                layout_config.screen_config.get_size('transaction_container_margin_right'),
                layout_config.screen_config.get_size('transaction_container_margin_bottom')
            ],
            'spacing': layout_config.screen_config.get_size('transaction_buttons_spacing')
        }