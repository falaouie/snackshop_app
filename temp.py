# Changes needed in pos_view.py for Group 1: Button Dimensions

# 1. Add layout_config import at the top (keep screen_config for now)
from styles.layouts import layout_config

class POSView(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.screen_config = screen_config  # Keep for now
        self.layout_config = layout_config.get_instance()  # Add this line
        # ... rest of __init__ remains the same ...

    def _create_order_widget(self):
        """Create order panel"""
        # ... existing code ...

        # In the horizontal buttons section, update button sizes:
        for button_type in HorizontalButtonType:
            config = HorizontalButtonConfig.get_config(button_type)
            btn = QPushButton(config['text'])
            btn.setStyleSheet(ButtonStyles.get_horizontal_button_style(button_type))
            
            # Replace this:
            # btn.setFixedSize(
            #     self.screen_config.get_size('horizontal_button.width'),
            #     self.screen_config.get_size('horizontal_button.height')
            # )
            
            # With this:
            button_config = self.layout_config.get_button_config('horizontal')
            btn.setFixedSize(
                button_config['width'],
                button_config['height']
            )
            
            # ... rest remains the same ...

    def _create_products_widget(self):
        """Create products panel"""
        # ... existing code ...

        # In the transaction buttons section:
        for button_type in TransactionButtonType:
            config = TransactionButtonConfig.get_config(button_type)
            btn = QPushButton(config['text'])
            btn.setStyleSheet(ButtonStyles.get_transaction_button_style(button_type))
            
            # Replace this:
            # btn.setFixedSize(
            #     self.screen_config.get_size('transaction_button.width'),
            #     self.screen_config.get_size('transaction_button.height')
            # )
            
            # With this:
            button_config = self.layout_config.get_button_config('transaction')
            btn.setFixedSize(
                button_config['width'],
                button_config['height']
            )
            
            # ... rest remains the same ...

        # In the order type buttons section:
        # Replace similar button size settings with:
        button_config = self.layout_config.get_button_config('order_type')
        btn.setFixedSize(
            button_config['width'],
            button_config['height']
        )

    def _create_bottom_bar(self):
        """Create bottom action bar"""
        # ... existing code ...

        # In the payment buttons section:
        for button_type in PaymentButtonType:
            config = PaymentButtonConfig.get_config(button_type)
            btn = QPushButton(config['text'])
            btn.setStyleSheet(ButtonStyles.get_payment_button_style(button_type))
            
            # Replace this:
            # btn.setFixedSize(
            #     self.screen_config.get_size('payment_button.width'),
            #     self.screen_config.get_size('payment_button.height')
            # )
            
            # With this:
            button_config = self.layout_config.get_button_config('payment')
            btn.setFixedSize(
                button_config['width'],
                button_config['height']
            )
            
            # ... rest remains the same ...