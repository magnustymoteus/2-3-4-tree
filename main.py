from typing import List
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
class NodeArray:
    def __init__(self, leftChild=None, rightChild=None):
        self.arr : List[Node] = []
        self.leftChild : NodeArray = leftChild
        self.rightChild : NodeArray = rightChild
    def setArr(self, arr):
        self.arr = arr
    def setLeftChild(self, leftChild):
        self.leftChild = leftChild
    def setRightChild(self, rightChild):
        self.rightChild = rightChild
    def isEmpty(self):
        return len(self.arr) == 0


def createTreeItem(key,val):
    return Node(key, val)
def getKeyOfNode(node):
    return node.key

class TwoThreeFourTree:
    def __init__(self):
        self.root : NodeArray = NodeArray()
    def isEmpty(self):
        return len(self.root.arr) == 0
    def insertItem(self, node):
        currentNodes : NodeArray = self.root
        while(not currentNodes.isEmpty()):
            if currentNodes.arr[0].key > node.key:
                if currentNodes.leftChild is not None:
                    currentNodes = currentNodes.leftChild
                else:
                    break
            elif currentNodes.arr[len(currentNodes.arr)-1].key < node.key:
                if currentNodes.rightChild is not None:
                    currentNodes = currentNodes.rightChild
                else:
                    break
        if len(currentNodes.arr) < 3:
            currentNodes.arr.append(node)
            currentNodes.arr.sort(key=getKeyOfNode)

t = TwoThreeFourTree()
print(t.isEmpty())
print(t.insertItem(createTreeItem(8, 8)))
print(t.insertItem(createTreeItem(5, 5)))
print(t.insertItem(createTreeItem(10, 10)))
#print(t.insertItem(createTreeItem(15, 15)))
#print(t.isEmpty())
#print(t.retrieveItem(5)[0])
#print(t.retrieveItem(5)[1])
#t.inorderTraverse(print)
#print(t.save())
#t.load({'root': [10], 'children': [{'root': [5]}, {'root': [11]}]})
#t.insertItem(createTreeItem(15, 15))
#print(t.deleteItem(0))
#print(t.save())
#print(t.deleteItem(10))
#print(t.save())