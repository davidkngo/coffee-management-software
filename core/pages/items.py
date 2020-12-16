import os
from pathlib import Path
from shutil import copyfile

from PySide2.QtCore import Signal, Qt, QSize, QRect, QFileInfo, QFile
from PySide2.QtGui import QPixmap, QResizeEvent, QPaintEvent, QPainterPath, QPainter
from PySide2.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QVBoxLayout, QGraphicsDropShadowEffect, \
    QHBoxLayout, QTableWidget, QSpacerItem, QSizePolicy, QHeaderView, QTableWidgetItem, QSpinBox, QLineEdit, QFileDialog

from core.utils import loadStyleSheet
from core.widgets.comps import SpinBox
from core.controllers.OrderController import OrderController
from core.controllers.ControllerFactory import ControllerFactory


class HomePage(QWidget):
    def __init__(self, parent=None):
        super(HomePage, self).__init__(parent)

        self.orderWidget = FDItemOrderWidget()
        self.itemGrid = FDItemGridWidget()

        for item in self.itemGrid.items:
            item.orderedItem.connect(self.orderWidget.addItem)

        layout = QHBoxLayout()
        layout.addWidget(self.itemGrid)
        layout.addWidget(self.orderWidget)

        self.setLayout(layout)


class ItemPage(QWidget):
    def __init__(self, parent=None):
        super(ItemPage, self).__init__(parent)

        self.detailWidget = FDItemDetail()

        layout = QVBoxLayout()
        layout.addWidget(self.detailWidget)

        self.setLayout(layout)


class FDItemImage(QLabel):
    def __init__(self, parent=None):
        super(FDItemImage, self).__init__(parent)

    def paintEvent(self, event: QPaintEvent):
        super(FDItemImage, self).paintEvent(event)


class FDItemWidget(QWidget):
    orderClicked = Signal(bool)
    orderedItem = Signal(str, str)

    def __init__(self, parent=None):
        super(FDItemWidget, self).__init__(parent)
        styleSheet = loadStyleSheet('assets/qss/fooddrinkitem.qss')
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setStyleSheet(styleSheet)
        self.setFixedSize(QSize(250, 250))
        self.image = FDItemImage()
        self.image.setScaledContents(True)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter)

        self.price = QLabel()
        self.price.setAlignment(Qt.AlignHCenter)

        self.orderBtn = QPushButton()
        self.orderBtn.clicked.connect(self.emitItem)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(10)
        layout.addWidget(self.image, 0, 0)
        layout.addWidget(self.label, 1, 0)
        layout.addWidget(self.orderBtn, 2, 0, Qt.AlignHCenter)
        self.setLayout(layout)

        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setBlurRadius(20)
        shadowEffect.setXOffset(0)
        shadowEffect.setColor(Qt.black)

        self.setGraphicsEffect(shadowEffect)

    def setPrice(self, price):
        self.price.setText(price)

    def setLabel(self, label):
        self.label.setText(label)

    def setPixmap(self, pixmap: QPixmap):
        p = pixmap.scaled(QSize(1000, 1000))
        rect = p.rect()
        target = QPixmap(p.size())
        target.fill(Qt.transparent)
        painter = QPainter(target)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRoundedRect(rect, 80, 80)
        path.addRect(QRect(rect.left(), rect.bottom() - 100, 100, 100))
        path.addRect(QRect(rect.right() - 100, rect.bottom() - 100, 100, 100))

        painter.drawPath(path.simplified())
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        painter.end()

        self.image.setPixmap(target)

    def emitItem(self):
        self.orderedItem.emit(self.label.text(), self.price.text())

    @staticmethod
    def createInstance(imageUrl, name, price):
        instance = FDItemWidget()
        instance.setPixmap(QPixmap(imageUrl))
        instance.setLabel(name)
        instance.setPrice(price)
        instance.orderBtn.setText(price)

        return instance


class FDItemOrderWidget(QWidget):
    def __init__(self, parent=None):
        super(FDItemOrderWidget, self).__init__(parent)
        styleSheet = loadStyleSheet("assets/qss/ordertable.qss")
        self.setStyleSheet(styleSheet)
        self.setFixedWidth(300)

        self.tableWidget = QTableWidget()
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Item', 'Quantity', 'Price'])

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        self.btnGroupLayout = QHBoxLayout()
        self.btnGroupLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.printBtn = QPushButton('Print')
        self.cancelBtn = QPushButton('Cancel')
        self.cancelBtn.clicked.connect(self.cancelOrder)
        self.btnGroupLayout.addWidget(self.cancelBtn)
        self.btnGroupLayout.addWidget(self.printBtn)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addLayout(self.btnGroupLayout)
        self.setLayout(layout)

    def cancelOrder(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

    def addItem(self, label, price):
        existedItems = self.tableWidget.findItems(label, Qt.MatchExactly)

        if len(existedItems) == 0:
            numRows = self.tableWidget.rowCount()
            self.tableWidget.insertRow(numRows)
            self.tableWidget.setItem(numRows, 0, QTableWidgetItem(label))
            self.tableWidget.setItem(numRows, 2, QTableWidgetItem(price))

            spinBox = SpinBox(self.tableWidget)
            spinBox.setAlignment(Qt.AlignCenter)
            spinBox.setMinimum(1)
            spinBox.onValueChanged.connect(self.updateQuantity)
            self.tableWidget.setCellWidget(numRows, 1, spinBox)

    def updateQuantity(self, oldValue, newValue):
        row = self.tableWidget.currentRow()
        item = self.tableWidget.item(row, 2)
        updatedPrice = "%0.2f" % (float(item.text()) / oldValue * newValue)
        item.setText(updatedPrice)


class FDItemGridWidget(QWidget):
    def __init__(self, parent=None):
        super(FDItemGridWidget, self).__init__(parent)

        self.items = []

        self.item = FDItemWidget.createInstance("assets/img/coffee1.jpg", "Cappuchino", "29.99")
        self.items.append(self.item)

        self.item = FDItemWidget.createInstance("assets/img/coffee2.jpg", "Cappuchino1", "29.99")
        self.items.append(self.item)

        self.item = FDItemWidget.createInstance("assets/img/coffee3.jpg", "Cappuchino2", "29.99")
        self.items.append(self.item)

        self.item = FDItemWidget.createInstance("assets/img/coffee4.jpeg", "Cappuchino3", "29.99")
        self.items.append(self.item)

        layout = QGridLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.setLayout(layout)

        self.arrangeItems()

    def arrangeItems(self):
        layout = self.layout()
        rowCounter = 0
        MaxCol = self.width() // 250
        for idx, i in enumerate(self.items):
            layout.addWidget(i, rowCounter, idx % MaxCol)

            if idx % MaxCol == MaxCol - 1:
                rowCounter += 1

    def resizeEvent(self, event: QResizeEvent):
        super(FDItemGridWidget, self).resizeEvent(event)
        self.arrangeItems()


class FDItemDetail(QWidget):
    def __init__(self, ctrlFactory=None, parent=None):
        super(FDItemDetail, self).__init__(parent)

        self.ctrlFactory = ctrlFactory

        styleSheet = loadStyleSheet("assets/qss/itemdetail.qss")
        self.setStyleSheet(styleSheet)

        self.nameLabel = QLabel('Name')
        self.nameField = QLineEdit()

        self.priceLabel = QLabel('Price')
        self.priceField = QLineEdit()

        fieldLayout = QVBoxLayout()
        fieldLayout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        fieldLayout.addWidget(self.nameLabel)
        fieldLayout.addWidget(self.nameField)
        fieldLayout.addWidget(self.priceLabel)
        fieldLayout.addWidget(self.priceField)

        self.imageThumbnail = QLabel()
        self.imageThumbnail.setObjectName('imageThumbnail')
        self.imageThumbnail.setFixedSize(QSize(250, 250))

        self.imageUrl = None

        self.browseBtn = QPushButton('Browse')
        self.browseBtn.setObjectName('browseBtn')
        self.browseBtn.setFixedWidth(250)
        self.browseBtn.clicked.connect(self.browseImage)

        self.newBtn = QPushButton('New')
        self.newBtn.clicked.connect(self.initNew)

        self.deleteBtn = QPushButton('Delete')
        self.editBtn = QPushButton('Edit')
        self.saveBtn = QPushButton('Save')

        btnLayout = QVBoxLayout()
        btnLayout.addWidget(self.newBtn)
        btnLayout.addWidget(self.deleteBtn)
        btnLayout.addWidget(self.editBtn)
        btnLayout.addWidget(self.saveBtn)

        self.imageDialog = QFileDialog(self, caption="Open Image", filter="Image Files (*.png *.jpg *.jpeg *.bmp)")

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(self.imageThumbnail, 0, 0, rowSpan=2, alignment=Qt.AlignCenter)
        layout.addWidget(self.browseBtn, 0, 0, rowSpan=2, alignment=Qt.AlignHCenter | Qt.AlignBottom)
        layout.addLayout(fieldLayout, 0, 2, rowSpan=2)
        layout.addLayout(btnLayout, 0, 3, rowSpan=2)
        self.setLayout(layout)

    def initNew(self):
        self.imageThumbnail.clear()
        self.nameField.clear()
        self.priceField.clear()


    def saveItem(self):
        
        desPath = os.path.join("assets/img", self.imageUrl.name)
        copyfile(str(self.imageUrl), desPath)

    def browseImage(self):

        try:
            filePath = Path(self.imageDialog.getOpenFileName()[0])

            self.imageUrl = filePath

            self.imageThumbnail.setPixmap(QPixmap(str(self.imageUrl)))
            self.imageThumbnail.setScaledContents(True)

        except IsADirectoryError as e:
            print(e)
