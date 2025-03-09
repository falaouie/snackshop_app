# components/common/top_bar/top_bar_widget.py
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QFont
from PyQt5.QtSvg import QSvgRenderer

from config.layouts.top_bar_layout import top_bar_layout_config
from styles.top_bar import TopBarStyles
from components.common.search_widget import KeyboardEnabledSearchWidget

class TopBarWidget(QFrame):
    """
    Standard top bar widget component used across different views.
    
    Signals:
        search_changed: Emitted when the search text changes
        lock_clicked: Emitted when the lock button is clicked
    """
    
    # Define signals
    search_changed = pyqtSignal(str)
    lock_clicked = pyqtSignal()
    
    def __init__(self, user_id=None, user_name=None, parent=None):
        """
        Initialize the top bar widget.
        
        Args:
            user_id (str, optional): Employee ID to display
            parent (QWidget, optional): Parent widget
        """
        super().__init__(parent)
        
        self.user_id = user_id
        self.user_name = user_name
        
        # Set style
        self.setStyleSheet(TopBarStyles.get_top_bar_container_style())
        
        # Explicitly set fixed height from config
        height = top_bar_layout_config.get_size('height')
        self.setFixedHeight(height)
        
        # Initialize timer for datetime updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)  # Update every second
        
        self._setup_ui()
        
        # Initial time update
        self._update_time()
    
    def _setup_ui(self):
        """Initialize the main UI structure"""
        # Get container dimensions
        container_dims = top_bar_layout_config.get_container_dimensions()
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            container_dims['padding_left'],
            container_dims['padding_top'],
            container_dims['padding_right'],
            container_dims['padding_bottom']
        )
        layout.setSpacing(container_dims['section_spacing'])
        
        # Create all sections
        emp_zone = self._create_employee_zone()
        layout.addWidget(emp_zone)
        
        # Center section with search
        center_section = self._create_center_section()
        layout.addWidget(center_section, 1)  # Stretch to fill available space
        
        # Lock button section
        controls_zone = self._create_controls_zone()
        layout.addWidget(controls_zone)
    
    def _create_employee_zone(self):
        """Create employee info section with datetime"""
        emp_config = top_bar_layout_config.get_employee_section_config()
        
        # Container
        emp_zone = QFrame()
        emp_zone.setStyleSheet(TopBarStyles.get_employee_zone_style())
        
        # Layout
        emp_layout = QHBoxLayout(emp_zone)
        emp_layout.setContentsMargins(0, 0, 0, 0)
        emp_layout.setSpacing(emp_config['spacing'])
        
        # Employee icon
        emp_icon = QLabel()
        
        # Load SVG icon
        icon_size = emp_config['icon_size']
        renderer = QSvgRenderer("assets/images/employee_icon.svg")
        pixmap = QPixmap(icon_size, icon_size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        emp_icon.setPixmap(pixmap)
        
        # Employee ID
        emp_id = QLabel(f"{self.user_name}" if self.user_name else "")
        emp_id.setStyleSheet(TopBarStyles.get_employee_id_style())
        
        # Set font size from config
        emp_font = QFont()
        emp_font.setPointSize(emp_config['font_size'])
        emp_id.setFont(emp_font)
        
        # Add employee elements
        emp_layout.addWidget(emp_icon)
        emp_layout.addWidget(emp_id)
        
        # DateTime Zone
        time_zone = self._create_datetime_zone()
        emp_layout.addWidget(time_zone)
        
        return emp_zone
    
    def _create_datetime_zone(self):
        """Create the date and time display zone"""
        datetime_config = top_bar_layout_config.get_datetime_config()
        
        # Container
        time_zone = QFrame()
        time_zone.setStyleSheet(TopBarStyles.get_datetime_zone_style())
        
        # Layout
        time_layout = QVBoxLayout(time_zone)
        padding = datetime_config['container_padding']
        time_layout.setContentsMargins(padding, padding, padding, padding)
        time_layout.setSpacing(datetime_config['container_spacing'])
        
        # Date and time labels
        self.date_label = QLabel()
        self.date_label.setStyleSheet(TopBarStyles.get_date_label_style())
        
        # Set date font size
        date_font = QFont()
        date_font.setPointSize(datetime_config['date_font_size'])
        self.date_label.setFont(date_font)
        
        self.time_label = QLabel()
        self.time_label.setStyleSheet(TopBarStyles.get_time_label_style())
        
        # Set time font size
        time_font = QFont()
        time_font.setPointSize(datetime_config['time_font_size'])
        self.time_label.setFont(time_font)
        
        time_layout.addWidget(self.date_label)
        time_layout.addWidget(self.time_label)
        
        return time_zone
    
    def _create_center_section(self):
        """Create center section with search"""
        center_config = top_bar_layout_config.get_center_section_config()
        
        # Container
        center_container = QFrame()
        center_container.setStyleSheet(TopBarStyles.get_center_section_style())
        center_container.setMinimumWidth(center_config['min_width'])
        
        # Layout
        center_layout = QHBoxLayout(center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(center_config['spacing'])
        
        # Add stretches for centering
        center_layout.addStretch(1)
        
        # Create and connect search widget
        self.search_input = KeyboardEnabledSearchWidget(self)
        self.search_input.search_changed.connect(self._on_search_changed)
        center_layout.addWidget(self.search_input)
        
        center_layout.addStretch(1)
        
        return center_container
    
    def _create_controls_zone(self):
        """Create controls zone with lock button"""
        lock_config = top_bar_layout_config.get_lock_button_config()
        
        # Container
        controls_zone = QFrame()
        controls_layout = QHBoxLayout(controls_zone)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(lock_config['padding'])
        
        # Lock button
        self.lock_btn = QPushButton()
        
        # Load SVG icon
        icon_size = lock_config['icon_size']
        renderer = QSvgRenderer("assets/images/lock_screen.svg")
        pixmap = QPixmap(icon_size, icon_size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        self.lock_btn.setIcon(QIcon(pixmap))
        self.lock_btn.setIconSize(QSize(icon_size, icon_size))
        self.lock_btn.setStyleSheet(TopBarStyles.get_lock_button_style())
        self.lock_btn.clicked.connect(self._handle_lock)
        
        controls_layout.addWidget(self.lock_btn)
        
        return controls_zone
    
    def _update_time(self):
        """Update the time display"""
        current = QDateTime.currentDateTime()
        self.date_label.setText(current.toString("dd-MM-yyyy"))
        self.time_label.setText(current.toString("h:mm AP"))
    
    def _on_search_changed(self, text):
        """Forward search signal"""
        self.search_changed.emit(text)
    
    def _handle_lock(self):
        """Handle lock button click"""
        self.lock_clicked.emit()
    
    def get_search_widget(self):
        """Get the search widget"""
        return self.search_input
    
    def clear_search(self):
        """Clear the search input"""
        self.search_input.clear()