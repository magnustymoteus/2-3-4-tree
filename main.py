from typing import List
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
class NodeArray:
    def __init__(self, parent=None):
        self.parent = parent
        self.arr : List[Node] = []
        self.children : List[NodeArray] = []
    def setArr(self, arr):
        self.arr = arr
    def setChildren(self, children):
        self.children = children
    def isEmpty(self):
        return len(self.arr) == 0
    def hasEmptyChildren(self):
        return len(self.children) == 0


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
            elif key > currentNodes.arr[len(currentNodes.arr) - 1].key and currentNodes.children[
                len(currentNodes.children) - 1] is not None:
                currentNodes = currentNodes.children[len(currentNodes.children) - 1]
                break
            for x in range(len(currentNodes.arr) - 1):
                if key > currentNodes.arr[x].key and key < currentNodes.arr[x + 1].key:
                    currentNodes = currentNodes.children[x + 1]
                    break
        for currentNode in currentNodes.arr:
            if key == currentNode.key:
                return (currentNode.value, True)
        return (None, False)
    def insertItem(self, node):
        currentNodes = self.root
        while not currentNodes.hasEmptyChildren():
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

        if len(currentNodes.arr) < 3:
            currentNodes.arr.append(node)
            currentNodes.arr.sort(key=getKeyOfNode)
        else:
            pass
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