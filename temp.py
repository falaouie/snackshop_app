def _create_bottom_bar(self):
        """Create bottom action bar"""
        self.bottom_bar = QFrame()
        bottom_bar_height = self.screen_config.get_size('pos_bottom_bar_height')
        
        # Apply the style with proper formatting
        self.bottom_bar.setStyleSheet(
            styles.POSStyles.BOTTOM_BAR.format(
                height=bottom_bar_height
            )
        )
        
        layout = QHBoxLayout(self.bottom_bar)
        layout.setContentsMargins(10, 5, 10, 10)
        layout.setSpacing(6)
        
        layout.addStretch()
        
