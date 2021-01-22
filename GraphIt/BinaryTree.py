class TreeNode:
    def __init__(self, key = 0, data = None):
        self.key = key
        self.data = data
        self.left = None 
        self.right = None 

    def get_left(self):
        return self.left if self.left is not None else TreeNode()

    def get_right(self):
        return self.right if self.right is not None else TreeNode()

class BinaryTree:
    def __init__(self):
        self.top = None

    def add(self, key, data = None):
        if self.top is None:
            self.top = TreeNode(key, data)
        else:
            node = self.top
            while node is not None:
                if key < node.key:
                    if node.left is not None:
                        node = node.left
                    else:
                        node.left = TreeNode(key, data)
                        break
                elif key > node.key:
                    if node.right is not None:
                        node = node.right
                    else:
                        node.right = TreeNode(key, data)
                        break
                else:
                    raise Exception("Key collision error")

    def remove(self, key):
        node = self.top
        parent = None

        while node is not None:
            if key == node.key:
                if node.left is not None and node.right is not None:
                    node_1 = node.right
                    parent_1 = node
                    while node_1.left is not None:
                        parent_1 = node_1
                        node_1 = node_1.left
                    
                    parent_1.left = None

                    node_1.left = node.left
                    node_1.right = node.right

                    if key > parent.key:
                        parent.right = node_1
                    elif key < parent.key:
                        parent.left = node_1


                elif node.left is not None:
                    if key > parent.key:
                        parent.right = node.left
                    elif key < parent.key:
                        parent.left = node.left
                elif node.right is not None:
                    if key > parent.key:
                        parent.right = node.right
                    elif key < parent.key:
                        parent.left = node.right
                else:
                    if key > parent.key:
                        parent.right = None
                    elif key < parent.key:
                        parent.left = None
                break
            elif key < node.key:
                parent = node
                node = node.left
            elif key > node.key:
                parent = node
                node = node.right


    def find(self, key):
        node = self.top
        
        while node is not None:
            if key == node.key:
                return node.data
            elif key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right

    def print(self):
        print("="*20,"Binary tree","="*20)
        queue = []
        if self.top is not None: queue.append(self.top)
        
        while len(queue) > 0:
            node = queue.pop(0)
            print(node.key, "-left:", node.get_left().key, "-right:", node.get_right().key)
            if node.left is not None: queue.append(node.left)
            if node.right is not None: queue.append(node.right)

        print("="*53)



    
    


