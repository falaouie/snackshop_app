# In styles/order_widgets.py
@staticmethod
def get_container_style(width=None):
    """Get container style with width from config"""
    # Use passed width for backward compatibility or get from config
    panel_width = width if width is not None else order_layout_config.get_size('panel_width')
    return f"""
        QFrame {{
            background: white;
            border: 1px solid #DEDEDE;
            width: {panel_width}px;
        }}
    """