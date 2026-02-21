from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class IconButton(QPushButton): # parent button
    def __init__(self, icon_path, tooltip="", checkable=False):
        super().__init__()

        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(20, 20))
        self.setFixedSize(120, 30)

        self.setCheckable(checkable)
        self.setToolTip(tooltip)

class HistoryButton(IconButton): # button for history panel
    def __init__(self, parent=None):
        super().__init__(
            icon_path="assets/history_icon.png",
            tooltip="Show/hide moves history panel",
            checkable=True
        )
        self.setObjectName("historyButton")

class MicroModeButton(IconButton): # button for micro mode, no history panel.
    def __init__(self, parent):
        super().__init__(
            icon_path="assets/icons/micro.svg",
            tooltip="Micro mode",
            checkable=True
        )
        self.clicked.connect(parent.toggle_micro_mode)
