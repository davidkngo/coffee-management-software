from PySide2.QtCore import Signal, Qt, QSize, QRect
from PySide2.QtGui import QPixmap, QResizeEvent, QPaintEvent, QPainterPath, QPainter
from PySide2.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QVBoxLayout, QGraphicsDropShadowEffect, \
    QTableView, QButtonGroup

from core.pages.pagemanager import PageManager
from core.utils import loadStyleSheet


class HomePage(PageManager):
    def __init__(self, parent=None, pageLabel=''):
        super(HomePage, self).__init__(parent, pageLabel)
        self.mainPage = FDItemPage()
        self.detailPage = FDDetailPage()

        self.addPage(self.mainPage)
        self.addPage(self.detailPage)

        for i in self.mainPage.items:
            i.detailedItem.connect(self.detailPage.detailedItemChanged)


class FDItemImage(QLabel):
    def __init__(self, parent=None):
        super(FDItemImage, self).__init__(parent)

    def paintEvent(self, event: QPaintEvent):
        super(FDItemImage, self).paintEvent(event)


class FDItemWidget(QWidget):
    orderClicked = Signal(bool)
    detailedItem = Signal(dict)

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
        self.detailBtn = QPushButton('Detail')
        self.detailBtn.clicked.connect(self.emitItem)

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
        rect = pixmap.rect()
        target = QPixmap(pixmap.size())
        target.fill(Qt.transparent)
        painter = QPainter(target)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRoundedRect(pixmap.rect(), 80, 80)
        path.addRect(QRect(rect.left(), rect.bottom() - 100, 100, 100))
        path.addRect(QRect(rect.right() - 100, rect.bottom() - 100, 100, 100))

        painter.drawPath(path.simplified())
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        self.image.setPixmap(target)

    def emitItem(self):
        item = {
            'label': self.label.text(),
            'price': self.price.text(),
        }

        self.detailedItem.emit(item)

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

        self.tableView = QTableView()

        self.btnGroup = QButtonGroup()

        layout = QVBoxLayout()
        layout.addWidget(self.tableView)
        layout.addWidget(self.btnGroup)


class FDItemPage(QWidget):
    def __init__(self, parent=None):
        super(FDItemPage, self).__init__(parent)

        self.items = []

        self.item = FDItemWidget.createInstance("assets/img/coffee1.jpg", "Cappuchino", "$29.99")
        self.items.append(self.item)

        self.item = FDItemWidget.createInstance("assets/img/coffee1.jpg", "Cappuchino", "$29.99")
        self.items.append(self.item)

        self.item = FDItemWidget.createInstance("assets/img/coffee1.jpg", "Cappuchino", "$29.99")
        self.items.append(self.item)

        self.item = FDItemWidget.createInstance("assets/img/coffee1.jpg", "Cappuchino", "$29.99")
        self.items.append(self.item)

        layout = QGridLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setLayout(layout)

        self.arrangeItems()

    def arrangeItems(self):
        layout = self.layout()
        rowCounter = 0
        MaxCol = self.width() // 200
        for idx, i in enumerate(self.items):
            layout.addWidget(i, rowCounter, idx % MaxCol)

            if idx % MaxCol == MaxCol - 1:
                rowCounter += 1

    def resizeEvent(self, event: QResizeEvent):
        super(FDItemPage, self).resizeEvent(event)
        self.arrangeItems()


class FDDetailPage(QWidget):
    detailedItem = Signal(dict)

    def __init__(self, parent=None):
        super(FDDetailPage, self).__init__(parent)

    def detailedItemChanged(self, value):
        print(value)
