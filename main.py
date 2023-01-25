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
    def getArrayOfKeys(self):
        arr = []
        for node in self.arr:
            arr.append(node.key)
        return arr
    def setArr(self, arr):
        self.arr = arr
    def push(self, Node : Node):
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
        index = self.parent.children.index(self)
        self.parent.children.insert(index+1, newNodes)


def createTreeItem(key,val):
    return Node(key, val)
def getKeyOfNode(node):
    return node.key
def getIndexOfKeyInNodes(nodes : NodeArray, key):
    for x in range(len(nodes.arr)):
        if nodes.arr[x].key == key:
            return x
def findNodeSuccessor(nodes : NodeArray, key):
    index = getIndexOfKeyInNodes(nodes, key)
    currentNode = nodes.children[index+1]
    while not currentNode.hasEmptyChildren():
        currentNode = currentNode.children[0]
    return currentNode


class TwoThreeFourTree:
    def __init__(self):
        self.root : NodeArray = NodeArray()
    def isEmpty(self):
        return len(self.root.arr) == 0
    def retrieveItem(self, key, returnNode=False):
        currentNodes = self.root
        while not currentNodes.hasEmptyChildren():
            if key < currentNodes.arr[0].key and currentNodes.children[0] is not None:
                currentNodes = currentNodes.children[0]
                continue
            elif key > currentNodes.arr[len(currentNodes.arr)-1].key and currentNodes.children[len(currentNodes.children)-1] is not None:
                currentNodes = currentNodes.children[len(currentNodes.children)-1]
                continue
            for x in range(len(currentNodes.arr)-1):
                if key > currentNodes.arr[x].key and key <= currentNodes.arr[x+1].key:
                    currentNodes = currentNodes.children[x+1]
                    break
            break
        for currentNode in currentNodes.arr:
            if key == currentNode.key:
                return (currentNode.value, True) if not returnNode else (currentNodes, True)
        return (None, False)
    def inorderTraverse(self, func, currentNode=None):
        if currentNode is None:
            currentNode = self.root
        elif currentNode.isEmpty():
            return
        for x in range(len(currentNode.arr)):
            if not currentNode.hasEmptyChildren():
                self.inorderTraverse(func, currentNode.children[x])
            func(currentNode.arr[x].key)
        if not currentNode.hasEmptyChildren():
            self.inorderTraverse(func, currentNode.children[len(currentNode.children)-1])
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
                if node.key < currentNodes.arr[0].key and currentNodes.children[0] is not None:
                    currentNodes = currentNodes.children[0]
                    continue
                elif node.key > currentNodes.arr[len(currentNodes.arr)-1].key and currentNodes.children[len(currentNodes.children)-1] is not None:
                    currentNodes = currentNodes.children[len(currentNodes.children)-1]
                    continue
                for x in range(len(currentNodes.arr)-1):
                    if currentNodes.arr[x].key < node.key < currentNodes.arr[x + 1].key:
                        currentNodes = currentNodes.children[x + 1]
                        continue
            else:
                break
        currentNodes.push(node)
        return True
    def save(self, currentNode=None):
        if currentNode is None:
            currentNode = self.root
        elif currentNode.isEmpty():
            return
        currentStr = "{'root': "+str(currentNode.getArrayOfKeys())
        if not currentNode.hasEmptyChildren():
            currentStr += ",'children':["
            for child in currentNode.children:
                currentStr += self.save(child)+","
            currentStr = currentStr[:-1]
            currentStr += "]"
        currentStr += "}"
        return currentStr
    def load(self, dict, currentNode : NodeArray = None):
        if currentNode is None:
            currentNode = NodeArray([])
            self.root = currentNode
        for key in dict.get('root'):
            newNode = Node(key, key)
            currentNode.arr.append(newNode)
        if "children" in dict:
            for child in dict.get("children"):
                childNode = NodeArray(None, currentNode)
                currentNode.children.append(childNode)
                self.load(child, childNode)
    def deleteItem(self, key):
        toBeDeletedResult = self.retrieveItem(key, True)
        deletedNodes : NodeArray = toBeDeletedResult[0]
        foundNode = toBeDeletedResult[1]
        if not foundNode:
            return False
        else:
            if not deletedNodes.hasEmptyChildren():
                successorNodes = findNodeSuccessor(deletedNodes, key)
                successorNode = successorNodes.arr[0]
                successorNodes.arr.pop(0)
                indexOfDeletedNode = getIndexOfKeyInNodes(deletedNodes, key)
                deletedNodes.arr[indexOfDeletedNode] = successorNode
            else:
                currentNodes = self.root
                while not currentNodes.hasEmptyChildren():
                    if key < currentNodes.arr[0].key and currentNodes.children[0] is not None:
                        currentNodes = currentNodes.children[0]
                        break
                    elif key > currentNodes.arr[len(currentNodes.arr) - 1].key and currentNodes.children[
                        len(currentNodes.children) - 1] is not None:
                        currentNodes = currentNodes.children[len(currentNodes.children) - 1]
                        break
                    for x in range(len(currentNodes.arr) - 1):
                        if key > currentNodes.arr[x].key and key <= currentNodes.arr[x + 1].key:
                            currentNodes = currentNodes.children[x + 1]
                            break
                    break
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
t.inorderTraverse(print)
print(t.save())
t.insertItem(createTreeItem(15, 15))
print(t.deleteItem(0))
print(t.save())
print(t.deleteItem(10))
print(t.save())

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