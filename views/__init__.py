# views/__init__.py
from .main_window import MainWindow
from .pos.pos_view import POSView
from .view_manager import ViewManager

__all__ = [
    'MainWindow',
    'POSView',
    'ViewManager',
]