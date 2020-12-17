from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QImage
from PySide2.QtWidgets import QMainWindow, QGridLayout, QWidget, QStackedWidget

from core.pages.items import HomePage, ItemPage
from core.utils import loadStyleSheet
from core.widgets.sidepane import SideButton, SidePane
from core.controller import ControllerFactory
from core.helpers.ItemHelper import ItemHelper
from core.helpers.OrderHelper import OrderHelper

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        styleSheet = loadStyleSheet('assets/qss/mainwindow.qss')
        self.setStyleSheet(styleSheet)

        self.setMinimumSize(QSize(1366, 768))

        controllerFactory = ControllerFactory()
        controllerFactory.register_controller(ItemHelper)
        controllerFactory.register_controller(OrderHelper)
    
        self.homePages = HomePage(controllerFactory=controllerFactory)

        self.itemPages = ItemPage(controllerFactory=controllerFactory)

        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(self.homePages)
        self.stackedWidget.addWidget(self.itemPages)

        self.homeBtn = SideButton(content='Home')
        self.homeBtn.setPixmap(QImage('assets/icons/home.png'))
        self.itemBtn = SideButton(content='Items')
        self.itemBtn.setPixmap(QImage('assets/icons/shipping.png'))

        self.sidePane = SidePane()
        self.sidePane.addSideButton(self.homeBtn)
        self.sidePane.addSideButton(self.itemBtn)
        self.sidePane.selectionChanged.connect(self.changePage)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setVerticalSpacing(0)
        layout.setHorizontalSpacing(0)
        layout.addWidget(self.sidePane, 0, 0, 1, 1, Qt.AlignLeft)
        layout.addWidget(self.stackedWidget, 0, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def changePage(self, index):
        self.stackedWidget.setCurrentIndex(index)
