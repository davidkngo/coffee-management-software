from PySide2.QtCore import Signal
from PySide2.QtWidgets import QSpinBox

from core.utils import loadStyleSheet


class SpinBox(QSpinBox):

    onValueChanged = Signal(int, int)

    def __init__(self, parent):
        super(SpinBox, self).__init__(parent)
        styleSheet = loadStyleSheet("assets/qss/spinbox.qss")
        self.setStyleSheet(styleSheet)
        self.preValue = None
        self.valueChanged.connect(self.getValueChanged)

    def getValueChanged(self, newValue):
        self.onValueChanged.emit(self.preValue, newValue)
        self.preValue = newValue
