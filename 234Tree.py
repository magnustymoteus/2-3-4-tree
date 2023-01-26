from typing import List


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class NodeArray:
    def __init__(self, nodes=None, parent=None):
        self.parent: NodeArray = parent
        self.arr: List[Node] = [] if nodes is None else nodes
        self.children: List[NodeArray] = []

    def print(self):
        for currentNode in self.arr:
            print(f"'{currentNode.key}'", end=" ")
        print()

    def getArrayOfKeys(self):
        arr = []
        for node in self.arr:
            arr.append(node.key)
        return arr

    def getIndexOfChild(self, parentNodes):
        for x in range(len(parentNodes.children)):
            if parentNodes.children[x].arr == self.arr:
                return x

    def has3NodeOr4NodeSibling(self):
        index = self.getIndexOfChild(self.parent)
        if index > 0:
            if len(self.parent.children[index - 1].arr) > 1:
                return self.parent.children[index - 1], True
            elif index != len(self.parent.children) - 1:
                if len(self.parent.children[index + 1].arr) > 1:
                    return self.parent.children[index + 1], True
        elif len(self.parent.children[index + 1].arr) > 1:
            return self.parent.children[index + 1], True
        return None, False

    def hasAll2NodeSiblings(self):
        index = self.getIndexOfChild(self.parent)
        if index == 0 and self.parent.children[1].is2Node():
            return self.parent.children[1], True
        elif index == len(self.parent.children) - 1 and self.parent.children[index - 1].is2Node():
            return self.parent.children[index - 1], True
        elif self.parent.children[index - 1].is2Node() and self.parent.children[index + 1].is2Node():
            return self.parent.children[index - 1], True
        return None, False

    def has2NodeSibling(self):
        index = self.getIndexOfChild(self.parent)
        sibling = self.parent.children[0] if index > 0 else self.parent.children[1]
        return sibling, sibling.is2Node()

    def setArr(self, arr):
        self.arr = arr

    def push(self, node: Node):
        self.arr.append(node)
        self.arr.sort(key=getKeyOfNode)

    def setChildren(self, children):
        self.children = children
        for child in children:
            child.parent = self

    def isEmpty(self):
        return len(self.arr) == 0

    def remove(self, index):
        self.arr.pop(index)
        if self.isEmpty() and not self.isRoot():
            self.parent.children.pop(self.getIndexOfChild(self.parent))

    def hasEmptyChildren(self):
        return len(self.children) == 0

    def is4Node(self):
        return len(self.arr) == 3

    def is3Node(self):
        return len(self.arr) == 2

    def is2Node(self):
        return len(self.arr) == 1

    def isRoot(self):
        return self.parent is None

    def split(self):
        newNodes = NodeArray([self.arr[1]], self.parent)
        self.remove(1)
        index = self.parent.children.index(self)
        self.parent.children.insert(index + 1, newNodes)

    def getBelongingParentIndex(self, siblingIndex):
        return (self.getIndexOfChild(self.parent) + siblingIndex) // 2

    def getIndexOfKeyInNodes(self, key):
        for x in range(len(self.arr)):
            if self.arr[x].key == key:
                return x


def createTreeItem(key, val):
    return Node(key, val)


def getKeyOfNode(node):
    return node.key


class TwoThreeFourTree:
    def __init__(self):
        self.root: NodeArray = NodeArray()

    def isEmpty(self):
        return len(self.root.arr) == 0

    def findNodeSuccessor(self, currentNodes, key):
        index = currentNodes.getIndexOfKeyInNodes(key)
        currentNode = self.adjustNodeForDeletion(currentNodes.children[index + 1])
        while not currentNode.hasEmptyChildren():
            currentNode = self.adjustNodeForDeletion(currentNode.children[0])
        return currentNode

    def adjustNodeForDeletion(self, currentNodes):
        if not currentNodes.isRoot() and currentNodes.is2Node():
            if currentNodes.has3NodeOr4NodeSibling()[1]:
                siblingNodes = currentNodes.has3NodeOr4NodeSibling()[0]
                indexOfSibling = siblingNodes.getIndexOfChild(siblingNodes.parent)
                indexOfCurrent = currentNodes.getIndexOfChild(currentNodes.parent)
                indexOfParent = currentNodes.getBelongingParentIndex(indexOfSibling)
                deletionIndex = 0 if indexOfSibling > indexOfCurrent else len(siblingNodes.arr) - 1
                siblingNode = siblingNodes.arr[deletionIndex]
                siblingNodes.remove(deletionIndex)
                parentNode = currentNodes.parent.arr[indexOfParent]
                currentNodes.parent.remove(indexOfParent)
                currentNodes.parent.push(siblingNode)
                currentNodes.push(parentNode)
            elif currentNodes.parent.is2Node() and currentNodes.has2NodeSibling()[1]:
                siblingNodes = currentNodes.has2NodeSibling()[0]
                siblingNode = siblingNodes.arr[0]
                parentNode = currentNodes.parent.arr[0]
                indexOfCurrent = currentNodes.getIndexOfChild(currentNodes.parent)
                indexOfSibling = siblingNodes.getIndexOfChild(siblingNodes.parent)
                self.root = NodeArray()
                self.root.push(currentNodes.arr[0])
                self.root.push(parentNode)
                self.root.push(siblingNode)
                if indexOfSibling < indexOfCurrent:
                    self.root.setChildren(siblingNodes.children + currentNodes.children)
                else:
                    self.root.setChildren(currentNodes.children + siblingNodes.children)
                return self.root
            elif currentNodes.hasAll2NodeSiblings()[1] and (
                    currentNodes.parent.is3Node() or currentNodes.parent.is4Node()):
                siblingNodes = currentNodes.hasAll2NodeSiblings()[0]
                indexOfSibling = siblingNodes.getIndexOfChild(siblingNodes.parent)
                indexOfCurrent = currentNodes.getIndexOfChild(currentNodes.parent)
                indexOfParent = currentNodes.getBelongingParentIndex(indexOfSibling)
                parentNode = currentNodes.parent.arr[indexOfParent]
                currentNodes.parent.remove(indexOfParent)
                currentNodes.parent.children.pop(indexOfSibling)
                currentNodes.push(parentNode)
                currentNodes.push(siblingNodes.arr[0])
                if indexOfSibling < indexOfCurrent:
                    currentNodes.setChildren(siblingNodes.children + currentNodes.children)
                else:
                    currentNodes.setChildren(currentNodes.children + siblingNodes.children)
        return currentNodes

    def retrieveItem(self, key, returnNode=False):
        currentNodes = self.root
        while not currentNodes.hasEmptyChildren():
            if key < currentNodes.arr[0].key and currentNodes.children[0] is not None:
                currentNodes = currentNodes.children[0]
                continue
            elif key > currentNodes.arr[len(currentNodes.arr) - 1].key and currentNodes.children[
                len(currentNodes.children) - 1] is not None:
                currentNodes = currentNodes.children[len(currentNodes.children) - 1]
                continue
            for x in range(len(currentNodes.arr) - 1):
                if currentNodes.arr[x].key < key < currentNodes.arr[x + 1].key:
                    currentNodes = currentNodes.children[x + 1]
                    break
            break
        for currentNode in currentNodes.arr:
            if key == currentNode.key:
                return (currentNode.value, True) if not returnNode else (currentNodes, True)
        return None, False

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
            self.inorderTraverse(func, currentNode.children[len(currentNode.children) - 1])

    def insertItem(self, node):
        currentNodes = self.root
        while not currentNodes.isEmpty():
            if currentNodes.is4Node():
                isRoot = currentNodes.isRoot()
                middleNode = currentNodes.arr[1]
                currentNodes.remove(1)
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
                elif node.key > currentNodes.arr[len(currentNodes.arr) - 1].key and currentNodes.children[
                    len(currentNodes.children) - 1] is not None:
                    currentNodes = currentNodes.children[len(currentNodes.children) - 1]
                    continue
                for x in range(len(currentNodes.arr) - 1):
                    if currentNodes.arr[x].key < node.key < currentNodes.arr[x + 1].key:
                        currentNodes = currentNodes.children[x + 1]
                        continue
            else:
                break
        currentNodes.push(node)
        return True

    def save(self, currentNode: NodeArray = None):
        if currentNode is None:
            currentNode = self.root
        elif currentNode.isEmpty():
            return
        currentStr = "{'root': " + str(currentNode.getArrayOfKeys())
        if not currentNode.hasEmptyChildren():
            currentStr += ",'children':["
            for child in currentNode.children:
                currentStr += self.save(child) + ","
            currentStr = currentStr[:-1]
            currentStr += "]"
        currentStr += "}"
        return currentStr

    def load(self, dict, currentNode: NodeArray = None):
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
        deletedNodes: NodeArray = toBeDeletedResult[0]
        foundNode = toBeDeletedResult[1]
        if not foundNode:
            return False
        if not deletedNodes.hasEmptyChildren():
            successorNodes = self.findNodeSuccessor(deletedNodes, key)
            successorNode = successorNodes.arr[0]
            successorNodes.remove(0)
            indexOfDeletedNode = deletedNodes.getIndexOfKeyInNodes(key)
            deletedNodes.arr[indexOfDeletedNode] = successorNode
            return True
        elif deletedNodes.is2Node():
            currentNodes = self.root
            foundInLoop = False
            while not currentNodes.isEmpty():
                currentNodes = self.adjustNodeForDeletion(currentNodes)
                if foundInLoop:
                    break
                if key < currentNodes.arr[0].key and currentNodes.children[0] is not None:
                    currentNodes = currentNodes.children[0]
                    continue
                elif key > currentNodes.arr[len(currentNodes.arr) - 1].key and currentNodes.children[
                    len(currentNodes.children) - 1] is not None:
                    currentNodes = currentNodes.children[len(currentNodes.children) - 1]
                    continue
                for x in range(len(currentNodes.arr) - 1):
                    if key > currentNodes.arr[x].key and key <= currentNodes.arr[x + 1].key:
                        currentNodes = currentNodes.children[x + 1]
                        foundInLoop = True
            currentNodes.remove(currentNodes.getIndexOfKeyInNodes(key))
        else:
            deletedNodes.remove(deletedNodes.getIndexOfKeyInNodes(key))
        return True


t = TwoThreeFourTree()
t.load({'root': [5], 'children': [{'root': [2], 'children': [{'root': [1]}, {'root': [3, 4]}]},
                                  {'root': [12], 'children': [{'root': [10]}, {'root': [13, 15, 16]}]}]})
t.deleteItem(13)
t.deleteItem(10)
print(t.save())
t.deleteItem(16)
print(t.save())
