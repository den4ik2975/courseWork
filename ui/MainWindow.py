from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from ui.GraphWindow import GraphWindow
from database import crud
from utils.helper_functions import answers_parser, hasse_parser
from utils.picture_generator import ImageGenerator


class MainWindow(QMainWindow):
    failureSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.variant = crud.get_random_variant()
        self.picture_generator = ImageGenerator(hasse_parser(self.variant.connections), self.variant.start, self.variant.end)
        self.graph_window = GraphWindow(self.variant)

        uic.loadUi("ui/MainWindow.ui", self)
        self.current_action = ''

        self.graph_window.saveSignal.connect(self.handle_signal)

        for key, value in self.__dict__.items():
            if 'Button' in key and 'end' not in key:
                name = key[:-6]
                getattr(self, key).clicked.connect(self.click_handler)
                self.current_action = name

        self.picture_generator.generate_image().save('resources/temp/graph.png')
        self.image.setPixmap(QPixmap('resources/temp/graph.png'))




    @pyqtSlot(str)
    def handle_signal(self, data):
        getattr(self, self.current_action).setText(f'{data}')

        user_answer = [i for i in data.split(', ')]
        if user_answer == ['∅']: user_answer = ['Z']

        if self.current_action in ['maxes', 'mins', 'largest', 'smallest']:
            user_answer = set(user_answer)

        task_answer = answers_parser(self.variant.answers, self.current_action)

        if task_answer != user_answer:
            self.graph_window.close()
            getattr(self, self.current_action).setStyleSheet("QLabel { background-color: #F1506B; color: #0b392c; padding-left: 10px; border-radius: 6px;}")
            self.failureSignal.emit(self.current_action)

        else:
            getattr(self, self.current_action).setStyleSheet("QLabel { background-color: #67E667; color: #0b392c; padding-left: 10px; border-radius: 6px;}")

    def click_handler(self):
        sender = self.sender().objectName()[:-6]
        self.current_action = sender
        self.graph_window.exec()

    def end_choice(self):
        pass