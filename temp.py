class SearchLineEdit(KeyboardEnabledInput):
    def __init__(self, parent=None):
        # Initialize with search type keyboard
        super().__init__(parent, style_type='search', keyboard_type=KeyboardType.FULL)
        self.parent_view = parent
        
        # Load search icon (left)
        search_icon = QSvgRenderer("assets/images/search.svg")
        self.search_pixmap = QPixmap(20, 20)
        self.search_pixmap.fill(Qt.transparent)
        painter = QPainter(self.search_pixmap)
        search_icon.render(painter)
        painter.end()
        
        # Connect text changed signal for filtering
        self.textChanged.connect(parent._filter_products)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.drawPixmap(12, (self.height() - 20) // 2, self.search_pixmap)