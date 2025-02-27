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
    
    # Add USD Preset Widget (without removing the payment button yet)
    self.usd_preset_widget = USDPresetWidget()
    self.usd_preset_widget.preset_selected.connect(self._handle_preset_selected)
    self.usd_preset_widget.payment_requested.connect(
        lambda payment_type: self._on_payment_action(payment_type)
    )
    layout.addWidget(self.usd_preset_widget)

    # Add LBP Preset Widget (without removing the payment button yet)
    self.lbp_preset_widget = LBPPresetWidget()
    self.lbp_preset_widget.preset_selected.connect(self._handle_preset_selected)
    self.lbp_preset_widget.payment_requested.connect(
        lambda payment_type: self._on_payment_action(payment_type)
    )
    layout.addWidget(self.lbp_preset_widget)
    
    # Create payment options container for totals and payment methods
    payment_container = QFrame()
    payment_container.setStyleSheet(POSStyles.PAYMENT_CONTAINER())
    payment_layout = QVBoxLayout(payment_container)
    payment_layout.setContentsMargins(5, 5, 5, 5)
    payment_layout.setSpacing(10)
    
    # Now we'll get the payment buttons from the preset widgets and add them to the payment container
    
    # Get USD payment button reference (we'll remove it from its original layout in Step 3)
    self.usd_payment_btn = self.usd_preset_widget.payment_btn
    
    # Get LBP payment button reference (we'll remove it from its original layout in Step 3)
    self.lbp_payment_btn = self.lbp_preset_widget.payment_btn
    
    # Add card payment widget
    self.card_payment_widget = CardPaymentWidget()
    self.card_payment_widget.payment_requested.connect(lambda payment_type: self._on_payment_action(payment_type))
    
    # Add other payment widget
    self.other_payment_widget = OtherPaymentWidget()
    self.other_payment_widget.payment_requested.connect(lambda payment_type: self._on_payment_action(payment_type))
    
    # Add payment container to main layout
    layout.addWidget(payment_container)
    
    # Add totals widget
    self.totals_widget = TotalsWidget(self.exchange_rate)
    layout.addWidget(self.totals_widget)

    return container