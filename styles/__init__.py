from .base import BaseStyles
from .layouts import LayoutConfig, LayoutSizes, layout_config, init_layout_config

__all__ = ['BaseStyles', 'LayoutConfig', 'LayoutSizes', 'layout_config']

def init_styles(screen_config):
    """Initialize all style-related configurations"""
    from .buttons import ButtonStyles
    global layout_config
    layout_config = init_layout_config(screen_config)
    __all__.append('ButtonStyles')
    return layout_config