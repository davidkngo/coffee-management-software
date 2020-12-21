import os
from pathlib import Path
from shutil import copyfile

from PySide2.QtCore import Signal, Qt, QSize, QRect
from PySide2.QtGui import QPixmap, QResizeEvent, QPaintEvent, QPainterPath, QPainter
from PySide2.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QVBoxLayout, QGraphicsDropShadowEffect, \
    QHBoxLayout, QTableWidget, QSpacerItem, QSizePolicy, QHeaderView, QTableWidgetItem, QLineEdit, QFileDialog, QScrollArea

from core.utils import loadStyleSheet
from core.widgets.comps import SpinBox
from datetime import date
from core.signals import WidgetSignal

WidgetSignal = WidgetSignal()

class LoginPage(QWidget):
    def __init__(self, controllerFactory=None, parent=None):
        super(LoginPage, self).__init__(parent)

        self.controllerFactory = controllerFactory

        self.loginBox = FDLoginBox(self.controllerFactory)

        # scrollArea = QScrollArea(self)
        # scrollArea.setWidget(self.loginBox)
        # scrollArea.setWidgetResizable(True)
        # scrollArea.setMinimumWidth(840)
        # scrollArea.setMaximumWidth(1330)

        layout = QHBoxLayout()
        layout.addWidget(self.loginBox)

        self.setLayout(layout)

        self.connectOrdered()

        WidgetSignal.fdItemUpdated.connect(self.connectOrdered)

class FDLoginBox(QWidget):
    def __init__(self, parent=None):
        super(FDLoginBox, self).__init__(parent)
        styleSheet = loadStyleSheet('assets/qss/loginbox.qss')
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setStyleSheet(styleSheet)
        self.setFixedSize(QSize(500, 250))

        self.userid = QLabel()
        self.userid.setAlignment(Qt.AlignVCenter)
        self.userid.setText("User ID")
        self.useridField = QLineEdit()

        self.username = QLabel()
        self.username.setAlignment(Qt.AlignVCenter)
        self.username.setText("User Name")
        self.usernameField = QLineEdit()

        self.role = QLabel()
        self.role.setAlignment(Qt.AlignVCenter)
        self.role.setText("Role")
        self.roleField = QLineEdit()

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(10)
        layout.addWidget(self.userid, 1, 0)
        layout.addWidget(self.useridField, 1, 1)

        layout.addWidget(self.username, 2, 0)
        layout.addWidget(self.usernameField, 2, 1)

        layout.addWidget(self.role, 3, 0)
        layout.addWidget(self.roleField, 3, 1)

        self.loginBtn = QPushButton('Login')
        self.loginBtn.clicked.connect(self.login)

        self.setLayout(layout)

        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setBlurRadius(20)
        shadowEffect.setXOffset(0)
        shadowEffect.setColor(Qt.black)

        self.setGraphicsEffect(shadowEffect)

    def login(self, id, name, role):
        userHelper = self.controllerFactory.get_controller(key="UserHelper")

        userHelper.login(id, name, role)
        # ... to be continued

class StaffPage(QWidget):
    def __init__(self, controllerFactory=None, parent=None):
        super(StaffPage, self).__init__(parent)

        self.controllerFactory = controllerFactory

        self.detailWidget = StaffDetail(controllerFactory=self.controllerFactory)

        layout = QVBoxLayout()
        layout.addWidget(self.detailWidget)
        self.setLayout(layout)

class StaffDetail(QWidget):
    def __init__(self, controllerFactory=None, parent=None):
        super(StaffDetail, self).__init__(parent)

        self.controllerFactory = controllerFactory

        styleSheet = loadStyleSheet("assets/qss/itemdetail.qss")
        self.setStyleSheet(styleSheet)

        self.idLabel = QLabel('ID')
        self.idField = QLineEdit()

        self.usernameLabel = QLabel('User First Name')
        self.usernameField = QLineEdit()

        self.lastnameLabel = QLabel('User Last Name')
        self.lastnameField = QLineEdit()

        self.emailLabel = QLabel('Email')
        self.emailField = QLineEdit()

        self.roleLabel = QLabel('Role')
        self.roleField = QLineEdit()

        fieldLayout = QGridLayout()
        fieldLayout.addWidget(self.idLabel, 0, 0)
        fieldLayout.addWidget(self.idField, 0, 1)

        fieldLayout.addWidget(self.usernameLabel, 1, 0)
        fieldLayout.addWidget(self.usernameField, 1, 1)

        fieldLayout.addWidget(self.lastnameLabel, 1, 2)
        fieldLayout.addWidget(self.lastnameField, 1, 3)

        fieldLayout.addWidget(self.emailLabel, 2, 0)
        fieldLayout.addWidget(self.emailField, 2, 1)

        fieldLayout.addWidget(self.roleLabel, 2, 2)
        fieldLayout.addWidget(self.roleField, 2, 3)

        self.imageThumbnail = QLabel()
        self.imageThumbnail.setObjectName('imageThumbnail')
        self.imageThumbnail.setFixedSize(QSize(250, 250))

        self.imageUrl = None

        self.browseBtn = QPushButton('Browse')
        self.browseBtn.setObjectName('browseBtn')
        self.browseBtn.setFixedWidth(250)
        self.browseBtn.clicked.connect(self.browseImage)

        self.saveBtn = QPushButton('Save')
        self.saveBtn.clicked.connect(self.saveUser)

        btnLayout = QVBoxLayout()
        btnLayout.addWidget(self.saveBtn)

        self.imageDialog = QFileDialog(self, caption="Open Image", filter="Image Files (*.png *.jpg *.jpeg *.bmp)")

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(self.imageThumbnail, 0, 0, rowSpan=2, alignment=Qt.AlignCenter)
        layout.addWidget(self.browseBtn, 0, 0, rowSpan=2, alignment=Qt.AlignHCenter | Qt.AlignBottom)
        layout.addLayout(fieldLayout, 0, 2, rowSpan=2)
        layout.addLayout(btnLayout, 0, 3, rowSpan=2)
        self.setLayout(layout)

    def browseImage(self):

        try:
            filePath = Path(self.imageDialog.getOpenFileName()[0])

            self.imageUrl = filePath

            self.imageThumbnail.setPixmap(QPixmap(str(self.imageUrl)))
            self.imageThumbnail.setScaledContents(True)

        except IsADirectoryError as e:
            print(e)

    def saveUser(self):
        userHelper = self.controllerFactory.get_controller(key="UserHelper")

        userHelper.editUser(self.usernameField.text(), self.lastnameField.text(), self.emailField.text())

