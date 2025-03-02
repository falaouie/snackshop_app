# styles/top_bar.py
"""
Styles for the TopBar component

This module follows a clean separation of concerns where:
1. Stylesheets handle only visual appearance (colors, borders)
2. Widget methods handle sizing and font properties
3. Config values are used directly by the widget, not in the stylesheet

This approach follows Qt best practices:
- Stylesheets for colors and visual styling
- Qt methods (setFixedHeight, QFont) for dimensions and text properties
"""
class TopBarStyles:
    """Styles for top bar and related components"""
    
    @staticmethod
    def get_top_bar_container_style():
        """Get the main container style"""
        return """
            QFrame {
                background: #F0F0F0;
                border-bottom: 1px solid #DEDEDE;
            }
        """
    
    @staticmethod
    def get_employee_zone_style():
        """Get employee zone style"""
        return """
            QFrame {
                background: transparent;
                border: none;
            }
        """
    
    @staticmethod
    def get_employee_id_style():
        """Get employee ID label style"""
        return """
            QLabel {
                color: #333;
                font-weight: 500;
            }
        """
    
    @staticmethod
    def get_datetime_zone_style():
        """Get datetime zone style"""
        return """
            QFrame {
                background: transparent;
                border: none;
            }
        """
    
    @staticmethod
    def get_date_label_style():
        """Get date label style"""
        return """
            QLabel {
                color: #666;
            }
        """
    
    @staticmethod
    def get_time_label_style():
        """Get time label style"""
        return """
            QLabel {
                color: #333;
                font-weight: 500;
                padding-left: 4px;
            }
        """
    
    @staticmethod
    def get_lock_button_style():
        """Get lock button style"""
        return """
            QPushButton {
                background: transparent;
                border: none;
                padding: 0px;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 0.05);
                border-radius: 4px;
            }
        """
    
    @staticmethod
    def get_center_section_style():
        """Get center section style"""
        return """
            QFrame {
                background: transparent;
                border: none;
            }
        """