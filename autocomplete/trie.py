class Trie:

    def __init__(self, key_value_pairs):
        self.root = TrieNode()
        for key, value in key_value_pairs:
            self.insert(key, value)

    def insert(self, key, value):
        if key == "":
            raise ValueError("Key cannot be empty")
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        self.root.insert(key, value)

    def search(self, word):
        if word == "":
            raise ValueError("Word cannot be empty")
        if not isinstance(word, str):
            raise ValueError("Word must be a string")
        return self.root.search(word)

    def as_dict(self):
        return self.root.as_dict()


class TrieNode:

    def __init__(self):
        self.children = {}
        self.value = None
        self.parent = None
        self.prefix = ""

    def insert(self, key, value):
        if len(key) == 0:
            self.value = value
            return self
        prefix, suffix = key[0], key[1:]
        if prefix in self.children:
            child = self.children[prefix]
            child.insert(suffix, value)
            return

        # If there is no children with that key, create one
        child = TrieNode()
        self.children[prefix] = child
        child.parent = self
        child.prefix = prefix
        child.insert(suffix, value)

    def search(self, word):
        if len(word) == 1:
            return self.children.get(word)
        char = word[0]
        if char not in self.children:
            return None
        return self.children[char].search(word[1:])

    def as_dict(self):
        return {k: v.as_dict() for k, v in self.children.items()}

    def get_key(self):
        if self.parent is None:
            return ""
        return self.parent.get_key() + self.prefix
