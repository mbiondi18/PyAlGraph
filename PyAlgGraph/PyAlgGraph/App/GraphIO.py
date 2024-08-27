import json
import networkx as nx

class GraphIO:
    def __init__(self):
        pass

    def save_graph(self, graph, filename):
        # Implementa la exportación de grafos aquí
        pass

    def load_graph(self, filename):
        # Implementa la importación de grafos aquí
        # Añadir los nodos y las aristas al grafo
        with open(filename) as f:
            data = json.load(f)

        graph = nx.Graph()

        for node in data['nodes']:
            graph.add_node(node['id'], **node['attributes'])

        for edge in data['edges']:
            graph.add_edge(edge['source'], edge['target'], **edge['attributes'])
        pass


