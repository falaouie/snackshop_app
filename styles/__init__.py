from .buttons import ButtonStyles
from .pos import POSStyles
from .app import AppStyles
from .layouts import LayoutConfig, LayoutSizes, layout_config, init_layout_config
from .keyboard import KeyboardStyles, KeyboardConfig, KeyboardEnabledInputStyles
from .numpad import NumpadStyles

# Make sure init_styles is included here
__all__ = [
    'ButtonStyles', 'POSStyles', 'AppStyles', 
    'LayoutConfig', 'LayoutSizes', 'layout_config', 'init_layout_config',
    'KeyboardStyles', 'KeyboardConfig', 'KeyboardEnabledInputStyles',
    'NumpadStyles', 'init_styles'
]

def init_styles(screen_config):
    """Initialize all style-related configurations"""
    POSStyles.init_screen_config(screen_config)
    
    # Initialize layout_config
    layout_config = init_layout_config(screen_config)
    
    # Initialize layout_config for ButtonStyles
    ButtonStyles.init_layout_config(layout_config)
    return layout_config