from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QDialog


class FailureWindow(QDialog):
    exitSignal = pyqtSignal(str)
    retrySignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/FailureWindow.ui", self)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.exitButton.clicked.connect(self.exit_handler)
        # self.retryButton.clicked.connect(self.retry_handler)

    def exit_handler(self):
        self.exitSignal.emit('O')

    def retry_handler(self):
        self.retrySignal.emit('')
