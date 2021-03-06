from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QImage
from PySide2.QtWidgets import QMainWindow, QGridLayout, QWidget, QStackedWidget

from core.pages.items import HomePage, ItemPage
from core.pages.staffs import StaffPage, LoginPage
from core.utils import loadStyleSheet
from core.widgets.sidepane import SideButton, SidePane
from core.controller import ControllerFactory
from core.helpers.ItemHelper import ItemHelper
from core.helpers.OrderHelper import OrderHelper
from core.helpers.UserHelper import UserHelper

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        styleSheet = loadStyleSheet('assets/qss/mainwindow.qss')
        self.setStyleSheet(styleSheet)

        self.setMinimumSize(QSize(1450, 768))

        controllerFactory = ControllerFactory()
        controllerFactory.register_controller(ItemHelper)
        controllerFactory.register_controller(OrderHelper)
        controllerFactory.register_controller(UserHelper)
    
        self.homePages = HomePage(controllerFactory=controllerFactory)

        self.itemPages = ItemPage(controllerFactory=controllerFactory)

        self.staffPages = StaffPage(controllerFactory=controllerFactory)

        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(self.homePages)
        self.stackedWidget.addWidget(self.itemPages)
        self.stackedWidget.addWidget(self.staffPages)

        self.homeBtn = SideButton(content='Home')
        self.homeBtn.setPixmap(QImage('assets/icons/home.png'))
        self.itemBtn = SideButton(content='Items')
        self.itemBtn.setPixmap(QImage('assets/icons/shipping.png'))
        self.staffBtn = SideButton(content='Staff')
        self.staffBtn.setPixmap(QImage('assets/icons/user.png'))

        self.sidePane = SidePane()
        self.sidePane.addSideButton(self.homeBtn)
        self.sidePane.addSideButton(self.itemBtn)
        self.sidePane.addSideButton(self.staffBtn)
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
