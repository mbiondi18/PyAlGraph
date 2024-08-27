import sys
sys.path.insert(0, 'C:/Users/ameri/Documents/PyAlgGraph')
from App.GraphColorer import GraphColorer
import networkx as nx

def test_color_graph():
    colorer = GraphColorer()
    graph = nx.Graph()
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 1)
    graph.add_edge(1, 4)
    graph.add_edge(4, 5)
    graph.add_edge(5, 6)
    graph.add_edge(6, 4)
    node_colors = colorer.color_graph(graph)
    assert node_colors == ['red', 'green', 'blue', 'yellow', 'pink', 'orange']
    result = colorer.greedy_coloring(graph)
    assert result == {1: 'Red', 2: 'Green', 3: 'Blue', 4: 'Green', 5: 'Red', 6: 'Blue'}
    result = colorer.backtracking(graph)
    assert result == {1: 'Red', 2: 'Green', 3: 'Blue', 4: 'Green', 5: 'Red', 6: 'Blue'}
