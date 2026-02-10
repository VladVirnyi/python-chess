from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QListWidget
from PySide6.QtCore import Qt
import chess


class HistoryPanel(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(0, 2, parent)

        self.setHorizontalHeaderLabels(["White", "Black"])
        self.verticalHeader().setVisible(False)

        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionMode(QTableWidget.NoSelection)

        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        self.setFixedWidth(220)

    def update_history(self, board: chess.Board):
        self.setRowCount(0)

        moves = board.move_stack

        self.san_moves = QListWidget() # pyside for better styles
        list_layout = QHBoxLayout()
        list_layout.addStretch()
        list_layout.addWidget(self.san_moves)
        list_layout.addStretch()
        list_layout.setAlignment(Qt.AlignCenter)


        temp_board = chess.Board()
        for move in moves:
            self.san_moves.addItem(temp_board.san(move))
            temp_board.push(move)

        for i in range(0, self.san_moves.count(), 2):
            row = self.rowCount()
            self.insertRow(row)

            white_item = QTableWidgetItem(self.san_moves.item(i).text())
            white_item.setTextAlignment(Qt.AlignLeft)

            self.setItem(row, 0, white_item)

            if i + 1 < self.san_moves.count():
                black_item = QTableWidgetItem(self.san_moves.item(i + 1).text())
                black_item.setTextAlignment(Qt.AlignRight)
                self.setItem(row, 1, black_item)
