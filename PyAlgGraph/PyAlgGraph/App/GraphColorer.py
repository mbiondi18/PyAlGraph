import networkx as nx
import time

colors = ["Red", "Green", "Blue", "Yellow", "Orange", "Violet", "Brown", "Gray", "Black", "White", "Pink", "Cyan", "Magenta", "Lime", "Teal", "Indigo", "Maroon", "Olive", "Navy", "Purple", "Silver", "Aqua", "Fuchsia", "WhiteSmoke", "AliceBlue", "AntiqueWhite", "Azure", "Beige", "Bisque", "BlanchedAlmond", "BurlyWood", "Coral", "CornflowerBlue", "Cornsilk", "Crimson", "DarkGoldenRod", "DarkKhaki", "DarkOrange", "DarkOrchid", "DarkSalmon", "DarkSeaGreen", "DarkTurquoise", "DarkViolet", "DeepPink", "DeepSkyBlue", "DimGray", "DodgerBlue", "FireBrick", "FloralWhite", "ForestGreen", "Gainsboro", "GhostWhite", "Gold", "GoldenRod", "GreenYellow", "HoneyDew", "HotPink", "IndianRed", "Ivory", "Khaki", "Lavender", "LavenderBlush", "LawnGreen", "LemonChiffon", "LightBlue", "LightCoral", "LightCyan", "LightGoldenRodYellow", "LightGray", "LightGreen", "LightPink", "LightSalmon", "LightSeaGreen", "LightSkyBlue", "LightSlateGray", "LightSteelBlue", "LightYellow", "LimeGreen", "Linen", "MediumAquaMarine", "MediumOrchid", "MediumPurple", "MediumSeaGreen", "MediumSlateBlue", "MediumSpringGreen", "MediumTurquoise", "MediumVioletRed", "MintCream", "MistyRose", "Moccasin", "NavajoWhite", "OldLace", "OrangeRed", "Orchid", "PaleGoldenRod", "PaleGreen", "PaleTurquoise", "PaleVioletRed", "PapayaWhip", "PeachPuff", "Peru", "Pink", "Plum", "PowderBlue", "RosyBrown", "RoyalBlue", "SaddleBrown", "Salmon", "SandyBrown", "SeaGreen", "SeaShell", "Sienna", "SkyBlue", "SlateBlue", "SlateGray", "Snow", "SpringGreen", "SteelBlue"]

class GraphColorer:

    def __init__(self, graph: nx.Graph):
        self.execution_time = 0
        self.color = {}
        self.dsatur = {}

    def welsh_powell_ordering(self, graph: nx.Graph):
        # Ordena las aristas en orden descendente de grado (suma de grados de los nodos)
        edges = sorted(graph.edges(), key=lambda x: graph.degree(x[0]) + graph.degree(x[1]), reverse=True)
        return edges
    
    def matula_marble_isaacson_ordering(self, graph: nx.Graph):
        # Ordena las aristas en orden ascendente de grado (suma de grados de los nodos)
        edges = sorted(graph.edges(), key=lambda x: graph.degree(x[0]) + graph.degree(x[1]))
        return edges

    def secuencial_coloring(self, graph: nx.Graph, edges: list):
        start_time = time.time()
        # Diccionario para guardar el color asignado a cada arista
        edge_colors = {}

        for u, v in edges:
            print("Edge: ", (u, v))
            available_colors = [True] * len(colors)

            # Verificar colores de aristas adyacentes
            for w in graph.neighbors(u):
                edge = (u, w) if u < w else (w, u)
                if edge in edge_colors:
                    color_index = colors.index(edge_colors[edge])
                    available_colors[color_index] = False
            for w in graph.neighbors(v):
                edge = (v, w) if v < w else (w, v)
                if edge in edge_colors:
                    color_index = colors.index(edge_colors[edge])
                    available_colors[color_index] = False

            for color_index, is_available in enumerate(available_colors):
                if is_available:
                    edge_color = colors[color_index]
                    edge = (u, v) if u < v else (v, u)
                    edge_colors[edge] = edge_color
                    print("Color: ", edge_color)
                    break
        
        print("Greedy Coloring edge colors: ", edge_colors)
        end_time = time.time()
        self.execution_time = end_time - start_time
        print("Execution time: ", self.execution_time, " seconds")
        return edge_colors
    
    def bipartite_coloring(self, graph: nx.Graph):
        start_time = time.time()
        left_nodes = {n for n, d in graph.nodes(data=True) if d['bipartite'] == 0}
        right_nodes = set(graph) - left_nodes

        edge_colors = {}
        for left_node in left_nodes:
            available_colors = set(colors)
            for neighbor in graph[left_node]:
                if (left_node, neighbor) in edge_colors:
                    available_colors.discard(edge_colors[(left_node, neighbor)])
                elif (neighbor, left_node) in edge_colors:
                    available_colors.discard(edge_colors[(neighbor, left_node)])
            
            for neighbor in graph[left_node]:
                if (left_node, neighbor) not in edge_colors and (neighbor, left_node) not in edge_colors:
                    edge_color = min(available_colors, key=lambda c: sum(graph.nodes[n]['weight'] for n in [left_node, neighbor]))
                    edge_colors[(left_node, neighbor)] = edge_color
                    available_colors.discard(edge_color)

        end_time = time.time()
        self.execution_time = end_time - start_time
        print("Execution time: ", self.execution_time, " seconds")
        return edge_colors

    def brelaz_coloring(self, graph: nx.Graph):
        start_time = time.time()
        edge_colors = {}
        dsatur = {edge: 0 for edge in graph.edges()}

        while len(edge_colors) < len(graph.edges()):
            # Seleccionar la arista con el mayor grado de saturación
            uncolored_edges = [e for e in graph.edges() if e not in edge_colors]
            max_dsatur = max(dsatur[e] for e in uncolored_edges)
            max_degree_edges = [e for e in uncolored_edges if dsatur[e] == max_dsatur]
            e = max(max_degree_edges, key=lambda x: graph.degree(x[0]) + graph.degree(x[1]))

            # Colorear la arista con el primer color disponible
            available_colors = set(colors)
            for n in e:
                for adj in graph[n]:
                    adj_edge = (n, adj) if n < adj else (adj, n)
                    if adj_edge in edge_colors:
                        available_colors.discard(edge_colors[adj_edge])
            
            edge_color = min(available_colors)
            edge_colors[e] = edge_color

            # Actualizar el grado de saturación de las aristas adyacentes
            for n in e:
                for adj in graph[n]:
                    adj_edge = (n, adj) if n < adj else (adj, n)
                    if adj_edge not in edge_colors:
                        dsatur[adj_edge] = len(set(edge_colors[e] for e in graph.edges(n) if e in edge_colors))

        end_time = time.time()
        self.execution_time = end_time - start_time
        print("Execution time: ", self.execution_time, " seconds")
        return edge_colors
    
    def block_coloring(self, graph):
        # Divide el grafo en bloques
        blocks = list(nx.biconnected_components(graph))

        # Colorea cada bloque de manera independiente
        block_colors = []
        for block in blocks:
            block_graph = graph.subgraph(block)
            colorer = GraphColorer(block_graph)
            block_colors.append(colorer.secuencial_coloring(block_graph, colorer.welsh_powell_ordering(block_graph)))

        # Combina los colores de todos los bloques
        edge_colors = {}
        for block_edge_colors in block_colors:
            edge_colors.update(block_edge_colors)

        return edge_colors
