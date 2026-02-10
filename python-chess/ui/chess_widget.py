import chess
import chess.svg # graphic board

from PySide6.QtWidgets import QWidget, QVBoxLayout, QInputDialog, QHBoxLayout # for .svg
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt
from game.game_state import GameState
from ui.buttons import HistoryButton, MicroModeButton
from ui.history_panel import HistoryPanel


# gui idea
class ChessWidget(QWidget): 
    def __init__(self):
        super().__init__()

        self.micro_mode = False
        self.setWindowTitle("Chess Widget")
        self.setFixedSize(700, 500)

        self.selected_square = None
        self.game = GameState()

        self.svg_widget = QSvgWidget()
        self.svg_widget.setFixedSize(400, 400)
        self.svg_widget.mousePressEvent = self.on_click # .svg board
        self.history_button = HistoryButton()
        self.history_panel = HistoryPanel()
        self.history_button.toggled.connect(self.toggle_history)
        self.micro_mode_button = MicroModeButton(self)
        self.micro_mode_button.toggled.connect(self.toggle_micro_mode)

        self.update_board()

        # history button
        layoutH = QHBoxLayout()
        layoutH.addWidget(self.history_button)
        layoutH.addStretch()
        layoutH.addWidget(self.micro_mode_button)
        layoutH.addStretch()

        # chess board
        layoutV = QVBoxLayout()
        layoutV.addLayout(layoutH)
        layoutV.addWidget(self.svg_widget)

        main_layout = QHBoxLayout()
        main_layout.addLayout(layoutV)
        main_layout.addWidget(self.history_panel)
        
        self.setLayout(main_layout)

    def update_board(self):
        highlight_squares = []
        fill = {}

        if self.game.board.is_check():
            self.king_square = self.game.board.king(self.game.board.turn) # get king square for check highlight
            fill[self.king_square] = "#ff0000"

        if self.selected_square is not None:
            for move in self.game.board.legal_moves:
                if move.from_square == self.selected_square:
                    highlight_squares.append(move.to_square)



            fill[self.selected_square] = "#ffd966" # set color for square
            for sq in highlight_squares:
                fill[sq] = "#9fc5e8"

        svg_data = chess.svg.board(
            self.game.board,
            squares=highlight_squares,
            fill=fill,
            lastmove=self.game.board.peek() if self.game.board.move_stack else None
        )

        self.svg_widget.load(bytearray(svg_data, encoding="utf-8"))

        self.update_status()

    def toggle_history(self, checked):
        self.history_panel.setVisible(checked)
        self.setFixedWidth(700 if checked else 450)

    def update_status(self):
        status = self.game.status()

        if status == "Checkmate":
            self.setWindowTitle("Checkmate")
        elif status == "Stalemate":
            self.setWindowTitle("Stalemate")
        elif status == "Check":
            self.setWindowTitle("Check")
        else:
            turn = "White" if self.game.board.turn == chess.WHITE else "Black"
            self.setWindowTitle(f"Turn: {turn}")


    def on_click(self, event):
        if event.button() != Qt.LeftButton:
            return
        
        square = self.pixel_to_square(event.position().x(), event.position().y()) # get square from click position
        if square is None:
            return

        if self.selected_square is None:
            piece = self.game.board.piece_at(square)
            if piece and piece.color == self.game.board.turn:
                self.selected_square = square
                self.update_board()
            return
        else:
            from_sq = self.selected_square
            to_sq = square
            self.selected_square = None
            
            if from_sq == to_sq:
                self.update_board()
                return
        
            # promotion logic
            if self.game.is_promotion(from_sq, to_sq):
                promo = self.get_promotion_piece()
                self.game.make_move(from_sq, to_sq, promo)
            else:
                self.game.make_move(from_sq, to_sq)

            self.history_panel.update_history(self.game.board)
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

    # Micro mode. Will be improved.
    def toggle_micro_mode(self):
        self.micro_mode = not self.micro_mode
        self.apply_window_mode()

    def apply_window_mode(self):
        if self.micro_mode:
            self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )
            self.setFixedSize(360, 360)
            self.history_panel.hide()
        else:
            self.setWindowFlags(Qt.Window)
            self.setMinimumSize(900, 600)
            self.history_panel.show()

        self.show()
