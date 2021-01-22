from GraphIt import Console, Graph, Edge, Vertex
import Maths
from BinaryTree import BinaryTree

bt = BinaryTree()
bt.add(2,"Dvojka")
bt.add(1,"Jednicka")
bt.add(3,"Trojka")
bt.add(6,"Sestka")
bt.add(9,"Devitka")
bt.add(4,"Ctyrka")
bt.add(5,"Petka")
bt.add(7,"Sedmicka")
bt.print()
bt.remove(6)
bt.print()
