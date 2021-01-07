from Matrix import Matrix
from Vertex import Vertex
from Edge import Edge
from Stack import Stack
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
        Vymazat vsechny hrany a vrcholy grafu
        """
        self.matrix = Matrix([])
        self.vertices = {}
        self.edges = []
        return self


    def export_file(self, r_path):
        """
        Exportuje graf do souboru
        """

        file = open(r_path + ".json", "w")

        data = {}
        data["graph"] = {}
        data["graph"]["vertices"] = []
        data["graph"]["edges"] = []
        
        for v in self.vertices:
            data["graph"]["vertices"].append({"id": v, "name": self.vertices[v].name})

        for e in self.edges:
            data["graph"]["edges"].append({"vertex_1":{"id": e.vertex_1.id}, "vertex_2":{"id": e.vertex_2.id}, "weight": e.weight})

        json.dump(data, file)

        file.close()

        return self

    def import_file(self, r_path):
        """
        Nacte graf ze souboru
        """
        self.clear()

        file = open(r_path + ".json")
        data = json.load(file)
        j_graph = data["graph"]

        for j_vertex in j_graph["vertices"]:
            vertex = Vertex(j_vertex["id"], j_vertex["name"])
            self.set_vertex(vertex)

        for j_edge in j_graph["edges"]:
            edge = Edge(Vertex(j_edge["vertex_1"]["id"]), Vertex(j_edge["vertex_2"]["id"]), j_edge["weight"])
            self.set_edge(edge, "a")

        file.close()

        return self

    def set_vertex(self, vertex: Vertex):
        """
        Pridat vrchol do grafu

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

    def set_vertices(self, vertices: []):
        """
        Pridat vrcholy do grafu
        """
        for vertex in vertices:
            self.set_vertex(vertex)
        return self

   
    def set_edge(self, edge: Edge, mode = "n"):
        """
        Vlozit hranu mezi dva vrcholy grafu
        ---------------------------------------------------------
        Mode
        > mode = "n" ... vychozi hodnota, pokud nejsou vrcholy hrany v grafu, vyhodi vyjimku
        > mode = "a" ... pokud nejsou vrcholy hrany v grafu, pridam je
        """

        for e in self.edges:

            # Pokud hrana mezi vrcholy jiz existuje
            if (e.vertex_1.id == edge.vertex_1.id and e.vertex_2.id == edge.vertex_2.id) or (e.vertex_1.id == edge.vertex_2.id and e.vertex_2.id == edge.vertex_1.id):

                e.weight = edge.weight

                # Indexy vrcholu v poli
                v1_index = self.vertices[edge.vertex_1.id]._index
                v2_index = self.vertices[edge.vertex_2.id]._index

                # Neorientovany graf -> symetricka matice
                self.matrix.array[v1_index][v2_index] = edge.weight
                self.matrix.array[v2_index][v1_index] = edge.weight

                return self

        if mode == "n":
            if not edge.vertex_1.id in self.vertices or not edge.vertex_2.id in self.vertices:
                raise Exception("No such a vertex in graph")
        elif mode == "a":
            if not edge.vertex_1.id in self.vertices:
                self.set_vertex(edge.vertex_1)
            if not edge.vertex_2.id in self.vertices:
                self.set_vertex(edge.vertex_2)

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

    def remove_vertex(self, vertex: Vertex):
        """
        Odstranit vrchol z grafu
        """
        
        temp_v = {}
        temp_v.update(self.vertices)

        temp_e = []
        temp_e.extend(self.edges)

        self.clear()

        for v in temp_v:
            if temp_v[v].id == vertex.id:
                continue
            self.set_vertex(temp_v[v])

        
        for e in temp_e:
            if e.vertex_1.id== vertex.id or e.vertex_2.id== vertex.id:
                continue
            self.set_edge(e)

        return self

    def remove_edge(self, edge: Edge):
        """
        Odstranit hranu z grafu
        """
        # Indexy vrcholu v poli
        v1_index = self.vertices[edge.vertex_1.id]._index
        v2_index = self.vertices[edge.vertex_2.id]._index

        # Odstranim vzdalenost v matici
        self.matrix.array[v1_index][v2_index] = 0
        self.matrix.array[v2_index][v1_index] = 0
        
        # Odstranim hranu
        for i in range(len(self.edges)):
            e = self.edges[i]
            if e.vertex_1.id == edge.vertex_1.id and e.vertex_2.id == edge.vertex_2.id:
                self.edges.remove(e)
                i -= 1

        return self


    def set_edges(self, edges: []):
        """
        Vlozit vice hran do grafu
        """
        for edge in edges:
            self.set_edge(edge)
        return self

   
    def is_connected(self): 
        """
        Vraci True nebo False, zda je graf souvisly
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

    def get_vertexEdges(self, vertex: Vertex, exception):
        """
        Vraci hrany vedouci od vrcholu
        Parametr exception rika, ze pokud hrana obsahuje vrchol s danym id, tak ji nevracim
        """
        edges = []
        for e in self.edges:
            if e.vertex_1.id == vertex.id or e.vertex_2.id == vertex.id:
                if e.vertex_1.id != exception and e.vertex_2.id != exception:
                    edges.append(e)

        return edges
  
    def is_tree(self):
        """
        Vraci True nebo False, zda je graf strom.
        """
        return len(self.edges) == len(self.vertices) - 1 and self.is_connected()
    
    def contains_cycle(self):
        """
        Obsahuje graf cyklus
        """
        cycle = False

        if len(self.vertices) == 0:
            return False

        visited = {}
        for v in self.vertices:
            visited[v] = False

        key = list(self.vertices.keys())[0]
        visited[key] = True

        prev_key = ""

        queue = []
        while not cycle:
            for edge in self.get_vertexEdges(Vertex(key), prev_key):
                if visited[edge.vertex_1.id] and edge.vertex_1.id != key:
                    cycle = True
                    break
                if visited[edge.vertex_2.id] and edge.vertex_2.id != key:
                    cycle = True
                    break

                if edge.vertex_1.id != key:
                    queue.append((edge.vertex_1.id, key))
                if edge.vertex_2.id != key:
                    queue.append((edge.vertex_2.id, key))
            
            if len(queue) < 1:
                for e in self.edges:
                    if not visited[e.vertex_1.id]:
                        queue.append((e.vertex_1.id,""))
                        key = ""
                        break
                    if not visited[e.vertex_2.id]:
                        queue.append((e.vertex_2.id,""))
                        key = ""
                        break
                if len(queue) < 1:
                    break

            
            k = queue.pop(0)
            key = k[0]
            prev_key = k[1]
            visited[key] = True

        return cycle

   
    def get_minSpanningTree(self):
        """
        Vraci podgraf, ktery je minimalni kostrou grafu (Kruskaluv algoritmus)
        """
        spanningTree = Graph()

        # Seradim hrany podle ohodnoceni
        sorted_edges = []
        sorted_edges.extend(self.edges)
        GraphEdgesHandler.sort(sorted_edges)

        while len(spanningTree.edges) < len(self.vertices) - 1 and len(sorted_edges) > 0: # Dokud nejsou hrany mezi vsemi vrcholy
            edge = sorted_edges.pop(0) # Hrana s nejnizsim ohodnocennim
            spanningTree.set_vertex(edge.vertex_1)
            spanningTree.set_vertex(edge.vertex_2)
            spanningTree.set_edge(edge)
            
            if spanningTree.contains_cycle():
                spanningTree.remove_edge(edge)
        return spanningTree

    def get_neighbours(self, vertex):
        """
        Vraci sousedy vcholu a ohodnoceni hran k nim vedoucich
        """
        neighbours = {}
            
        for edge in self.edges:
            if edge.vertex_1.id == vertex:
                neighbours[edge.vertex_2.id] = edge.weight
            if edge.vertex_2.id == vertex:
                neighbours[edge.vertex_1.id] = edge.weight

        return neighbours

    def find_route(self, source : Vertex, dest : Vertex):
        """
        Najde nejktratsi cestu mezi vrcholy
        """

        distances = {}
        previous_vertices = {}

        for v in self.vertices:
            distances[v] = float("inf")
            previous_vertices[v] = None

        distances[source.id] = 0
        vertices = {}
        vertices.update(self.vertices)

        while len(vertices) > 0:
            current_vertex = min(vertices, key = lambda v: distances[v])
            vertices.pop(current_vertex)
            if distances[current_vertex] == float("inf"):
                break
            
            neighbours = self.get_neighbours(current_vertex)
            for neighbour in neighbours:
                weight = neighbours[neighbour]
                distance = distances[current_vertex] + weight
                
                if distance < distances[neighbour]:
                    distances[neighbour] = distance
                    previous_vertices[neighbour] = current_vertex

        route = []

        current_vertex = dest.id
        while previous_vertices[current_vertex] is not None:
            route.append((current_vertex, distances[current_vertex]))
            current_vertex = previous_vertices[current_vertex]
        
        if len(route) > 0:
             route.append((current_vertex, distances[current_vertex]))

        route.reverse()

        return route

    def get_vertexByIndex(self, index):
        """
        Vrati vrchol podle indexu
        """

        for v in self.vertices:
            if self.vertices[v]._index == index:
                return v

        return None

       
    def print(self):
        """
        Vyprinti graf to konzole
        
        """
        lc = 12

        print("=" * lc, "VERTICES", "=" * lc)
        for vertex_id in self.vertices:
            print("Vertex [" + str(vertex_id) + "] - " + self.vertices[vertex_id].name)

        print("=" * lc, "EDGES", "=" * lc)
        for edge in self.edges:
            print("Edge from [" + str(edge.vertex_1.id) + ", (" + self.vertices[edge.vertex_1.id].name + ")] to [" + str(edge.vertex_2.id) + ", (" + self.vertices[edge.vertex_2.id].name + ")] of weight " + str(edge.weight))

        return self

    def clone(self):
        """
        Deepclone
        """
        return copy.deepcopy(self)


    

