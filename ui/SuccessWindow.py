from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import pyqtSlot, pyqtSignal


class SuccessWindow(QDialog):
    exitSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/SuccessWindow.ui", self)
        self.finishButton.clicked.connect(self.exit_handler)

    def exit_handler(self):
        self.exitSignal.emit('O')