import GraphIt

graph = GraphIt.Graph()
graph.init_vertices({1:"Jedna", 2:"Dva", 3:"Treti", 4:"Ctvrty"})
graph.add_edge(GraphIt.Edge(GraphIt.Vertex(1), GraphIt.Vertex(2)))

GraphIt.console_start()
