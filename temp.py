def _create_qwerty_section(self):
    qwerty_widget = QWidget()
    qwerty_layout = QGridLayout(qwerty_widget)
    qwerty_layout.setSpacing(10)

    qwerty_rows = [
        list('QWERTYUIOP'),  # 10 letters
        list('ASDFGHJKL'),   # 9 letters
        list('ZXCVBNM')      # 7 letters
    ]

    self.key_button_styles = """
        QPushButton {
            background: white;
            border: 1px solid #DEDEDE;
            border-radius: 10px;
            padding: 8px;
            color: #333;
            font-size: 18px;
        }
        QPushButton:hover {
            background: #F8F9FA;
            border-color: #2196F3;
        }
    """

    for row, letters in enumerate(qwerty_rows):
        # Calculate offset for each row to center it
        offset = (10 - len(letters)) // 2  # Using 10 (length of first row) as reference
        for col, letter in enumerate(letters):
            btn = QPushButton(letter)
            btn.setFixedSize(50, 50)
            btn.setStyleSheet(self.key_button_styles)
            btn.clicked.connect(lambda checked, l=letter: self._on_key_press(l))
            qwerty_layout.addWidget(btn, row, col + offset)

    return qwerty_widget