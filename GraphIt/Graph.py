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

        # Pokud vrchol uz existuje, aktualizuji jen jmeno
        if vertex.id in self.vertices:
            self.vertices[vertex.id].name = vertex.name
        else:
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

        # Indexy vrcholu v poli
        v1_index = self.vertices[edge.vertex_1.id]._index
        v2_index = self.vertices[edge.vertex_2.id]._index

        # Neorientovany graf -> symetricka matice
        self.matrix.array[v1_index][v2_index] = edge.weight
        self.matrix.array[v2_index][v1_index] = edge.weight

        # Nastavim vrcholy hrany
        edge.vertex_1 = self.vertices[edge.vertex_1.id]
        edge.vertex_2 = self.vertices[edge.vertex_2.id]

        # Pridam hranu
        self.edges.append(edge)

        return self

    def remove_edge(self, edge: Edge):

        # Indexy vrcholu v poli
        v1_index = self.vertices[edge.vertex_1.id]._index
        v2_index = self.vertices[edge.vertex_2.id]._index

        # Odstranim vzdalenost v matici
        self.matrix.array[v1_index][v2_index] = 0
        self.matrix.array[v2_index][v1_index] = 0

        # Odstranim hranu
        self.edges.remove(edge)

        return self

    # Vlozi vice hran
    def add_edges(self, edges: []):
        for edge in edges:
            self.add_edge(edge)
        return self

    # Vraci, zda je graf strom
    def is_tree(self): 

        # ==================================
        # TODO: Treba upravit, funguje jen pro souvisle grafy!
        # ==================================

        vertices = {}
        for edge in self.edges:
            vertices[edge.vertex_1.id] = edge.vertex_1
            vertices[edge.vertex_2.id] = edge.vertex_2

        return len(self.edges) == len(vertices) - 1 

    # Vrati nejakou kostru grafu
    def get_minSpanningTree(self):
        spanningTree = Graph()

        # Seradim hrany podle ohodnoceni
        sorted_edges = self.edges.copy()
        GraphEdgesHandler.sort(sorted_edges)

        while len(spanningTree.edges) < len(self.vertices) - 1: # Dokud nejsou hrany mezi vsemi vrcholy
            edge = sorted_edges.pop(0) # Hrana s nejnizsim ohodnocennim
            spanningTree.add_vertex(edge.vertex_1)
            spanningTree.add_vertex(edge.vertex_2)
            spanningTree.add_edge(edge)
            
            if not spanningTree.is_tree():
                spanningTree.remove_edge(edge)
        return spanningTree

    # dijkstruv algoritmus
    def dijkstra(self):

        return self
    
    



    

