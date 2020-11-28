from Matrix import Matrix

class Vertex:
    def __init__(self, id, name = "", index = 0):
        self.id = id
        self.name = name
        self._index = index

    @property
    def id(self):
       return self.__id

    @id.setter
    def id(self, value):
       self.__id = value

    @property
    def name(self):
       return self.__name

    @name.setter
    def name(self, value):
       self.__name = value

    @property
    def _index(self):
       return self.__index

    @_index.setter
    def _index(self, value):
       self.__index = value

class Edge:
    def __init__(self, vertex_1: Vertex, vertex_2: Vertex, weight = 1):
        self.vertex_1 = vertex_1
        self.vertex_2 = vertex_2
        self.weight = weight

    @property
    def vertex_1(self):
       return self.__vertex_1

    @vertex_1.setter
    def vertex_1(self, value):
       self.__vertex_1 = value

    @property
    def vertex_2(self):
       return self.__vertex_2

    @vertex_2.setter
    def vertex_2(self, value):
       self.__vertex_2 = value

    @property
    def weight(self):
       return self.__weight

    @weight.setter
    def weight(self, value):
       self.__weight = value

class Graph:
    def __init__(self, matrix = []):
        self.matrix = Matrix(matrix)

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

    def clear(self):
       self.matrix = Matrix()
       self.vertices = {}
       return self

    # Nacte vrcholy do matice
    # Vstup: vertices = {"vertexId1": "vertexName1", "vertexId2": "vertexName2", ... }
    # 
    def init_vertices(self, vertices: {}):
        self.clear()
           
        i = 0
        for id in vertices:
            row = [0] * len(vertices)
            row[i] = float('inf') 
            self.matrix.array.append(row)

            vertex = Vertex(id, vertices[id], i)
            self.vertices[id] = vertex

            i += 1
        return self

    # Vlozi hranu mezi dva vrcholy grafu
    def add_edge(self, edge: Edge):

        v1_index = self.vertices[edge.vertex_1.id]._index
        v2_index = self.vertices[edge.vertex_2.id]._index

        # Neorientovany graf -> symetricka matice
        self.matrix.array[v1_index][v2_index] = edge.weight
        self.matrix.array[v2_index][v1_index] = edge.weight

        return self
    

