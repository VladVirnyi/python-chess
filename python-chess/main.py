import sys
import chess
import chess.svg # graphic board

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout # for .svg
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt

# gui idea
class ChessWidget(QWidget): 
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chess Widget")
        self.setFixedSize(420, 420)

        self.board = chess.Board()
        self.selected_square = None

        self.svg_widget = QSvgWidget()
        self.svg_widget.setFixedSize(400, 400)
        self.svg_widget.mousePressEvent = self.on_click # .svg board

        self.update_board()

        layout = QVBoxLayout()
        layout.addWidget(self.svg_widget)
        self.setLayout(layout)

    def update_board(self):
        highlight_squares = []
        fill = {}

        if self.selected_square is not None:
            for move in self.board.legal_moves:
                if move.from_square == self.selected_square:
                    highlight_squares.append(move.to_square)



            fill[self.selected_square] = "#ffd966"
            for sq in highlight_squares:
                fill[sq] = "#9fc5e8"

        svg_data = chess.svg.board(
            self.board,
            squares=highlight_squares,
            fill=fill,
            lastmove=self.board.peek() if self.board.move_stack else None
        )

        self.svg_widget.load(bytearray(svg_data, encoding="utf-8"))
        self.update_status()

    def update_status(self):
        if self.board.is_checkmate():
            self.setWindowTitle("Checkmate")
        elif self.board.is_stalemate():
            self.setWindowTitle("Stalemate")
        elif self.board.is_check():
            self.setWindowTitle("Check")
        else:
            turn = "White" if self.board.turn == chess.WHITE else "Black"
            self.setWindowTitle(f"Turn: {turn}")

    def on_click(self, event):
        if event.button() != Qt.LeftButton:
            return

        square = self.pixel_to_square(event.position().x(), event.position().y())
        if square is None:
            return

        if self.selected_square is None:
            if self.board.piece_at(square):
                self.selected_square = square
                self.update_board()
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
            self.selected_square = None
            self.update_board()


    def pixel_to_square(self, x, y):
        size = self.svg_widget.width()
        square_size = size / 8

        file = int(x // square_size)
        rank = 7 - int(y // square_size)

        if 0 <= file <= 7 and 0 <= rank <= 7:
            return chess.square(file, rank)
        return None


app = QApplication(sys.argv) # create application
window = ChessWidget()
window.show()
sys.exit(app.exec())



