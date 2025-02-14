class BaseStyles:
    """Base styles and common style utilities"""
    
    @staticmethod
    def create_button_style(
        background_color: str,
        text_color: str,
        hover_color: str,
        border_radius: int,
        padding: int,
        font_size: int,
        extra_styles: dict = None
    ) -> str:
        """Generate a base button style with given properties"""
        style = f"""
            QPushButton {{
                background-color: {background_color};
                color: {text_color};
                border: none;
                border-radius: {border_radius}px;
                padding: {padding}px;
                font-size: {font_size}px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """
        
        if extra_styles:
            for state, properties in extra_styles.items():
                style += f"\nQPushButton:{state} {{\n"
                for prop, value in properties.items():
                    style += f"    {prop}: {value};\n"
                style += "}"
                
        return style