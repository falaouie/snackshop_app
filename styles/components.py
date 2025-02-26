# styles/components.py

class SearchStyles:
    """Styles for search components"""
    
    @staticmethod
    def get_input_style(width, height):
        """Get search input style with specific dimensions
        
        Args:
            width: Width in pixels
            height: Height in pixels
        """
        return f"""
            QLineEdit {{
                border: 1px solid #DEDEDE;
                border-radius: 20px;
                padding: 8px 40px;
                font-size: 14px;
                color: #333;
                background: white;
                width: {width}px;
                height: {height}px;
            }}
            QLineEdit:focus {{
                border-color: #2196F3;
                outline: none;
            }}
        """
    
# class NumpadComponentStyles:
#     """Component-specific styles for numpad"""
    
#     @staticmethod
#     def get_container_style():
#         """Get style for the numpad container"""
#         return """
#             QFrame {
#                 background: white;
#                 border: 1px solid #DEDEDE;
#                 border-radius: 5px;
#             }
#         """
    
#     @staticmethod
#     def get_button_grid_style():
#         """Get style for the button grid container"""
#         return """
#             QFrame {
#                 background: transparent;
#                 border: none;
#             }
#         """