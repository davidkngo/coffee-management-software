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

class StaffDetail(QWidget):
    def __init__(self, controllerFactory=None, parent=None):
