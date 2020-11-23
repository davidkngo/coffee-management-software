import sys
from PySide2.QtWidgets import QApplication
from core.mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
