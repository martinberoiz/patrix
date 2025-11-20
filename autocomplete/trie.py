class Trie:

    def __init__(self, key_value_pairs):
        self.root = TrieNode()
        for key, value in key_value_pairs:
            if key == "":
                raise ValueError("Key cannot be empty")
            if not isinstance(key, str):
                raise ValueError("Key must be a string")
            self.root.insert(key, value)

    def as_dict(self):
        return self.root.as_dict()


class TrieNode:

    def __init__(self):
        self.children = {}
        self.value = None

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
        child.insert(suffix, value)

    def as_dict(self):
        return {k: v.as_dict() for k, v in self.children.items()}
