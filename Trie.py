# Node class
class Node:
    def __init__(self):
        self.isWord = False
        self.children = {}

# Trie class
class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word: str) -> None:
        currentNode = self.root
        for char in word:
            if char not in currentNode.children:
                currentNode.children[char] = Node()
            currentNode = currentNode.children[char]
        currentNode.isWord = True

    def search(self, word: str) -> bool:
        currentNode = self.root
        for char in word:
            if char not in currentNode.children:
                return False
            currentNode = currentNode.children[char]
        return currentNode.isWord

    def starts_with(self, prefix: str) -> bool:
        currentNode = self.root
        for char in prefix:
            if char not in currentNode.children:
                return False
            currentNode = currentNode.children[char]
        return True

    def get_similar_words(self, prefix: str) -> list:
        if not self.starts_with(prefix):
            return []

        similarWords = []
        currentNode = self.root

        # Traverse to the node corresponding to the prefix
        for char in prefix:
            currentNode = currentNode.children[char]

        # Call a recursive function to find similar words starting from the currentNode
        self._find_similar_words(currentNode, prefix, similarWords)

        return similarWords

    def _find_similar_words(self, node: Node, word: str, similar_words: list):
        if node.isWord:
            similar_words.append(word)

        for char, childNode in node.children.items():
            self._find_similar_words(childNode, word + char, similar_words)
    
    def delete(self, word: str) -> bool:
        if not self.search(word):
            return False

        nodes_traversed = []
        currentNode = self.root
        for char in word:
            nodes_traversed.append((currentNode, char))
            currentNode = currentNode.children[char]
            
        currentNode.isWord = False

        if len(currentNode.children) == 0 and not currentNode.isWord:
            for node, char in reversed(nodes_traversed):
                del node.children[char]
                if len(node.children) > 0 or node.isWord:
                    break
        return True