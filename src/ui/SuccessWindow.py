from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QDialog


class SuccessWindow(QDialog):
    exitSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/SuccessWindow.ui", self)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.finishButton.clicked.connect(self.exit_handler)

    def exit_handler(self):
        self.exitSignal.emit('O')
