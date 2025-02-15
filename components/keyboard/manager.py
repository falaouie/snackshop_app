from typing import Set, Optional, Protocol
from .types import KeyboardType

class KeyboardEnabled(Protocol):
    """Protocol defining required methods for keyboard-enabled widgets"""
    def setFocus(self) -> None:
        ...
    
    def text(self) -> str:
        ...
    
    def setText(self, text: str) -> None:
        ...
    
    def cursorPosition(self) -> int:
        ...
    
    def setCursorPosition(self, pos: int) -> None:
        ...

class KeyboardManager:
    """Singleton manager for virtual keyboard interactions"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KeyboardManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the keyboard manager"""
        self.current_input = None
        self.keyboard = None
        self.registered_inputs = set()
        
    def register_keyboard(self, keyboard):
        """Register the virtual keyboard instance"""
        self.keyboard = keyboard
        
    def register_input(self, input_widget):
        """Register an input widget to use the virtual keyboard"""
        self.registered_inputs.add(input_widget)
        
    def unregister_input(self, input_widget):
        """Unregister an input widget"""
        if input_widget in self.registered_inputs:
            self.registered_inputs.remove(input_widget)
            
    def set_current_input(self, input_widget):
        """Set the currently focused input widget"""
        if input_widget in self.registered_inputs:
            self.current_input = input_widget
            return True
        return False
    
    def show_keyboard(self, input_widget, keyboard_type=KeyboardType.FULL):
        """Show keyboard for a specific input widget with specified type"""
        if self.keyboard and input_widget in self.registered_inputs:
            self.current_input = input_widget
            
            # If keyboard is minimized, restore it first
            if self.keyboard.is_minimized:
                self.keyboard._on_restore()
                
            self.keyboard.set_input(input_widget, keyboard_type)
            self.keyboard.show()
            return True
        return False
    
    def hide_keyboard(self) -> None:
        """Hide the virtual keyboard"""
        if self.keyboard:
            self.keyboard.hide()
            
    def get_current_input(self):
        """Get the currently focused input widget"""
        return self.current_input