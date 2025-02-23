class NumpadStyles:
    """Styles for the numpad component"""
    
    # Base container style
    CONTAINER = """
        QFrame {
            background: white;
            border: 1px solid #DEDEDE;
            border-radius: 4px;
        }
    """

    # Display style
    DISPLAY = """
        QLineEdit {
            border: 1px solid #DEDEDE;
            border-radius: 4px;
            padding: 8px;
            font-size: 24px;
            background: #F9F9F9;
            min-height: 50px;
        }
        QLineEdit:disabled {
            background: #F9F9F9;
            color: #333;
        }
    """

    # QTY mode button style
    QTY_BUTTON = """
        QPushButton {
            background: white;
            border: 1px solid #DEDEDE;
            border-radius: 4px;
            padding: 8px;
            font-size: 16px;
            min-width: 70px;
            min-height: 70px;
        }
        QPushButton:hover {
            background: #F5F5F5;
        }
        QPushButton:checked {
            background: #007AFF;
            color: white;
            border: none;
        }
        QPushButton:pressed {
            background: #EBEBEB;
        }
    """

    # Number button style
    NUMBER_BUTTON = """
        QPushButton {
            background: white;
            border: 1px solid #DEDEDE;
            border-radius: 4px;
            padding: 8px;
            font-size: 20px;
            min-width: 70px;
            min-height: 70px;
        }
        QPushButton:hover {
            background: #F5F5F5;
        }
        QPushButton:pressed {
            background: #EBEBEB;
        }
        QPushButton:disabled {
            background: #F5F5F5;
            color: #999;
        }
    """

class NumpadConfig:
    """Configuration for numpad dimensions and layout"""
    
    # Default dimensions
    DIMENSIONS = {
        'width': 350,           # Total numpad width
        'display_height': 50,   # Height of display area
        'button_size': 70,      # Size of number buttons
        'qty_button_size': 70,  # Size of QTY button
        'spacing': 8,           # Spacing between elements
    }

    # Layout configuration
    LAYOUT = {
        'main_margins': (8, 8, 8, 8),
        'grid_margins': (0, 0, 0, 0),
        'grid_spacing': 8,
        'display_row_spacing': 8,  # Spacing between QTY button and display
    }

    @classmethod
    def get_dimensions(cls):
        """Get numpad dimensions configuration"""
        return cls.DIMENSIONS.copy()

    @classmethod
    def get_layout(cls):
        """Get numpad layout configuration"""
        return cls.LAYOUT.copy()