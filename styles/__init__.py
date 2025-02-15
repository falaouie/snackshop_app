from .base import BaseStyles
from .buttons import ButtonStyles
from .pos import POSStyles
from .app import AppStyles
from .layouts import LayoutConfig, LayoutSizes, layout_config, init_layout_config

__all__ = ['BaseStyles', 'ButtonStyles', 'POSStyles', 'AppStyles', 'LayoutConfig', 'LayoutSizes', 'layout_config']

def init_styles(screen_config):
    """Initialize all style-related configurations"""
    ButtonStyles.init_screen_config(screen_config)
    POSStyles.init_screen_config(screen_config)
    layout_config = init_layout_config(screen_config)
    return layout_config