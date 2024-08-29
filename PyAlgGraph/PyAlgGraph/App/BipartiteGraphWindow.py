from PyQt5.QtWidgets import QMainWindow, QPushButton, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem, QLabel, QGraphicsLineItem, QInputDialog
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QPainter, QFont
import networkx as nx

class BipartiteGraphWindow(QMainWindow):
    def __init__(self, app, graph, parent=None):
        super(BipartiteGraphWindow, self).__init__(parent)
        self.app = app
        self.graph = nx.Graph()
        
        self.resize(1600, 900)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setRenderHint(QPainter.Antialiasing)

        self.count_vertex_left = 0
        self.count_vertex_right = 0
        self.nodes_left = {}
        self.nodes_right = {}
        self.nodes = {}
        self.vertex_weights = {}
        self.vertex_items = {}
        self.text_items = {}
        self.edge_items = {}


        self.view.move(200, 0)
        self.view.resize(1300, 900)

        self.setGeometry(250, 50, 1600, 900)

        self.vertex_left_button = QPushButton('Add Left Vertex', self)
        self.vertex_left_button.clicked.connect(self.add_vertex_left_mode)
        self.vertex_left_button.setGeometry(10, 10, 150, 50)

        self.vertex_right_button = QPushButton('Add Right Vertex', self)
        self.vertex_right_button.clicked.connect(self.add_vertex_right_mode)
        self.vertex_right_button.setGeometry(10, 70, 150, 50)

        self.edge_button = QPushButton('Add Edge', self)
        self.edge_button.clicked.connect(self.add_edge_mode)
        self.edge_button.setGeometry(10, 130, 150, 50)

        self.delete_button = QPushButton('Delete', self)
        self.delete_button.clicked.connect(self.delete_mode)
        self.delete_button.setGeometry(10, 190, 150, 50)

        self.create_graph_button = QPushButton('Create Bipartite Graph', self)
        self.create_graph_button.clicked.connect(self.create_graph)
        self.create_graph_button.setGeometry(10, 250, 150, 50)   

        self.vertex_mode_left = False
        self.vertex_mode_right = False
        self.edge_mode = False
        self.start_vertex = None
        self.delete_mode_active = False

    def add_vertex_left_mode(self):
        self.vertex_mode_left = True
        self.vertex_mode_right = False
        self.edge_mode = False
        self.delete_mode_active = False

    def add_vertex_right_mode(self):
        self.vertex_mode_left = False
        self.vertex_mode_right = True
        self.edge_mode = False
        self.delete_mode_active = False

    def add_edge_mode(self):
        self.edge_mode = True
        self.vertex_mode_left = False
        self.vertex_mode_right = False
        self.delete_mode_active = False

    def delete_mode(self):
        self.delete_mode_active = True
        self.vertex_mode_left = False
        self.vertex_mode_right = False
        self.edge_mode = False

    def create_graph(self):
        self.app.create_bipartite_graph(self.graph)
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            if self.is_within_drawing_area(x, y):
                if self.vertex_mode_left:
                    self.handle_vertex_mode(event, is_left=True)
                elif self.vertex_mode_right:
                    self.handle_vertex_mode(event, is_left=False)
                elif self.edge_mode:
                    self.handle_edge_mode(event)
                elif self.delete_mode_active:
                    self.handle_delete_mode(event)

    def handle_vertex_mode(self, event, is_left):
        pos = self.view.mapToScene(event.pos())
        real_pos_x = pos.x() - 200 if is_left else pos.x() + 200
        radius = 15
        vertex_item = QGraphicsEllipseItem(real_pos_x - radius/2, pos.y() - radius/2, radius, radius)
        self.scene.addItem(vertex_item)
        
        if is_left:
            self.count_vertex_left += 1
            count = self.count_vertex_left
            self.nodes_left[count] = (real_pos_x, pos.y())
        else:
            self.count_vertex_right += 1
            count = self.count_vertex_right
            self.nodes_right[count] = (real_pos_x, pos.y())

        self.vertex_items[count] = vertex_item
        
        text_item = QGraphicsTextItem(str(count))
        text_item.setFont(QFont('Arial', 8))
        text_item.setPos(real_pos_x - radius/2, pos.y() - radius/2 - 3)
        self.scene.addItem(text_item)
        self.text_items[count] = text_item

        self.graph.add_node(count, bipartite=0 if is_left else 1)
        self.add_weight(count)

    def add_weight(self, vertex):
        weight, ok = QInputDialog.getInt(self, "Vertex Weight", "Enter weight for vertex " + str(vertex))
        if ok:
            self.vertex_weights[vertex] = weight

    def handle_edge_mode(self, event):
        pos = self.view.mapToScene(event.pos())
        real_pos_x = pos.x()
        vertex = self.get_vertex_at(real_pos_x, pos.y())
        if vertex is not None:
            if self.start_vertex is None:
                self.start_vertex = vertex
                print(f"Start vertex selected: {self.start_vertex}")
            else:
                if self.start_vertex != vertex:
                    # Check if the vertices are from different sets
                    if ((self.start_vertex in self.nodes_left and vertex in self.nodes_right) or
                        (self.start_vertex in self.nodes_right and vertex in self.nodes_left)):
                        self.handle_edge_creation(vertex)
                    else:
                        print("Edges can only be created between left and right sets.")
                self.start_vertex = None

    def handle_edge_creation(self, end_vertex):
        start_vertex_coords = self.nodes_left.get(self.start_vertex) or self.nodes_right.get(self.start_vertex)
        end_vertex_coords = self.nodes_left.get(end_vertex) or self.nodes_right.get(end_vertex)
        if start_vertex_coords and end_vertex_coords:
            if not self.graph.has_edge(self.start_vertex, end_vertex):
                edge_item = QGraphicsLineItem(start_vertex_coords[0], start_vertex_coords[1],
                                              end_vertex_coords[0], end_vertex_coords[1])
                self.scene.addItem(edge_item)
                self.edge_items[(self.start_vertex, end_vertex)] = edge_item
                self.graph.add_edge(self.start_vertex, end_vertex)
                print(f"Edge created between {self.start_vertex} and {end_vertex}")
            else:
                print(f"Edge between {self.start_vertex} and {end_vertex} already exists")
        else:
            print("Invalid vertex coordinates")

    def get_vertex_at(self, x, y):
        for nodes in [self.nodes_left, self.nodes_right]:
            for vertex, (vertex_x, vertex_y) in nodes.items():
                if abs(vertex_x - x) < 15 and abs(vertex_y - y) < 15:  # 15 is the error margin
                    return vertex
        return None
    
    def get_edge_at(self, x, y):
        for nodes in [self.nodes_left, self.nodes_right]:
            for vertex, (vertex_x, vertex_y) in nodes.items():
                if abs(vertex_x - x) < 15 and abs(vertex_y - y) < 15:  # 15 is the error margin
                    return vertex
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