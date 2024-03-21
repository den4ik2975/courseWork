from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from ui.GraphWindow import GraphWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.graph_window = GraphWindow()
        uic.loadUi("ui/MainWindow.ui", self)
        self.currentAction = ''
        self.graph_window.saveSignal.connect(self.handle_signal)

        for key, value in self.__dict__.items():
            if 'Button' in key:
                name = key[:-6]
                getattr(self, key).clicked.connect(getattr(self, name + '_choice'))
                self.currentAction = name

    @pyqtSlot(str)
    def handle_signal(self, data):
        getattr(self, self.currentAction).setText(f'{data}')

    def click_handler(self):
        self.graph_window.show()

    def maxes_choice(self):
        self.graph_window.show()
        self.currentAction = 'maxes'

    def mins_choice(self):
        self.graph_window.show()
        self.currentAction = 'mins'

    def largest_choice(self):
        self.graph_window.show()
        self.currentAction = 'largest'

    def smallest_choice(self):
        self.graph_window.show()
        self.currentAction = 'smallest'

    def section_choice(self):
        self.graph_window.show()
        self.currentAction = 'section'

    def revsection_choice(self):
        self.graph_window.show()
        self.currentAction = 'revsection'

    def order_choice(self):
        self.graph_window.show()
        self.currentAction = 'order'

    def end_choice(self):
        pass