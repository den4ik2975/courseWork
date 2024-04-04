from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QDialog
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QFont
from utils.helper_functions import hasse_parser, humanizer
from database import crud


class GraphNode(QPushButton):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)  # Set the button text to the node name
        self.name = name
        self.endpoint = False
        self.setFixedSize(60, 60)  # Increase the size of the buttons
        self.setFont(QFont("Century Gothic", 16))

        if parent.start_node == self.name or parent.end_node == self.name:
            self.endpoint = True

        self.change_styling()
        self.clicked.connect(self.on_click)

    def on_click(self):
        parent = self.parent()
        if isinstance(parent, GraphArea):
            parent.node_clicked(self)

    def change_styling(self):
        if self.endpoint:
            self.setStyleSheet("QPushButton {border-radius: 30px;"
                               "background-color: #FFF9E8;"
                               "border-radius: 30px; "
                               "font-weight: bold;"
                               "border: 2px solid #ffb804;} "
                               "QPushButton:hover {background-color: #6e9673; "
                               "color: white;"
                               "border: None;}")
        else:
            self.setStyleSheet("QPushButton {border-radius: 30px;"
                               "background-color: #E2EFE4;"
                               "border-radius: 30px; "
                               "font-weight: bold;"
                               "border: 2px solid #6e9673;} "
                               "QPushButton:hover {background-color: #6e9673; "
                               "color: white;}")


class GraphArea(QWidget):
    def __init__(self, variant, parent=None):
        super(GraphArea, self).__init__(parent)
        self.node_positions = {}
        self.adjacency_list, self.start_node, self.end_node = {}, '', ''
        self.selected_nodes: list[GraphNode] = []
        self.adjacency_list = hasse_parser(variant.connections)
        self.start_node = variant.start
        self.end_node = variant.end

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 3))
        for start_node, connected_nodes in self.adjacency_list.items():
            if start_node in self.node_positions:
                start_pos = self.node_positions[start_node]
                for end_node in connected_nodes:
                    if end_node in self.node_positions:
                        end_pos = self.node_positions[end_node]

                        painter.drawLine(QPoint(*start_pos), QPoint(*end_pos))

    def node_clicked(self, button):
        if button not in self.selected_nodes:
            button.setStyleSheet("QPushButton {border-radius: 30px; font-weight: bold; background-color: #6e9673;}")
            self.selected_nodes.append(button)
        else:
            button.change_styling()

            self.selected_nodes.remove(button)
        self.update_parent_info_label()

    def update_parent_info_label(self):
        if self.parent().info_label:
            selected_text = ', '.join(node.name for node in self.selected_nodes)
            self.parent().info_label.setText(selected_text if selected_text else "∅")


class GraphWindow(QDialog):
    saveSignal = pyqtSignal(str)

    def __init__(self, variant):
        super().__init__()
        self.setGeometry(100, 100, 600, 700)
        self.selected_nodes = []
        self.variant = variant
        self.action = ''
        self.initUI()
        self.setFont(QFont("Century Gothic", 20))
        self.setStyleSheet("background-color: white; "
                           "QLabel { font-weight: bold; }"
                           "QPushButton { font-weight: bold; }")

    def initUI(self):
        self.setWindowTitle("Выберите элементы")
        self.graph_area = GraphArea(self.variant, self)
        self.graph_area.setGeometry(50, 50, 500, 500)

        positions = [(225, 55), (150, 145), (300, 145), (75, 235), (225, 235), (375, 235), (150, 325), (300, 325),
                     (225, 415)]
        names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        for pos, name in zip(positions, names):
            node = GraphNode(name, self.graph_area)
            node.move(*pos)
            self.graph_area.node_positions[name] = (pos[0] + 30, pos[1] + 30)

        self.info_label = QLabel("∅", self)
        self.info_label.setGeometry(40, 550, 520, 40)
        self.info_label.setFont(QFont("Century Gothic", 18))
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("background-color: #f6f8f7; "
                                      "font-weight: bold;"
                                      "color: #0b392c; "
                                      "padding-left: 10px; "
                                      "border-radius: 10px;")

        reset_button = QPushButton("Сбросить", self)
        reset_button.setGeometry(40, 600, 200, 60)
        reset_button.setFont(QFont("Century Gothic", 20))
        reset_button.clicked.connect(self.reset_graph)

        reset_button.setStyleSheet("QPushButton {background-color: #bb8a52; "
                                   "color: white; "
                                   "border-radius: 6px; "
                                   "text-align: center;"
                                   "font-weight: bold;} "
                                   "QPushButton:hover {background-color: #A47A4C; "
                                   "color: white;}")

        save_button = QPushButton("Завершить", self)
        save_button.setGeometry(360, 600, 200, 60)
        save_button.setFont(QFont("Century Gothic", 20))
        save_button.clicked.connect(self.save_graph)

        save_button.setStyleSheet("QPushButton {background-color: #ffb804;"
                                  "border-radius: 10px;"
                                  "color: white;"
                                  "font-weight: bold;}"
                                  "QPushButton:hover {background-color: #f3a600}")

        self.task_label = QLabel('', self)
        self.task_label.setGeometry(40, 20, 520, 60)
        self.task_label.setFont(QFont("Century Gothic", 20))
        self.task_label.setAlignment(Qt.AlignCenter)
        self.task_label.setStyleSheet("background-color: #6e9673; "
                                      "border-radius: 10px;"
                                      "font-weight: bold;"
                                      "color: white;")

    def reset_graph(self):
        for node in self.graph_area.selected_nodes:
            node.change_styling()
        self.graph_area.selected_nodes.clear()
        self.info_label.setText("∅")

    def save_graph(self):
        selected_node_names = [node.name for node in self.graph_area.selected_nodes]
        if selected_node_names:
            self.saveSignal.emit(', '.join(selected_node_names))
        else:
            self.saveSignal.emit('∅')

        self.close()
        self.reset_graph()

