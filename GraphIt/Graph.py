from Matrix import Matrix
from Vertex import Vertex
from Edge import Edge
import GraphEdgesHandler
import json
import copy

class Graph:
    def __init__(self):
        self.matrix = Matrix([])
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
        """
# =========================================================
# Vymazat vsechny hrany a vrcholy grafu
# =========================================================
        """
        self.matrix = Matrix()
        self.vertices = {}
        self.edges = []
        return self


    def load_fromFile(self, r_path):
        """
# =========================================================
# Nacte graf ze souboru
# ---------------------------------------------------------
# Struktura (JSON)
# graph:{
#   vertices:[
#       {
#           id: 1
#           name: "Vrchol 1"
#       },
#       {
#           id: 2
#           name: "Vrchol 1"
#       }
#   ]
#   edges:
#   [
#       {
#           weight: 4
#           vertex_1:{
#               id: 1
#           }
#           vertex_2:{
#               id: 2
#           }
#       },
#   ]
# }
# =========================================================
        """

        self.clear()

        file = open(r_path)
        data = json.load(file)
        j_graph = data["graph"]

        for j_vertex in j_graph["vertices"]:
            vertex = Vertex(j_vertex["id"], j_vertex["name"])
            self.add_vertex(vertex)

        for j_edge in j_graph["edges"]:
            edge = Edge(Vertex(j_edge["vertex_1"]["id"]), Vertex(j_edge["vertex_2"]["id"]), j_edge["weight"])
            self.add_edge(edge, "a")

        return self

   
    def add_vertex(self, vertex: Vertex):
        """
# =========================================================
# Pridat vrchol do grafu
# =========================================================
        """
        # Pokud vrchol uz existuje, aktualizuji jen jmeno
        if vertex.id in self.vertices:
            if vertex.name is not None:
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

    def add_vertices(self, vertices: []):
        """
# =========================================================
# Pridat vrcholy do grafu
# =========================================================
        """
        for vertex in vertices:
            self.add_vertex(vertex)
        return self

   
    def add_edge(self, edge: Edge, mode = "n"):
        """
# =========================================================
# Vlozit hranu mezi dva vrcholy grafu
# ---------------------------------------------------------
# Mode
# > mode = "n" ... vychozi hodnota, pokud nejsou vrcholy hrany v grafu, vyhodi vyjimku
# > mode = "a" ... pokud nejsou vrcholy hrany v grafu, pridam je
# =========================================================
        """

        if mode == "n":
            if not edge.vertex_1.id in self.vertices or not edge.vertex_2.id in self.vertices:
                raise Exception("No such a vertex in graph")
        elif mode == "a":
            if not edge.vertex_1.id in self.vertices:
                self.add_vertex(self, edge.vertex_1)
            if not edge.vertex_2.id in self.vertices:
                self.add_vertex(self, edge.vertex_2)

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
        """
# =========================================================
# Odstranit hranu z grafu
# =========================================================
        """
        # Indexy vrcholu v poli
        v1_index = self.vertices[edge.vertex_1.id]._index
        v2_index = self.vertices[edge.vertex_2.id]._index

        # Odstranim vzdalenost v matici
        self.matrix.array[v1_index][v2_index] = 0
        self.matrix.array[v2_index][v1_index] = 0

        # Odstranim hranu
        self.edges.remove(edge)

        return self


    def add_edges(self, edges: []):
        """
# =========================================================
# Vlozit vice hran do grafu
# =========================================================
        """
        for edge in edges:
            self.add_edge(edge)
        return self

   
    def is_connected(self): 
        """
# =========================================================
# Vraci True nebo False, zda je graf souvisly
# =========================================================
        """
        if len(self.vertices) < 1:
            return False

        count = 1
        visited = {}
        for key in self.vertices:
            visited[key] = False

        key = list(self.vertices.keys())[0]
        visited[key] = True

        queue = []
        while True:
            for edge in self.edges:
                if edge.vertex_1.id == key and not visited[edge.vertex_2.id]:
                    queue.append(edge.vertex_2.id)
                    visited[edge.vertex_2.id] = True
                    count += 1
                if edge.vertex_2.id == key and not visited[edge.vertex_1.id]:
                    queue.append(edge.vertex_1.id)
                    visited[edge.vertex_1.id] = True
                    count += 1

            if len(queue) < 1:
                break
            key = queue.pop(0)
                    
        
        return count == len(self.vertices)

  
    def is_tree(self):
        """
# =========================================================
# Vraci True nebo False, zda je graf strom.
# =========================================================
        """
        return len(self.edges) == len(self.vertices) - 1 

   
    def get_minSpanningTree(self):
        """
# =========================================================
# Vraci podgraf, ktery je minimalni kostrou grafu
# =========================================================
        """
        spanningTree = Graph()

        # Seradim hrany podle ohodnoceni
        sorted_edges = copy.deepcopy(self.edges)
        GraphEdgesHandler.sort(sorted_edges)

        while len(spanningTree.edges) < len(self.vertices) - 1 and len(sorted_edges) > 0: # Dokud nejsou hrany mezi vsemi vrcholy
            edge = sorted_edges.pop(0) # Hrana s nejnizsim ohodnocennim
            spanningTree.add_vertex(edge.vertex_1)
            spanningTree.add_vertex(edge.vertex_2)
            spanningTree.add_edge(edge)
            
            if not spanningTree.is_tree():
                spanningTree.remove_edge(edge)
        return spanningTree
     
    
    def min_distance(self, dist_arr, visited_arr): 
        """
# =========================================================
# Podpurna fce dijkstrova algoritmu, vraci nejkratsi vzdalenost k nenavstivenym vrcholum
# =========================================================
        """
        min_index = -1
        min = float('inf')
        #min_index = 0
        for v in range(len(self.vertices)): 
            if dist_arr[v] < min and visited_arr[v] == False: 
                min = dist_arr[v] 
                min_index = v 
        return min_index 

    
    def get_minDistDic(self, source: Vertex):
        """
# =========================================================
# Dijkstruv algoritmus, vraci dic minimalnich vzdalenosti ke vsem vrcholum
# =========================================================
        """
        count = len(self.vertices)

        dist_arr = [float('inf')] * count
        visited_arr = [False] * count
        dist_arr[self.vertices[source.id]._index] = 0
   
        for i in range(count): 
            v = self.min_distance(dist_arr, visited_arr) 
            if v == -1:
                continue
            visited_arr[v] = True
   
            for u in range(count): 
                if self.matrix.array[v][u] > 0 and visited_arr[u] == False and dist_arr[u] > dist_arr[v] + self.matrix.array[v][u]: 
                    dist_arr[u] = dist_arr[v] + self.matrix.array[v][u]

        dist_dic = {}
        for v_id in self.vertices: 
            dist_dic[v_id] = dist_arr[self.vertices[v_id]._index]

        return dist_dic


       
    def print(self):
        """
# =========================================================
# Vyprinti graf to konzole
# =========================================================
        """
        for edge in self.edges:
            print("Edge from [" + str(edge.vertex_1.id) + "] to [" + str(edge.vertex_2.id) + "] of weight " + str(edge.weight))

        return self

    def clone(self):
        """
# =========================================================
# Deep copy instance
# =========================================================
        """
        return copy.deepcopy(self)


    

