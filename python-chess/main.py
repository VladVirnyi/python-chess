import sys

from PySide6.QtWidgets import QApplication
from ui.chess_widget import ChessWidget



def main():
    app = QApplication(sys.argv)
    
    try:
        with open("python-chess/style.qss", "r") as f:
            style = f.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Style file not found.")

    window = ChessWidget()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


