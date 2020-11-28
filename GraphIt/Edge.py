from Vertex import Vertex

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
