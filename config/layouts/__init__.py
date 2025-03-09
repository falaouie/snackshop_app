"""
Layout configuration package for UI components.
Provides centralized access to screen-responsive layout configurations.
"""
# Import layout configurations for easy access
from config.layouts.numpad_layout import numpad_layout_config
from config.layouts.auth_layout import AuthTopBarLayoutConfig

# This allows imports like: from config.layouts import numpad_layout_config
__all__ = ['numpad_layout_config', 'AuthTopBarLayoutConfig']

# As you refactor more components, add their config imports and __all__ entries here