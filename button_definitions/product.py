from .types import ProductButtonType
from typing import Dict, Any

class ProductButtonConfig:
    """Configuration for product buttons with support for future customization"""
    DEFAULTS = {
        "text_color": "#333333",
        "font_weight": 500,
        "background": "white",
        "border_color": "#DEDEDE",
        "border_color_hover": "#2196F3",
        "background_hover": "#F8F9FA",
        "background_pressed": "#F1F1F1"
    }

    @classmethod
    def get_config(cls, button_type: ProductButtonType, product_name: str, category: str = None) -> dict:
        """
        Get configuration for a product button
        
        Args:
            button_type: Type of product button (enum)
            product_name: Name of the product
            category: Optional category for future category-based styling
        """
        if button_type != ProductButtonType.PRODUCT:
            return {}

        colors = cls.DEFAULTS.copy()
        
        # Future enhancement: Check for custom styles
        # if db_connection:
        #     custom_style = db_connection.get_product_style(product_name)
        #     if custom_style:
        #         colors.update(custom_style)
        
        # Future enhancement: Check for category-based styles
        # if category and db_connection:
        #     category_style = db_connection.get_category_style(category)
        #     if category_style:
        #         colors.update(category_style)

        return {
            "text": product_name,
            "colors": colors,
            "action": "_handle_product_click"
        }

    @classmethod
    def create_grid_button(cls, product_name: str, category: str = None) -> dict:
        """Create a complete button configuration for the product grid"""
        return {
            "type": ProductButtonType.PRODUCT,
            "config": cls.get_config(product_name, category)
        }