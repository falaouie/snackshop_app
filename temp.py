def _create_intermediate_container(self):
    """Create container for numpad and payment section"""
    container = QFrame()
    container.setFixedHeight(
        self.layout_config.get_pos_layout()['intermediate_container_height']
    )
    container.setStyleSheet(POSStyles.INTERMEDIATE_CONTAINER())
    
    layout = QHBoxLayout(container)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(10)

    # Add numpad
    self.numpad_widget = NumpadWidget(self)
    self.numpad_widget.value_changed.connect(self._handle_numpad_value_change)
    if hasattr(self.numpad_widget, 'clear'):
        old_clear = self.numpad_widget.clear
        def new_clear():
            old_clear()
            self._on_numpad_cleared()
        self.numpad_widget.clear = new_clear
    layout.addWidget(self.numpad_widget)
    
    # Create and add USD Preset Widget (no longer has payment button) 
    self.usd_preset_widget = USDPresetWidget()
    self.usd_preset_widget.preset_selected.connect(self._handle_preset_selected)
    layout.addWidget(self.usd_preset_widget)

    # Create and add LBP Preset Widget (no longer has payment button)
    self.lbp_preset_widget = LBPPresetWidget()
    self.lbp_preset_widget.preset_selected.connect(self._handle_preset_selected)
    layout.addWidget(self.lbp_preset_widget)

    # Create payment options container
    payment_container = QFrame()
    payment_container.setStyleSheet(POSStyles.PAYMENT_CONTAINER())
    payment_layout = QVBoxLayout(payment_container)
    payment_layout.setContentsMargins(5, 5, 5, 5)
    payment_layout.setSpacing(10)
    
    # Add dedicated payment widgets
    # USD Payment Widget
    self.cash_usd_widget = CashUSDPaymentWidget()
    self.cash_usd_widget.payment_requested.connect(
        lambda payment_type: self._on_payment_action(payment_type)
    )
    payment_layout.addWidget(self.cash_usd_widget)
    
    # LBP Payment Widget
    self.cash_lbp_widget = CashLBPPaymentWidget()
    self.cash_lbp_widget.payment_requested.connect(
        lambda payment_type: self._on_payment_action(payment_type)
    )
    payment_layout.addWidget(self.cash_lbp_widget)
    
    # Card Payment Widget
    self.card_payment_widget = CardPaymentWidget()
    self.card_payment_widget.payment_requested.connect(
        lambda payment_type: self._on_payment_action(payment_type)
    )
    payment_layout.addWidget(self.card_payment_widget)
    
    # Other Payment Widget
    self.other_payment_widget = OtherPaymentWidget()
    self.other_payment_widget.payment_requested.connect(
        lambda payment_type: self._on_payment_action(payment_type)
    )
    payment_layout.addWidget(self.other_payment_widget)
    
    # Add payment container to main layout
    layout.addWidget(payment_container)
    
    # Add totals widget
    self.totals_widget = TotalsWidget(self.exchange_rate)
    layout.addWidget(self.totals_widget)

    return container