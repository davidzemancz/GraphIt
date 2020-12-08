from GraphIt import Console, Graph, Edge, Vertex

graph = Graph()
graph.add_vertex(Vertex(1, "Jedna"))
graph.add_vertex(Vertex(2, "Dva"))
graph.add_vertex(Vertex(3, "Tri"))
graph.add_vertices([Vertex(4, "Ctyri"), Vertex(5, "Pet"), Vertex(6, "Sest")])
graph.add_edge(Edge(Vertex(1), Vertex(2), 2))
graph.add_edge(Edge(Vertex(3), Vertex(2), 4))
graph.add_edge(Edge(Vertex(4), Vertex(6), 1))
graph.add_edge(Edge(Vertex(4), Vertex(5), 9))
graph.add_edge(Edge(Vertex(1), Vertex(6), 7))
graph.add_edge(Edge(Vertex(2), Vertex(4), 1))
graph.add_edge(Edge(Vertex(1), Vertex(4), 2))
graph.add_edge(Edge(Vertex(3), Vertex(6), 2))
#print("Is tree? -", graph.is_tree())
#spanning_tree = graph.get_minSpanningTree()
#for edge in spanning_tree.edges:
#    print(edge.vertex_1.id, "<->", edge.vertex_2.id, "weight - ", edge.weight)
dic = graph.get_minDistDic(Vertex(1))
for v_id in dic:
    print(v_id, "-", dic[v_id])

Console.start()
