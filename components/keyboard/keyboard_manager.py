from typing import Set, Optional, Protocol
from PyQt5.QtWidgets import QWidget

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
    _instance: Optional['KeyboardManager'] = None
    
    def __new__(cls) -> 'KeyboardManager':
        if cls._instance is None:
            cls._instance = super(KeyboardManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize the keyboard manager's state"""
        self.current_input: Optional[KeyboardEnabled] = None
        self.keyboard: Optional[QWidget] = None
        self.registered_inputs: Set[KeyboardEnabled] = set()
        
    def register_keyboard(self, keyboard: QWidget) -> None:
        """Register the virtual keyboard instance"""
        self.keyboard = keyboard
        
    def register_input(self, input_widget: KeyboardEnabled) -> None:
        """Register an input widget to use the virtual keyboard"""
        self.registered_inputs.add(input_widget)
        
    def unregister_input(self, input_widget: KeyboardEnabled) -> None:
        """Unregister an input widget"""
        if input_widget in self.registered_inputs:
            self.registered_inputs.remove(input_widget)
            
    def set_current_input(self, input_widget: KeyboardEnabled) -> bool:
        """
        Set the currently focused input widget
        
        Returns:
            bool: True if input was set successfully, False otherwise
        """
        if input_widget in self.registered_inputs:
            self.current_input = input_widget
            return True
        return False
    
    def show_keyboard(self, input_widget: KeyboardEnabled) -> bool:
        """
        Show keyboard for a specific input widget
        
        Returns:
            bool: True if keyboard was shown successfully, False otherwise
        """
        if self.keyboard and input_widget in self.registered_inputs:
            self.current_input = input_widget
            self.keyboard.set_input(input_widget)
            self.keyboard.show()
            return True
        return False
    
    def hide_keyboard(self) -> None:
        """Hide the virtual keyboard"""
        if self.keyboard:
            self.keyboard.hide()
            
    def get_current_input(self) -> Optional[KeyboardEnabled]:
        """Get the currently focused input widget"""
        return self.current_input