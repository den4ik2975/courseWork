from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt


class HelpWindow(QDialog):
    closeHelpSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/HelpWindow.ui", self)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.closeButton.clicked.connect(self.close_handler)

    def close_handler(self):
        self.closeHelpSignal.emit('O')