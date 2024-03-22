import time

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot

from ui.MainWindow import MainWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window = MainWindow()
        uic.loadUi("ui/LoginWindow.ui", self)
        self.fio = ''
        self.group = ''
        self.start_time = ''

        self.startButton.clicked.connect(self.start_handler)

    def start_handler(self):
        self.fio = self.fioLine.text()
        self.group = self.groupLine.text()

        self.start_time = time.time()

        self.close()
        self.main_window.show()

