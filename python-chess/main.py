import sys
import chess
import chess.svg # graphic board

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QInputDialog # for .svg
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



            fill[self.selected_square] = "#ffd966" # set color for square
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

        square = self.pixel_to_square(event.position().x(), event.position().y()) # get square from click position
        if square is None:
            return

        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.update_board()
        else:
            from_sq = self.selected_square
            to_sq = square
            self.selected_square = None

            if from_sq == to_sq:
                self.update_board()
                return

            # promotion logic
            is_promotion = False
            piece = self.board.piece_at(from_sq)
            if piece and piece.piece_type == chess.PAWN:
                # checking horizontal rank for promotion
                if (piece.color == chess.WHITE and chess.square_rank(to_sq) == 7) or \
                   (piece.color == chess.BLACK and chess.square_rank(to_sq) == 0):
                    if chess.Move(from_sq, to_sq, promotion=chess.QUEEN) in self.board.legal_moves:
                        is_promotion = True

            if is_promotion:
                promo_piece = self.get_promotion_piece()
                move = chess.Move(from_sq, to_sq, promotion=promo_piece)
                self.board.push(move)
            else:
                move = chess.Move(from_sq, to_sq)
                if move in self.board.legal_moves:
                    self.board.push(move)
            
            self.update_board()

    def get_promotion_piece(self): # promotion ui. For now its just new window open up. Gonna improve it.
        items = ["Queen", "Rook", "Bishop", "Knight"]
        item, ok = QInputDialog.getItem(self, "Promotion", "Select piece:", items, 0, False)
        
        mapping = {
            "Queen": chess.QUEEN,
            "Rook": chess.ROOK,
            "Bishop": chess.BISHOP,
            "Knight": chess.KNIGHT
        }

        return mapping[item] if (ok and item in mapping) else chess.QUEEN
    
    
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



