import sys

from PySide6.QtWidgets import QApplication
from ui.chess_widget import ChessWidget


app = QApplication(sys.argv) # create application
window = ChessWidget()
window.show()
sys.exit(app.exec())

if __name__ == "__main__":
    main()


