class Node:
    """Class for the nodes wich makes up the trie structure """
    def __init__(self, char):
        self.char = char
        self.children = []
    
def add(root, word):
    """Add a word to a trie with the given root"""
    node = root
    for char in word:
        char_found = False
        for child in node.children:
            if child.char == char:
                char_found = True
                node = child
                break
        if not char_found:
            appended_node = Node(char)
            node.children += [appended_node]
            node = appended_node 

def find(root,word):
    """Returns true if a given words can be found in a trie with the given root """
    node = root
    if not node.children:
        return False
    for char in word:
        char_found = False
        for child in node.children:
            if char == child.char:
                char_found = True
                node = child
                break
        if not char_found:
            return False
    return True

def print_trie(root):
    """Basic print function used for debugging purposes"""
    node = root
    if not node.children:
        print(node.char + " END")    
        return
    print(node.char + " children: "+str(len(node.children)))
    for child in node.children:
        print_trie(child)