# styles/components.py
from config.layouts.search_layout import search_layout_config

class SearchStyles:
    @staticmethod
    def get_input_style(width, height):
        config = search_layout_config._get_current_config()
        font_size = config['font_size']
        padding = config['padding']
        border_radius = config['border_radius']
            
        return f"""
            QLineEdit {{
                width: {width}px;
                height: {height}px;
                background-color: white;
                border: 1px solid #DEDEDE;
                border-radius: {border_radius}px;
                padding-left: {padding + 30}px;
                padding-right: {padding}px;
                font-size: {font_size}px;
                color: #333333;
            }}
            QLineEdit:focus {{
                border: 1px solid #2196F3;
            }}
        """