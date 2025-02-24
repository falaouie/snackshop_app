class ProductGridWidget(QFrame):
    # ... existing code ...

    def _populate_grid(self, items):
        """Populate grid with product buttons"""
        product_style = ButtonStyles.get_product_button_style()
        grid_config = self.layout_config.get_product_grid_config()

        for i, item in enumerate(items):
            btn = QPushButton(item)
            btn.setProperty('product_name', item)  # Track product name
            btn.setProperty('disabled_by_numpad', False)  # Track disabled state
            btn.setFixedSize(
                grid_config['product_button']['width'],
                grid_config['product_button']['height']
            )
            btn.setStyleSheet(product_style)
            btn.clicked.connect(lambda checked, name=item: self.product_selected.emit(name))
            
            row = i // 3  # 3 columns per row
            col = i % 3
            self.products_grid.addWidget(btn, row, col)

    def disable_button_temporarily(self, product_name):
        """Handle temporary button disable with styling"""
        button = self.find_product_button(product_name)
        if button:
            self._apply_disabled_style(button)
            return True
        return False

    def enable_button(self, product_name):
        """Reset button to normal state"""
        button = self.find_product_button(product_name)
        if button:
            self._reset_button_style(button)

    def _apply_disabled_style(self, button):
        """Apply disabled style to button"""
        button.setProperty('disabled_by_numpad', True)
        base_style = ButtonStyles.get_product_button_style()
        disabled_style = base_style + """
            QPushButton[disabled_by_numpad="true"] {
                background-color: #E0E0E0;
                color: #666666;
            }
        """
        button.setStyleSheet(disabled_style)
        self._refresh_button_style(button)

    def _reset_button_style(self, button):
        """Reset button to normal style"""
        button.setProperty('disabled_by_numpad', False)
        button.setStyleSheet(ButtonStyles.get_product_button_style())
        self._refresh_button_style(button)

    def _refresh_button_style(self, button):
        """Force button style refresh"""
        button.style().unpolish(button)
        button.style().polish(button)
        button.update()

    def find_product_button(self, product_name):
        """Find a product button by its name"""
        for i in range(self.products_grid.count()):
            widget = self.products_grid.itemAt(i).widget()
            if isinstance(widget, QPushButton) and widget.property('product_name') == product_name:
                return widget
        return None