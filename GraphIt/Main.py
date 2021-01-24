from GraphIt import Console, Graph, Edge, Vertex
import Maths
from BinaryTree import BinaryTree
from Heap import Heap

h = Heap()
h.build([15,14,11,16,9,10,7,5,8,6])
h.print()
print(h.check())
print(h.sort())