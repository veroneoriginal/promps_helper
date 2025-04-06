# pylint: disable=E0611: no-name-in-module
import sys

from PyQt6.QtWidgets import QApplication

from UI.main import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
