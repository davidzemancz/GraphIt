from Matrix import Matrix
from Vertex import Vertex
from Edge import Edge
import GraphEdgesHandler

class Graph:
    def __init__(self):
        self.matrix = Matrix()
        self.vertices = {}
        self.edges = []

    @property
    def matrix(self):
       return self.__matrix

    @matrix.setter
    def matrix(self, value):
       self.__matrix = value

    @property
    def vertices(self):
       return self.__vertices

    @vertices.setter
    def vertices(self, value):
       self.__vertices = value

    @property
    def edges(self):
       return self.__edges

    @edges.setter
    def edges(self, value):
       self.__edges = value

    def clear(self):
       self.matrix = Matrix()
       self.vertices = {}
       self.edges = []
       return self

    # Prida novy vrchol, tj. radek a sloupec do matice
    def add_vertex(self, vertex: Vertex):
        # Pridam sloupec do existujicich radku
        for i in range(len(self.matrix.array)):
            self.matrix.array[i].append(0)

        # Pridam novy radek
        new_size = len(self.matrix.array) + 1
        new_row = [0] * new_size
        new_index = new_size - 1
        new_row[new_index] = float('inf') # Novy vrchol
        self.matrix.array.append(new_row)

        vertex._index = new_index
        self.vertices[vertex.id] = vertex

        return self

    # Prida nove vrcholy
    def add_vertices(self, vertices: []):
        for vertex in vertices:
            self.add_vertex(vertex)
        return self


    # Vlozi hranu mezi dva vrcholy grafu
    def add_edge(self, edge: Edge):

        v1_index = self.vertices[edge.vertex_1.id]._index
        v2_index = self.vertices[edge.vertex_2.id]._index

        # Neorientovany graf -> symetricka matice
        self.matrix.array[v1_index][v2_index] = edge.weight
        self.matrix.array[v2_index][v1_index] = edge.weight

        self.edges.append(edge)

        return self

    # Vlozi vice hran
    def add_edges(self, edges: []):
        for edge in edges:
            self.add_edge(edge)
        return self


    # Vrati nejakou kostru grafu
    def get_spanningTree(self):
        spanningTree = Graph()

        # Seradim hrany podle ohodnoceni
        sorted_edges = self.edges.copy()
        GraphEdgesHandler.sort(sorted_edges)

        for edge in sorted_edges:
            print(edge.vertex_1.id, "<->", edge.vertex_2.id, "weight - ", edge.weight)



        return spanningTree
    
    



    

