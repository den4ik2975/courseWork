from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from ui.GraphWindow import GraphWindow

from database import crud
from utils.helper_functions import answers_parser


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.variant = crud.get_random_variant()
        self.graph_window = GraphWindow(self.variant)

        uic.loadUi("ui/MainWindow.ui", self)
        self.current_action = ''

        self.graph_window.saveSignal.connect(self.handle_signal)

        for key, value in self.__dict__.items():
            if 'Button' in key and 'end' not in key:
                name = key[:-6]
                getattr(self, key).clicked.connect(self.click_handler)
                self.current_action = name

    @pyqtSlot(str)
    def handle_signal(self, data):
        getattr(self, self.current_action).setText(f'{data}')

        user_answer = [i for i in data.split(', ')]
        if user_answer == ['∅']: user_answer = ['Z']

        if self.current_action in ['maxes', 'mins', 'largest', 'smallest']:
            user_answer = set(user_answer)

        task_answer = answers_parser(self.variant.answers, self.current_action)

        if task_answer != user_answer:
            getattr(self, self.current_action).setStyleSheet("QLabel { background-color: #F1506B; color: #0b392c; padding-left: 10px; border-radius: 6px;}")



    def click_handler(self):
        self.current_action = self.sender().objectName()[:-6]
        self.graph_window.show()

    def end_choice(self):
        pass