from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import networkx as nx

class GraphVisualizer(QWidget):
    def __init__(self, parent=None):
        super(GraphVisualizer, self).__init__(parent)

        self.figure = Figure(figsize=(10, 16), dpi=1000) 
        self.canvas = FigureCanvas(self.figure)

        self.label = QLabel("Tiempo de ejecución: ", self)
        self.positions = None

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.move(180,0)
        self.resize(1300, 900)
    
    def create_graph(self, graph):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if self.positions is None:
            self.positions = nx.spring_layout(graph)  # Calcula las posiciones de los nodos
        nx.draw(graph, pos=self.positions, with_labels=True, ax=ax, node_size=4, font_size=1, width=0.25)
        self.canvas.draw()

    def draw_graph(self, graph, edge_colors):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        nx.draw(graph, pos=self.positions, with_labels=True, edge_color=edge_colors.values(), ax=ax, node_size=4, font_size=1, width=2.0)
        self.canvas.draw()

    def draw_execution_time(self, execution_time):     
        self.label.setText("Tiempo de ejecución: " + str(execution_time) + " segs.")