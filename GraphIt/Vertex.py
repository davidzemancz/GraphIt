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
