from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QStackedWidget, QGridLayout, QPushButton, QLabel

from core.utils import loadStyleSheet


class PageManager(QWidget):
    def __init__(self, parent=None, pageLabel=''):
        super(PageManager, self).__init__(parent)
        styleSheet = loadStyleSheet('assets/qss/pagemanager.qss')
        self.setStyleSheet(styleSheet)

        self.pageLabel = QLabel(pageLabel)

        self.backBtn = QPushButton()
        self.backBtn.setIcon(QIcon('assets/icons/back-button.png'))
        self.backBtn.setFixedSize(QSize(60, 60))

        self.stackedWidget = QStackedWidget()

        layout = QGridLayout()
        layout.addWidget(self.backBtn, 0, 0)
        layout.addWidget(self.pageLabel, 0, 1)
        layout.addWidget(self.stackedWidget, 1, 0, 1, 0)

        self.setLayout(layout)

    def addPage(self, page: QWidget):
        self.stackedWidget.addWidget(page)

    def gotoPage(self):
        pass

    def goBack(self):
        pass
