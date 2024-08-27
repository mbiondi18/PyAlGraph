from PyQt5.QtWidgets import QVBoxLayout,QMainWindow, QPushButton, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QComboBox, QGraphicsTextItem, QLabel, QGraphicsLineItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QPainter, QFont
from WeightDialog import WeightDialog
from GraphVisualizer import GraphVisualizer
from GraphColorer import GraphColorer
from GraphAnalyzer import GraphAnalyzer
from GraphIO import GraphIO
from Tutorial import Tutorial
from StepByStepSolver import StepByStepSolver
import networkx as nx

class GraphWindow(QMainWindow):
    def __init__(self, app, graph, parent=None):
        super(GraphWindow, self).__init__(parent)
        self.app = app
        self.graph = graph
        
        self.resize(1600, 900)

        self.colorer = GraphColorer(self.graph)
        self.analyzer = GraphAnalyzer()
        self.io = GraphIO()
        self.tutorial = Tutorial()
        self.solver = StepByStepSolver()

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setRenderHint(QPainter.Antialiasing)

        self.count_vertex = 0
        self.nodes = {}
        self.vertex_weights = {}
        self.vertex_items = {}
        self.text_items = {}
        self.edge_items = {}
        self.user_nodes = []

        self.view.move(200,0)
        self.view.resize(1300, 900)

        self.setGeometry(250, 50, 1600, 900)

        self.vertex_button = QPushButton('Add Vertex', self)
        self.vertex_button.clicked.connect(self.add_vertex_mode)
        self.vertex_button.setGeometry(10, 10, 150, 50)

        self.edge_button = QPushButton('Add Edge', self)
        self.edge_button.clicked.connect(self.add_edge_mode)
        self.edge_button.setGeometry(10, 70, 150, 50)

        self.delete_button = QPushButton('Delete', self)
        self.delete_button.clicked.connect(self.delete_mode)
        self.delete_button.setGeometry(10, 130, 150, 50)

        self.create_graph_button = QPushButton('Create graph', self)
        self.create_graph_button.clicked.connect(self.create_graph)
        self.create_graph_button.setGeometry(10, 190, 150, 50)   

        self.vertex_mode = False
        self.edge_mode = False
        self.start_vertex = None
        self.delete_mode_active = False
        self.select_order_mode = False 

        self.layout1 = QVBoxLayout(self)
        self.layout1.addWidget(self.view)
        self.layout1.addWidget(self.vertex_button)
        self.layout1.addWidget(self.edge_button)
        self.layout1.addWidget(self.delete_button)
        self.layout1.addWidget(self.create_graph_button)
        self.setLayout(self.layout1)

        self.vertex_weight_label = QLabel(self)
        self.vertex_weight_label.setGeometry(10, 430, 150, 200)

    def add_vertex_mode(self):
        self.vertex_mode = True
        self.edge_mode = False
        self.delete_mode_active = False

    def add_edge_mode(self):
        self.edge_mode = True
        self.vertex_mode = False
        self.delete_mode_active = False

    def delete_mode(self):
        self.delete_mode_active = True
        self.vertex_mode = False
        self.edge_mode = False
    
    def unable_modes(self):
        self.vertex_mode = False
        self.edge_mode = False
        self.delete_mode_active = False
        self.select_order_mode = False

    def create_graph(self):
        self.app.create_graph(self.graph)
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            if self.is_within_drawing_area(x, y):
                if self.vertex_mode:
                    self.handle_vertex_mode(event)
                elif self.edge_mode:
                    self.handle_edge_mode(event)
                elif self.delete_mode_active:
                    self.handle_delete_mode(event)
                elif self.select_order_mode:
                    self.handle_select_order_mode(event)

    def handle_vertex_mode(self, event):
        pos = self.view.mapToScene(event.pos())
        real_pos_x = pos.x() - 200
        radius = 15
        vertex_item = QGraphicsEllipseItem(real_pos_x - radius/2, pos.y() - radius/2, radius, radius)
        self.scene.addItem(vertex_item)
        self.count_vertex += 1
        self.vertex_items[self.count_vertex] = vertex_item
        if self.count_vertex < 10:
            text_item = QGraphicsTextItem(str(self.count_vertex))
            text_item.setFont(QFont('Arial', 8))
            text_item.setPos(real_pos_x - radius/2, pos.y() - radius/2 - 3)
            self.scene.addItem(text_item)
            self.text_items[self.count_vertex] = text_item
        else:
            text_item = QGraphicsTextItem(str(self.count_vertex))
            text_item.setFont(QFont('Arial', 7))
            text_item.setPos(real_pos_x - radius/2 - 2, pos.y() - radius/2 - 3)
            self.scene.addItem(text_item)
            self.text_items[self.count_vertex] = text_item
        self.nodes[self.count_vertex] = (real_pos_x, pos.y())
        print(self.nodes)
        self.graph.add_node(self.count_vertex)
        self.añadir_peso()
        
    def añadir_peso(self):
        dialog = WeightDialog(self)
        if dialog.exec_():
            weight = dialog.get_weight()
            self.vertex_weights[self.count_vertex] = weight
            self.update_vertex_weights_text()
            print(self.vertex_weights)
    
    def update_vertex_weights_text(self):
        weights_text = "\n".join(f"Vértice {vertex}: {weight}" for vertex, weight in self.vertex_weights.items())
        self.vertex_weight_label.setText(weights_text)

    def handle_edge_mode(self, event):
        pos = self.view.mapToScene(event.pos())
        real_pos_x = pos.x() - 200
        vertex = self.get_vertex_at(real_pos_x, pos.y())
        print(real_pos_x, pos.y())
        print("vertice: ",vertex)
        if vertex is not None:
            if self.start_vertex is None:
                self.start_vertex = vertex
                print("start_vertex: ",self.start_vertex)
            else:
                if self.start_vertex != vertex:
                    self.handle_edge_creation(vertex)
                self.start_vertex = None

    def handle_edge_creation(self, end_vertex):
        start_vertex_coords = self.nodes[self.start_vertex]
        end_vertex_coords = self.nodes[end_vertex]
        if not self.graph.has_edge(self.start_vertex, end_vertex):
            edge_item = QGraphicsLineItem(start_vertex_coords[0], start_vertex_coords[1], end_vertex_coords[0], end_vertex_coords[1])
            self.scene.addItem(edge_item)
            self.edge_items[self.start_vertex, end_vertex] = edge_item
            self.graph.add_edge((self.start_vertex), (end_vertex))
    
    def get_vertex_at(self, x, y):
        for vertex, (vertex_x, vertex_y) in self.nodes.items():
            if abs(vertex_x - x) < 15 and abs(vertex_y - y) < 15:  # 15 es el margen de error
                return vertex
        return None
    
    def get_edge_at(self, x, y):
        for edge, edge_item in self.edge_items.items():
            if edge_item.contains(QPointF(x, y)):
                return edge
        return None

    def is_within_drawing_area(self, x, y):
        drawing_area_left = self.view.pos().x()
        drawing_area_right = drawing_area_left + self.view.width()
        drawing_area_top = self.view.pos().y()
        drawing_area_bottom = drawing_area_top + self.view.height()

        return (drawing_area_left <= x <= drawing_area_right and
                drawing_area_top <= y <= drawing_area_bottom)
    
    def handle_delete_mode(self, event):
        pos = self.view.mapToScene(event.pos())
        real_pos_x = pos.x() - 200
        vertex_id = self.get_vertex_at(real_pos_x, pos.y())
        edge_id = self.get_edge_at(real_pos_x, pos.y())
        if vertex_id is not None:
            self.eliminarVertice(vertex_id)
        elif edge_id is not None:
            edge_item = self.edge_items[edge_id]
            self.scene.removeItem(edge_item)
            if edge_id in self.graph.edges:
                self.graph.remove_edge(*edge_id)
            if edge_id in self.edge_items:
                del self.edge_items[edge_id]

    def eliminarVertice(self, vertex_id):
        vertex_item = self.vertex_items[vertex_id]
        text_item = self.text_items[vertex_id]
        self.scene.removeItem(vertex_item)
        self.scene.removeItem(text_item)
        for edge in self.edge_items.copy():
            print(edge[0], edge[1])
            if vertex_id == edge[0] or vertex_id == edge[1]:
                edge_item = self.edge_items[edge]
                self.scene.removeItem(edge_item)
                del self.edge_items[edge]
        self.graph.remove_node(vertex_id)
        if vertex_id in self.nodes:
            del self.nodes[vertex_id]
        if vertex_id in self.vertex_weights:
            del self.vertex_weights[vertex_id]
            self.update_vertex_weights_text()
    
    def handle_select_order_mode(self, event):
        pos = self.view.mapToScene(event.pos())
        real_pos_x = pos.x() - 200
        vertex_id = self.get_vertex_at(real_pos_x, pos.y())
        if vertex_id is not None:
            vertex_item = self.vertex_items[vertex_id]
            vertex_item.setBrush(QBrush(Qt.blue))
            self.scene.update()
            self.user_nodes.append(vertex_id)
            if len(self.user_nodes) == len(self.graph.nodes):
                self.select_order_mode = False
                result = self.colorer.secuencial_coloring(self.graph, self.user_nodes)
                self.print(result)