from PySide2.QtCore import Qt, QEvent, QVariantAnimation, QEasingCurve, Signal
from PySide2.QtGui import QIcon, QCursor, QResizeEvent, QPaintEvent, QPainter, QPixmap, QImage
from PySide2.QtWidgets import QWidget, QPushButton, QListWidget, QVBoxLayout, QListWidgetItem

from core.utils import loadStyleSheet


class SideButton(QPushButton):

    def __init__(self, parent=None, content=''):
        super(SideButton, self).__init__(parent)
        styleSheet = loadStyleSheet('assets/qss/sidebutton.qss')
        self.setStyleSheet(styleSheet)
        self.content = content
        self.setText(self.content)
        self.pixmap = QPixmap()

    def setPixmap(self, image: QImage):
        self.pixmap = self.pixmap.fromImage(image)
        self.pixmap = self.pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.FastTransformation)

    def resizeEvent(self, event: QResizeEvent):
        if event.size().width() <= 150:
            self.setText('')
        else:
            self.setText(self.content)

    def paintEvent(self, event: QPaintEvent):
        super(SideButton, self).paintEvent(event)
        painter = QPainter(self)
        if not self.pixmap.isNull():
            x = self.pixmap.width() // 2
            painter.drawPixmap(x, 0, self.pixmap)
        painter.end()


class SidePane(QWidget):
    selectionChanged = Signal(int)

    def __init__(self, parent=None):
        super(SidePane, self).__init__(parent=parent)
        styleSheet = loadStyleSheet('assets/qss/sidepane.qss')
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(styleSheet)
        self.setFixedWidth(250)

        self.expandBtn = QPushButton()
        self.expandBtn.setIcon(QIcon('assets/icons/menu.png'))
        self.expandBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.expandBtn.setFixedWidth(60)
        self.expandBtn.setFixedHeight(60)

        self.expandBtn.clicked.connect(self.resizeAnimation)

        self.listWidget = QListWidget()
        self.listWidget.horizontalScrollBar().hide()
        self.listWidget.verticalScrollBar().hide()
        self.listWidget.currentRowChanged.connect(self.changeSelection)

        layout = QVBoxLayout()

        layout.addWidget(self.expandBtn, 0)
        layout.addWidget(self.listWidget, 1)

        self.setLayout(layout)

        self.expandAnimation = QVariantAnimation(self)
        self.expandAnimation.setDuration(500)
        self.expandAnimation.setEasingCurve(QEasingCurve.InOutQuad)

        self._is_expanded = True

    def resizeAnimation(self):
        if self._is_expanded:
            self.expandAnimation.setStartValue(250)
            self.expandAnimation.setEndValue(80)
        else:
            self.expandAnimation.setStartValue(80)
            self.expandAnimation.setEndValue(250)

        self.expandAnimation.valueChanged.connect(self.changeWidth)
        self.expandAnimation.start()

        self._is_expanded = not self._is_expanded

    def changeSelection(self, selected):
        self.selectionChanged.emit(selected)

    def changeWidth(self, value):
        self.setFixedWidth(value)

    def addSideButton(self, button: QPushButton):
        item = QListWidgetItem()
        self.listWidget.insertItem(self.listWidget.count(), item)
        self.listWidget.setItemWidget(item, button)
        item.setSizeHint(button.sizeHint())
