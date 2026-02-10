from PySide6.QtWidgets import QPushButton


class HistoryButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Moves history", parent)
        self.setObjectName("historyButton")
        self.setCheckable(True)
