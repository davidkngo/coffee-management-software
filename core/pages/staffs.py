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
from enum import IntEnum


WidgetSignal = WidgetSignal()


class RoleEnum(IntEnum):
    ADMIN = 1
    MANANGER = 2
    STAFF = 3


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

        self.tableWidget = QTableWidget()
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'First Name', 'Last Name', 'Email', 'Role'])

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)

        
        layout = QVBoxLayout()
        layout.addWidget(self.detailWidget)
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.loadUser()

        WidgetSignal.userUpdated.connect(self.loadUser)

        self.tableWidget.cellPressed.connect(self.selectRow)


    def loadUser(self):
        userHelper = self.controllerFactory.get_controller("UserHelper")

        users = userHelper.getAllUser()

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        for row, user in enumerate(users):

            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(user.id)))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(user.firstName))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(user.lastName))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(user.email))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(RoleEnum(user.role).name))

    
    def selectRow(self, row, _):
        
        user = dict()
        
        for col in range(self.tableWidget.columnCount()):
            header = self.tableWidget.horizontalHeaderItem(col).text()
            user[header] = self.tableWidget.item(row, col).text()

        WidgetSignal.userDetailed.emit(user)

class StaffDetail(QWidget):
    def __init__(self, controllerFactory=None, parent=None):
        super(StaffDetail, self).__init__(parent)

        self.controllerFactory = controllerFactory

        styleSheet = loadStyleSheet("assets/qss/itemdetail.qss")
        self.setStyleSheet(styleSheet)

        self.idLabel = QLabel('ID')
        self.idField = QLabel()

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

        self.saveBtn = QPushButton('Save')
        self.saveBtn.clicked.connect(self.saveUser)

        btnLayout = QVBoxLayout()
        btnLayout.addWidget(self.saveBtn)

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addLayout(fieldLayout, 0, 1, rowSpan=2)
        layout.addLayout(btnLayout, 0, 2, rowSpan=2)
        self.setLayout(layout)

        WidgetSignal.userDetailed.connect(self.getDetailUser)

    def saveUser(self):
        userHelper = self.controllerFactory.get_controller(key="UserHelper")

        userHelper.createUser(name=self.usernameField.text(), lastname=self.lastnameField.text(),
         email=self.emailField.text(), role=RoleEnum[self.roleField.text().upper()].value)

        WidgetSignal.userUpdated.emit()

    
    def getDetailUser(self, user):
        self.idField.setText(user['ID'])
        self.usernameField.setText(user['First Name'])
        self.lastnameField.setText(user['Last Name'])
        self.emailField.setText(user['Email'])
        self.roleField.setText(user['Role'])

