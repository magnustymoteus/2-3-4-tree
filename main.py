from typing import List
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
class NodeArray:
    def __init__(self, nodes = None, parent=None):
        self.parent : NodeArray = parent
        self.arr : List[Node] = [] if nodes is None else nodes
        self.children : List[NodeArray] = []
    def print(self):
        for currentNode in self.arr:
            print(f"'{currentNode.key}'", end=" ")
        print()
    def setArr(self, arr):
        self.arr = arr
    def push(self, Node):
        self.arr.append(Node)
        self.arr.sort(key=getKeyOfNode)
    def setChildren(self, children):
        self.children = children
        for child in children:
            child.parent = self
    def isEmpty(self):
        return len(self.arr) == 0
    def hasEmptyChildren(self):
        return len(self.children) == 0
    def is4Node(self):
        return len(self.arr) == 3
    def isRoot(self):
        return self.parent is None
    def split(self):
        newNodes = NodeArray([self.arr[1]], self.parent)
        self.arr.pop(1)
        self.parent.children.append(newNodes)


def createTreeItem(key,val):
    return Node(key, val)
def getKeyOfNode(node):
    return node.key

class TwoThreeFourTree:
    def __init__(self):
        self.root : NodeArray = NodeArray()
    def isEmpty(self):
        return len(self.root.arr) == 0
    def retrieveItem(self, key):
        currentNodes = self.root
        while not currentNodes.hasEmptyChildren():
            if key < currentNodes.arr[0].key and currentNodes.children[0] is not None:
                currentNodes = currentNodes.children[0]
                break
            elif key > currentNodes.arr[len(currentNodes.arr)-1].key and currentNodes.children[len(currentNodes.children)-1] is not None:
                currentNodes = currentNodes.children[len(currentNodes.children)-1]
                break
            for x in range(len(currentNodes.arr)-1):
                if key > currentNodes.arr[x].key and key <= currentNodes.arr[x+1].key:
                    currentNodes = currentNodes.children[x+1]
                    break
            break
        for currentNode in currentNodes.arr:
            if key == currentNode.key:
                return (currentNode.value, True)
        return (None, False)
    '''def inorderTraverse(self, func, end=False, currentNode=None):
        if end == True:
            return
        if currentNode is None:
            currentNode = self.root
        isEnd = True if currentNode.hasEmptyChildren() else False
        self.inorderTraverse(func, isEnd, currentNode.children[0])
        for x in range(len())'''
    def insertItem(self, node):
        currentNodes = self.root
        while not currentNodes.isEmpty():
            if currentNodes.is4Node():
                isRoot = currentNodes.isRoot()
                middleNode = currentNodes.arr[1]
                currentNodes.arr.pop(1)
                if isRoot:
                    self.root = NodeArray([middleNode])
                    child1 = NodeArray([currentNodes.arr[0]], self.root)
                    child2 = NodeArray([currentNodes.arr[1]], self.root)
                    self.root.setChildren([child1, child2])
                else:
                    currentNodes.parent.push(middleNode)
                    currentNodes.split()
                if not currentNodes.hasEmptyChildren():
                    self.root.children[0].setChildren([currentNodes.children[0], currentNodes.children[1]])
                    self.root.children[1].setChildren([currentNodes.children[2], currentNodes.children[3]])
                currentNodes = self.root if isRoot else currentNodes.parent
            if not currentNodes.hasEmptyChildren():
                if node.key <= currentNodes.arr[0].key and currentNodes.children[0] is not None:
                    currentNodes = currentNodes.children[0]
                    break
                elif node.key > currentNodes.arr[len(currentNodes.arr)-1].key and currentNodes.children[len(currentNodes.children)-1] is not None:
                    currentNodes = currentNodes.children[len(currentNodes.children)-1]
                    break
                for x in range(len(currentNodes.arr)-1):
                    if node.key > currentNodes.arr[x].key and node.key <= currentNodes.arr[x+1].key:
                        currentNodes = currentNodes.children[x+1]
                        break
            else:
                break
        currentNodes.push(node)
        return True


t = TwoThreeFourTree()
print(t.isEmpty())
print(t.insertItem(createTreeItem(8, 8)))
print(t.insertItem(createTreeItem(5, 5)))
print(t.insertItem(createTreeItem(10, 10)))
print(t.insertItem(createTreeItem(15, 15)))
print(t.isEmpty())
print(t.retrieveItem(5)[0])
print(t.retrieveItem(5)[1])
t.root.children[1].print()
#t.inorderTraverse(print)
#print(t.save())
#t.load({'root': [10], 'children': [{'root': [5]}, {'root': [11]}]})
#t.insertItem(createTreeItem(15, 15))
#print(t.deleteItem(0))
#print(t.save())
#print(t.deleteItem(10))
#print(t.save())

'''
True
True
True
True
True
False
5
True
5
8
10
15
{'root': [8],'children':[{'root':[5]},{'root':[10,15]}]}
False
{'root': [10],'children':[{'root':[5]},{'root':[11,15]}]}
True
{'root': [11],'children':[{'root':[5]},{'root':[15]}]}
'''