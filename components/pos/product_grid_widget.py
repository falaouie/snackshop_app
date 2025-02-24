from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QScrollArea, QWidget, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from styles import POSStyles, ButtonStyles
from styles.layouts import layout_config
from models.product_catalog import PRODUCTS_BY_CATEGORY, CATEGORIES
from button_definitions.types import CategoryButtonType
from button_definitions.category import CategoryButtonConfig

class ProductGridWidget(QFrame):
    """Widget for displaying and managing product grid and categories"""
    
    # Signals
    product_selected = pyqtSignal(str)  # Emits product name when selected
    category_changed = pyqtSignal(str)  # Emits category name when changed
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background: #F8F9FA;
            }
        """)
        
        self.layout_config = layout_config.get_instance()
        self.categories = CATEGORIES
        self.selected_category = None
        self.category_buttons = {}
        self.search_text = ""
        
        self.category_bar = self._create_category_bar()
        self._setup_ui()
        # Initialize first category
        self._show_category_items(self.categories[0])

    def _setup_ui(self):
        """Initialize the product grid UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 5, 0, 0)
        main_layout.setSpacing(8)

        # Horizontal Categories Row
        # main_layout.addWidget(self._create_category_bar())

        # Products Grid Area
        self.products_scroll = QScrollArea()
        self.products_scroll.setWidgetResizable(True)
        self.products_scroll.setStyleSheet(POSStyles.SCROLL_AREA)
        
        products_container = QWidget()
        self.products_grid = QGridLayout(products_container)
        self.products_grid.setSpacing(10)
        self.products_grid.setContentsMargins(5, 5, 5, 5)
        self.products_scroll.setWidget(products_container)
        
        main_layout.addWidget(self.products_scroll, 1)

    def get_category_bar(self):
        """Return the category buttons bar widget"""
        return self.category_bar
    
    def _create_category_bar(self):
        """Create horizontal category buttons bar"""
        category_frame = QFrame()
        category_frame.setStyleSheet("background: transparent;")
        
        category_layout = QHBoxLayout(category_frame)
        category_layout.setContentsMargins(5, 0, 5, 0)
        category_layout.setSpacing(8)

        # Create category buttons
        for category in self.categories:
            config = CategoryButtonConfig.get_config(
                CategoryButtonType.CATEGORY,
                category
            )
            btn = QPushButton(config['text'])
            
            grid_config = self.layout_config.get_product_grid_config()
            btn.setStyleSheet(ButtonStyles.get_category_button_style(is_selected=False))
            btn.setFixedSize(
                grid_config['category_button']['width'],
                grid_config['category_button']['height']
            )
            
            btn.clicked.connect(lambda checked, c=category: self._show_category_items(c))
            category_layout.addWidget(btn)
            self.category_buttons[category] = btn

        category_layout.addStretch()
        return category_frame

    def _show_category_items(self, category):
        """Display product items for selected category"""
        # Update category button styles
        if category in self.category_buttons:
            # Reset previously selected button
            if self.selected_category:
                prev_btn = self.category_buttons[self.selected_category]
                prev_btn.setStyleSheet(ButtonStyles.get_category_button_style(is_selected=False))
            
            # Update newly selected button
            curr_btn = self.category_buttons[category]
            curr_btn.setStyleSheet(ButtonStyles.get_category_button_style(is_selected=True))
            self.selected_category = category
            self.category_changed.emit(category)

        # Clear existing products grid
        self._clear_grid()

        # Get items and apply search filter
        items = PRODUCTS_BY_CATEGORY[category]
        filtered_items = self._filter_items(items)

        # Add product buttons to grid
        self._populate_grid(filtered_items)

    def _clear_grid(self):
        """Clear all items from the product grid"""
        for i in reversed(range(self.products_grid.count())):
            widget = self.products_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def _filter_items(self, items):
        """Filter items based on search text"""
        if not self.search_text:
            return items
        return [item for item in items if self.search_text.lower() in item.lower()]

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

    def find_product_button(self, product_name):
        """Find a product button by its name
        
        Args:
            product_name (str): Name of the product to find
            
        Returns:
            QPushButton or None: The button if found, None otherwise
        """
        for i in range(self.products_grid.count()):
            widget = self.products_grid.itemAt(i).widget()
            if isinstance(widget, QPushButton) and widget.property('product_name') == product_name:
                return widget
        return None
    
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

    def set_search_text(self, text):
        """Update search filter and refresh grid"""
        self.search_text = text.strip()
        if self.selected_category:
            self._show_category_items(self.selected_category)