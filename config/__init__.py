"""
Configuration module for the application.
Provides access to layout configurations, screen settings, and style constants.
"""
# Import and re-export key configuration elements for easy access
from config.screen_config import screen_config
from config.style_constants import Colors, FontSizes, Spacing, BorderRadius
from config.size_categories import SizeCategory

# This allows imports like: from config import screen_config, Colors
__all__ = ['screen_config', 'Colors', 'FontSizes', 'Spacing', 'BorderRadius', 'SizeCategory']