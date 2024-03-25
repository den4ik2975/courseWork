from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import pyqtSlot, pyqtSignal


class FailureWindow(QDialog):
    exitSignal = pyqtSignal(str)
    retrySignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/FailureWindow.ui", self)
        self.exitButton.clicked.connect(self.exit_handler)
        self.retryButton.clicked.connect(self.retry_handler)

    def exit_handler(self):
        self.exitSignal.emit('O')

    def retry_handler(self):
        self.retrySignal.emit('')