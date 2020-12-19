from PySide2.QtCore import Signal, QObject


class WidgetSignal(QObject):
    fdItemUpdated = Signal()
    fdItemDetailed = Signal(dict)

    def __init__(self):
        super(WidgetSignal, self).__init__(parent=None)