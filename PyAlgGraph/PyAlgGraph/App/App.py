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
from GraphWindow import GraphWindow
from BipartiteGraphWindow import BipartiteGraphWindow
import networkx as nx

class App(QMainWindow):
    def __init__(app):
        super().__init__()
        app.resize(1600, 900)
        
        app.graph = nx.Graph()  # Create a graph instance for this App
        app.visualizer = GraphVisualizer(app)
        app.colorer = GraphColorer(app.graph)
        app.analyzer = GraphAnalyzer()
        app.io = GraphIO()
        app.tutorial = Tutorial()
        app.solver = StepByStepSolver()

        app.scene = QGraphicsScene()
        app.view = QGraphicsView(app.scene, app)
        app.view.setRenderHint(QPainter.Antialiasing)

        app.paint_graph_button = QPushButton('Make Graph', app)
        app.paint_graph_button.clicked.connect(app.open_graph_window)
        app.paint_graph_button.setGeometry(10, 190, 150, 50)

        app.paint_bipartite_graph_button = QPushButton('Make Bipartite Graph', app)
        app.paint_bipartite_graph_button.clicked.connect(app.open_bipartite_graph_window)
        app.paint_bipartite_graph_button.setGeometry(10, 250, 150, 50)

        app.secuencial_coloring_button = QComboBox(app)
        app.secuencial_coloring_button.addItems(["Secuencial coloring default order", "Secuencial coloring user order"])
        app.secuencial_coloring_button.activated[str].connect(app.on_secuencial_coloring_button_activated)
        app.secuencial_coloring_button.setGeometry(10, 310, 150, 50)

        layout = QVBoxLayout(app)
        layout.addWidget(app.secuencial_coloring_button)
        layout.addWidget(app.paint_graph_button)
        layout.addWidget(app.paint_bipartite_graph_button)
        layout.addWidget(app.visualizer)
        app.setLayout(layout)

        app.setGeometry(250, 50, 1600, 1100)

    def open_graph_window(app):
        app.graph_window = GraphWindow(app, app.graph)
        app.graph_window.show()    

    def unable_modes(app):
        app.select_order_mode = False

    def create_graph(app, graph): 
        print("create_graph method triggered")
        app.unable_modes()
        app.graph = graph  # Update the app's graph with the one from GraphWindow
        app.visualizer.create_graph(app.graph)

    def create_bipartite_graph(app, graph):
        print("create_bipartite_graph method triggered")
        app.unable_modes()
        app.graph = graph  # Update the app's graph with the bipartite graph
        app.visualizer.create_graph(app.graph)    

    def on_secuencial_coloring_button_activated(self, text):
        if text == "Secuencial coloring default order":
            self.secuencial_coloring(self.graph.edges())
        elif text == "Secuencial coloring user order":
            print("Secuencial coloring user order")
            self.secuencial_coloring_user_order()

    def bipartite_coloring(app):
        edge_colors = app.colorer.bipartite_coloring(app.graph)
        app.print(edge_colors)        


    def secuencial_coloring(app, edges):
        edge_colors = app.colorer.secuencial_coloring(app.graph, edges)
        app.print(edge_colors)

    def secuencial_coloring_user_order(app):
        app.unable_modes()
        app.select_order_mode = True
    
    def open_bipartite_graph_window(app):
        app.bipartite_graph_window = BipartiteGraphWindow(app, app.graph)
        app.bipartite_graph_window.show()

    def print(app, edge_colors):
        app.unable_modes()
        app.visualizer.draw_graph(app.graph, edge_colors)
        app.visualizer.draw_execution_time(app.colorer.execution_time)
