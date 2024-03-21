from PyQt5.QtWidgets import QPushButton, QWidget, QLabel
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QFont
from utils.helper_functions import hasseParser
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
                               "white;}")
        else:
            self.setStyleSheet("QPushButton {border-radius: 30px;background-color: "
                               "gray;}")


class GraphArea(QWidget):
    def __init__(self, parent=None):
        super(GraphArea, self).__init__(parent)
        self.node_positions = {}
        self.adjacency_list, self.start_node, self.end_node = {}, '', ''
        self.selected_nodes: list[GraphNode] = []
        self.get_variant()

    def get_variant(self) -> (dict[str, list[list, list]], str, str):
        variant = crud.get_random_variant()
        self.adjacency_list = hasseParser(variant.connections)

        self.start_node = variant.start
        self.end_node = variant.end

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2))
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
        self.update_parent_info_label()

    def update_parent_info_label(self):
        if self.parent().info_label:
            selected_text = ', '.join(node.name for node in self.selected_nodes)
            self.parent().info_label.setText(selected_text if selected_text else "∅")


class GraphWindow(QWidget):
    saveSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 700)
        self.selected_nodes = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Graph Visualization")
        self.graph_area = GraphArea(self)
        self.graph_area.setGeometry(50, 50, 500, 500)
        self.graph_area.setStyleSheet("background-color: white;")

        positions = [(225, 25), (150, 115), (300, 115), (75, 205), (225, 205), (375, 205), (150, 295), (300, 295),
                     (225, 385)]
        names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        for pos, name in zip(positions, names):
            node = GraphNode(name, self.graph_area)
            node.move(*pos)
            self.graph_area.node_positions[name] = (pos[0] + 30, pos[1] + 30)

        self.info_label = QLabel("∅", self)
        self.info_label.setGeometry(50, 560, 500, 40)
        self.info_label.setFont(QFont("Century Gothic", 16))
        self.info_label.setAlignment(Qt.AlignCenter)

        reset_button = QPushButton("Сбросить", self)
        reset_button.setGeometry(50, 620, 150, 40)
        reset_button.clicked.connect(self.reset_graph)

        # Add "Save" button
        save_button = QPushButton("Сохранить", self)
        save_button.setGeometry(400, 620, 150, 40)
        save_button.clicked.connect(self.save_graph)

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

