import time

from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QDialog, QPlainTextEdit
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
            self.setStyleSheet("QPushButton {border-radius: 30px;background-color: "
                               "white;} QPushButton:hover {background-color: red}")
        else:
            self.setStyleSheet("QPushButton {border-radius: 30px;background-color: "
                               "gray;} QPushButton:hover {background-color: red}")


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
            button.setStyleSheet("QPushButton {border-radius: 30px; background-color: red;}")

            self.selected_nodes.append(button)

        else:
            button.change_styling()

            self.selected_nodes.remove(button)

        if len(self.selected_nodes) == 2:
            time.sleep(0.2)

            self.update_pairs_text_edit()
            self.selected_nodes[0].change_styling()
            self.selected_nodes[-1].change_styling()
            self.selected_nodes.clear()

    def update_pairs_text_edit(self):
        if self.parent().plain_text_edit:
            selected_text = f'({self.selected_nodes[0].name};{self.selected_nodes[-1].name}), '
            self.parent().plain_text_edit.appendPlainText(selected_text if selected_text else "∅")

            cursor = self.parent().plain_text_edit.textCursor()
            cursor.setPosition(len(self.parent().plain_text_edit.toPlainText()))
            self.parent().plain_text_edit.setTextCursor(cursor)


class GraphPairWindow(QDialog):
    saveSignal = pyqtSignal(set)

    def __init__(self, variant):
        super().__init__()
        self.setGeometry(100, 100, 600, 700)
        self.selected_nodes = []
        self.variant = variant
        self.action = ''
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Graph Visualization")
        self.graph_area = GraphArea(self.variant, self)
        self.graph_area.setGeometry(50, 50, 500, 500)
        self.graph_area.setStyleSheet("background-color: white;")

        positions = [(225, 25), (150, 115), (300, 115), (75, 205), (225, 205), (375, 205), (150, 295), (300, 295),
                     (225, 385)]
        names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        for pos, name in zip(positions, names):
            node = GraphNode(name, self.graph_area)
            node.move(*pos)
            self.graph_area.node_positions[name] = (pos[0] + 30, pos[1] + 30)

        self.plain_text_edit = QPlainTextEdit(self)
        self.plain_text_edit.setGeometry(50, 520, 500, 80)
        self.plain_text_edit.textChanged.connect(self.filter_text)

        reset_button = QPushButton("Сбросить", self)
        reset_button.setGeometry(50, 620, 150, 40)
        reset_button.clicked.connect(self.reset_graph)

        save_button = QPushButton("Сохранить", self)
        save_button.setGeometry(400, 620, 150, 40)
        save_button.clicked.connect(self.save_graph)

        self.task_label = QLabel('', self)
        self.task_label.setGeometry(50, 10, 500, 40)
        self.task_label.setFont(QFont("Century Gothic", 16))
        self.task_label.setAlignment(Qt.AlignCenter)

    def reset_graph(self):
        for node in self.graph_area.selected_nodes:
            node.change_styling()
        self.graph_area.selected_nodes.clear()

    def save_graph(self):
        selected_pairs = self.plain_text_edit.toPlainText().split(', ')
        selected_pairs = {(pair[1], pair[3]) for pair in selected_pairs[:-1]}

        self.saveSignal.emit(selected_pairs)

        self.close()
        self.reset_graph()

    def filter_text(self):
        text = self.plain_text_edit.toPlainText()

        filtered_text = ''.join(filter(lambda x: x in '(), ABCDEFGHI;', text))

        if text != filtered_text:
            cursor_position = self.plain_text_edit.textCursor().position()

            self.plain_text_edit.setPlainText(filtered_text)

            cursor = self.plain_text_edit.textCursor()
            cursor.setPosition(min(cursor_position, len(filtered_text)))
            self.plain_text_edit.setTextCursor(cursor)


