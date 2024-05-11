import copy

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow

from src.database import crud
from src.ui.GraphPairWindow import GraphPairWindow
from src.ui.GraphWindow import GraphWindow
from src.ui.HelpWindow import HelpWindow
from src.utils.helper_functions import answers_parser, hasse_parser, humanizer, linear_checker, pair_checker
from src.utils.picture_generator import ImageGenerator


class MainWindow(QMainWindow):
    failureSignal = pyqtSignal(str)
    successSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.variant = crud.get_random_variant()
        self.picture_generator = ImageGenerator(hasse_parser(self.variant.connections), self.variant.start,
                                                self.variant.end)
        self.graph_window = GraphWindow(self.variant)
        self.graph_pair_window = GraphPairWindow(self.variant)
        self.help_window = HelpWindow()

        uic.loadUi("src/ui/MainWindow.ui", self)
        self.current_action = ''
        self.answer_counter = {'maxes': 0, 'mins': 0, 'largest': 0, 'smallest': 0, 'section': 0, 'revsection': 0,
                               'linear': 0, 'pair': 0}

        self.graph_window.saveSignal.connect(self.handle_signal)
        self.graph_pair_window.saveSignal.connect(self.handle_pair_signal)
        self.help_window.closeHelpSignal.connect(self.handle_help_signal)

        for key, value in self.__dict__.items():
            if 'Button' in key and 'end' not in key and 'pair' not in key and 'help' not in key:
                name = key[:-6]
                getattr(self, key).clicked.connect(self.click_handler)
                self.current_action = name
        self.endButton.clicked.connect(self.end_choice)
        self.pairButton.clicked.connect(self.pair_choice)
        self.helpButton.clicked.connect(self.help_choice)

        self.picture_generator.generate_image().save('src/resources/temp/graph.png')
        self.image.setPixmap(QPixmap('src/resources/temp/graph.png'))

        self.sectionButton.setText(f'[{self.variant.start}; {self.variant.end}]')
        self.revsectionButton.setText(f'[{self.variant.end}; {self.variant.start}]')

    @pyqtSlot(str)
    def handle_signal(self, data):
        getattr(self, self.current_action).setText(f'{data}')

        user_answer = [i for i in data.split(', ')]
        if user_answer == ['∅']: user_answer = ['Z']
        answer_flag = False

        if self.current_action == 'order':
            answer_flag = linear_checker(copy.deepcopy(self.variant.connections), ''.join(user_answer))

        else:
            user_answer = set(user_answer)
            task_answer = answers_parser(self.variant.answers, self.current_action)
            answer_flag = False if user_answer not in task_answer else True

        self.answer_flag_handler(answer_flag)

    @pyqtSlot(set)
    def handle_pair_signal(self, data):
        answer_flag = False

        ans = pair_checker(self.variant.connections)
        if data == ans:
            answer_flag = True

        self.answer_flag_handler(answer_flag)

    @pyqtSlot(str)
    def handle_help_signal(self, data):
        self.help_window.close()

    def click_handler(self):
        sender = self.sender().objectName()[:-6]
        self.current_action = sender
        self.graph_window.task_label.setText(humanizer(sender, self.variant.start, self.variant.end))
        self.graph_window.exec()

    def end_choice(self):
        if sum(self.answer_counter.values()) == 8:
            self.successSignal.emit('')

    def pair_choice(self):
        sender = self.sender().objectName()[:-6]
        self.current_action = sender
        self.graph_pair_window.task_label.setText(humanizer(sender, self.variant.start, self.variant.end))
        self.graph_pair_window.exec()

    def help_choice(self):
        self.help_window.exec()

    def answer_flag_handler(self, flag):
        if flag is False:
            self.graph_window.close()
            getattr(self, self.current_action).setStyleSheet(
                "QLabel { background-color: #F1506B; color: #0b392c; padding-left: 10px; border-radius: 6px;}")
            self.failureSignal.emit(self.current_action)

        else:
            getattr(self, self.current_action).setStyleSheet(
                "QLabel { background-color: #67E667; color: #0b392c; padding-left: 10px; border-radius: 6px;}")
            self.answer_counter[self.current_action] = 1
