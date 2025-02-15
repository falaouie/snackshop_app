from .types import CategoryButtonType

class CategoryButtonConfig:
    """Configuration for category selection buttons"""
    DEFAULTS = {
        # Normal state
        "text_color": "#333333",
        "background": "white",
        "border_color": "#DEDEDE",
        # Selected state
        "selected_text_color": "white",
        "selected_background": "#2196F3",
        "selected_border_color": "#2196F3",
        # Hover state
        "hover_background": "#F8F9FA",
        "hover_border_color": "#2196F3",
        # Selected hover state
        "selected_hover_background": "#1E88E5",
    }

    @classmethod
    def get_config(cls, button_type: CategoryButtonType, category_name: str) -> dict:
        """
        Get configuration for a category button
        
        Args:
            button_type: Type of category button (enum)
            category_name: Name of the category
        """
        if button_type != CategoryButtonType.CATEGORY:
            return {}

        colors = cls.DEFAULTS.copy()

        # Future enhancement: Check for custom category styles
        # if db_connection:
        #     custom_style = db_connection.get_category_style(category_name)
        #     if custom_style:
        #         colors.update(custom_style)

        return {
            "text": category_name,
            "colors": colors,
            "action": "_show_category_items"
        }