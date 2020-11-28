from GraphIt import Console, Graph, Edge, Vertex

graph = Graph()
graph.init_vertices({1:"Jedna", 2:"Dva", 3:"Treti", 4:"Ctvrty"})
graph.add_edge(Edge(Vertex(1), Vertex(2)))

Console.start()
