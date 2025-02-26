from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from styles import POSStyles
from styles.layouts import layout_config

class TotalsWidget(QFrame):
    """Widget for displaying order totals in USD and LBP"""
    
    def __init__(self, exchange_rate, parent=None):
        super().__init__(parent)
        self.layout_config = layout_config.get_instance()
        self.exchange_rate = exchange_rate
        self.setStyleSheet(POSStyles.TOTALS_FRAME)
        self._setup_ui()

    def _setup_ui(self):
        """Initialize the totals widget UI"""
        # Get configuration
        totals_config = self.layout_config.get_totals_widget_config()

        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            totals_config['padding'], 
            totals_config['padding'], 
            totals_config['padding'], 
            totals_config['padding']
        )
        main_layout.setSpacing(totals_config['spacing'])
        
        # Add "Totals" header label
        header_label = QLabel("Totals")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet(f"""
            QLabel {{
                font-size: {totals_config['header_font_size']}px;
                font-weight: bold;
                color: #333;
                padding-bottom: 5px;
                border-bottom: 1px solid #dedede;
            }}
        """)
        main_layout.addWidget(header_label)
        
        # USD Total
        usd_layout = QHBoxLayout()
        usd_label = QLabel("USD:")
        usd_label.setStyleSheet(f"font-size: {totals_config['label_font_size']}px; font-weight: bold; color: #333;")
        self.usd_amount = QLabel("$0.00")
        self.usd_amount.setStyleSheet(f"""
            QLabel {{
                font-size: {totals_config['amount_font_size']}px;
                font-weight: bold;
                color: #03991f;
                text-align: right;
            }}
        """)
        self.usd_amount.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        usd_layout.addWidget(usd_label)
        usd_layout.addWidget(self.usd_amount, 1)
        
        # LBP Total
        lbp_layout = QHBoxLayout()
        lbp_label = QLabel("LBP:")
        lbp_label.setStyleSheet(f"font-size: {totals_config['label_font_size']}px; font-weight: bold; color: #333;")
        self.lbp_amount = QLabel("0")
        self.lbp_amount.setStyleSheet(f"""
            QLabel {{
                font-size: {totals_config['amount_font_size']}px;
                font-weight: bold;
                color: #1890ff;
                text-align: right;
            }}
        """)
        self.lbp_amount.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lbp_layout.addWidget(lbp_label)
        lbp_layout.addWidget(self.lbp_amount, 1)
        
        # Add layouts to main layout
        main_layout.addLayout(usd_layout)
        main_layout.addLayout(lbp_layout)
        main_layout.addStretch(1)

    def update_totals(self, amount_usd):
        """Update total amounts in both currencies"""
        total_lbp = amount_usd * self.exchange_rate
        
        self.usd_amount.setText(f"${amount_usd:,.2f}")
        self.lbp_amount.setText(f"{int(total_lbp):,}")

    def set_exchange_rate(self, rate):
        """Update the exchange rate and recalculate totals"""
        self.exchange_rate = rate
        # Force update with current USD amount
        current_usd = float(self.usd_amount.text().replace('$', '').replace(',', ''))
        self.update_totals(current_usd)