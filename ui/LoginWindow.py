from datetime import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot

from ui.MainWindow import MainWindow
from ui.SuccessWindow import SuccessWindow
from ui.FailureWindow import FailureWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window = MainWindow()
        self.success_window = SuccessWindow()
        self.failure_window = FailureWindow()
        uic.loadUi("ui/LoginWindow.ui", self)

        self.fio = ''
        self.group = ''
        self.start_time = ''

        self.startButton.clicked.connect(self.start_handler)

        self.success_window.exitSignal.connect(self.exit_handler)
        self.failure_window.exitSignal.connect(self.exit_handler)
        self.main_window.failureSignal.connect(self.failure_handler)

    def start_handler(self):
        self.fio = self.fioLine.text()
        self.group = self.groupLine.text()

        self.start_time = datetime.now()

        self.close()
        self.main_window.show()

    @pyqtSlot(str)
    def failure_handler(self, data):
        self.failure_window.exec()

    @pyqtSlot(str)
    def success_handler(self, data):
        end_time = datetime.now()
        delta = end_time - self.start_time

        stringified_end = end_time.strftime('%m.%d %H:%M:%S')
        stringified_delta = delta.strftime('%H.%M.%S')

        self.success_window.fioLabel.setText(self.fio)
        self.success_window.groupLabel.setText(self.group)
        self.success_window.endLabel.setText(stringified_end)
        self.success_window.timeLabel.setText(stringified_delta)

    @pyqtSlot(str)
    def exit_handler(self, data):
        self.main_window.close()
        self.success_window.close()
        self.failure_window.close()



