"""
Radix tree (also known as a compressed trie or compact prefix tree) implementation.

This module provides a RadixTree data structure that stores key-value pairs efficiently
by compressing common prefixes. Unlike a standard trie, a radix tree compresses nodes
that have only one child, reducing memory usage while maintaining fast prefix-based
lookups and insertions.
"""


class RadixTree:
    """
    A radix tree data structure for key-value pairs storage with compressed prefixes.

    The RadixTree compresses common prefixes among keys, making it more memory-efficient
    than a standard trie while maintaining fast insertion and lookup operations.

    Attributes
    ----------
    root : RadixNode
        The root node of the radix tree.
    """

    def __init__(self, key_value_pairs):
        """
        Initialize a RadixTree with a collection of key-value pairs.

        Parameters
        ----------
        key_value_pairs : iterable
            An iterable of (key, value) tuples to insert into the tree.
            Each key must be a non-empty string.

        Raises
        ------
        ValueError
            If any key is empty or not a string.
        """
        self.root = RadixNode()
        for key, value in key_value_pairs:
            self.insert(key, value)

    def insert(self, key, value):
        """
        Insert a key-value pair into the radix tree.

        If the key already exists, its value will be updated. The tree structure
        is automatically compressed to share common prefixes among keys.

        Parameters
        ----------
        key : str
            The key to insert. Must be a non-empty string.
        value
            The value to associate with the key.

        Raises
        ------
        ValueError
            If key is empty or not a string.
        """
        if key == "":
            raise ValueError("Key cannot be empty")
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        self.root.insert(key, value)

    def completions(self, key):
        """
        Return possible completions for the given key.

        Parameters
        ----------
        key : str
            The key to search for.

        Returns
        -------
        list
            A list of possible completions for the given key.
        """
        return self.root.completions(key)

    def as_dict(self):
        """
        Convert the radix tree to a nested dictionary representation.

        Returns
        -------
        dict
            A nested dictionary where each key is a prefix and the value
            is either another dictionary (for nodes with children) or None.
            Note: This representation does not preserve the values stored
            in leaf nodes, only the tree structure.
        """
        return self.root.as_dict()

    @property
    def height(self):
        """
        Height of the radix tree.
        """
        # Subtract 1 to exclude the root node
        return self.root.height - 1

    @property
    def size(self):
        """
        Size of the radix tree.
        """
        return self.root.size

    @property
    def total_chars(self):
        """
        Total number of characters stored in all prefixes of the radix tree.

        This represents the compressed size of the tree. Compare this to the
        sum of len(key) for all keys to calculate the compression rate.
        """
        return self.root.total_chars


class RadixNode:
    """
    A node in the radix tree data structure.

    Each node stores a prefix (shared part of keys), an optional value,
    references to child nodes, and a reference to its parent node.

    Attributes
    ----------
    children : dict
        Dictionary mapping prefix strings to child RadixNode instances.
    value
        The value stored at this node (None if this is not a leaf node).
    parent : RadixNode, optional
        Reference to the parent node (None for root).
    prefix : str
        The prefix string associated with this node.
    """

    def __init__(self, prefix="", value=None, parent=None):
        """
        Initialize a RadixNode.

        Parameters
        ----------
        value : any, optional
            The value to store at this node. Defaults to None.
        prefix : str, optional
            The prefix string for this node. Defaults to empty string.
        parent : RadixNode, optional
            The parent node. Defaults to None.
        """
        self.children = {}
        self.value = value
        self.parent = parent
        self.prefix = prefix

    def insert(self, key, value):
        """
        Insert a key-value pair into the subtree rooted at this node.

        This method handles the radix tree compression logic:
        - If no common prefix exists with existing children, creates a new child
        - If the key exactly matches an existing prefix, updates that child's value
        - If the key shares a prefix with an existing child, recursively inserts
        - If the key partially matches a child's prefix, splits the node to preserve
          the tree structure while maintaining compression

        Parameters
        ----------
        key : str
            The key to insert. Must be non-empty.
        value
            The value to associate with the key.
        """
        # Look for a node to insert the key into
        common_prefix, existing_prefix, existing_child = self._find_common_prefix_child(
            key
        )

        # Case 1: No common prefix found - create a new child node
        if existing_child is None:
            self.children[key] = RadixNode(key, value, parent=self)
            return

        # Case 2: Exact match - key matches an existing child's prefix exactly
        if common_prefix == existing_prefix == key:
            existing_child.value = value
            return

        # Case 3: Key extends beyond the common prefix - recursively insert
        # into existing child
        if common_prefix == existing_prefix:
            remaining_key = key[len(common_prefix) :]
            existing_child.insert(remaining_key, value)
            return

        # Case 4: Key and existing child share a prefix but diverge - split the node
        # Create an intermediate node to hold the common prefix
        intermediate_node = RadixNode(common_prefix, None, parent=self)
        self.children[common_prefix] = intermediate_node

        # Move the existing child under the intermediate node with its remaining prefix
        remaining_existing_prefix = existing_prefix[len(common_prefix) :]
        intermediate_node.children[remaining_existing_prefix] = existing_child
        existing_child.prefix = remaining_existing_prefix
        existing_child.parent = intermediate_node

        # Create a new child for the key under the intermediate node
        remaining_key = key[len(common_prefix) :]
        intermediate_node.children[remaining_key] = RadixNode(
            remaining_key, value, parent=intermediate_node
        )

        # Remove the old reference to the existing child under its original prefix
        del self.children[existing_prefix]

    def completions(self, key):
        """
        Return possible completions for the given key.

        Parameters
        ----------
        key : str
            The key to search for completions.

        Returns
        -------
        set
            A set of possible completions for the given key.
        """

        query = key
        common_prefix, existing_prefix, node = self._find_common_prefix_child(query)
        if node is None:
            return set()

        while node is not None:
            # Update search prefix to remove the common_prefix found
            query = query[len(common_prefix) :]
            # Save the last node that is not None
            last_node = node
            common_prefix, existing_prefix, node = node._find_common_prefix_child(query)
        # If the key is shorter than this node's key, complete until reaching
        # the node's key
        if len(key) < len(last_node.key):
            return {last_node.key}
        # When at exactly this node's key, complete with the children's keys
        return set(nd.key for nd in last_node.children.values())

    @property
    def siblings(self):
        "Return all the siblings, including the child."
        return self.parent.children

    def _find_common_prefix_child(self, key):
        """
        Find the first child node that shares a common prefix with the given key.

        Iterates through all children to find the first one that has a non-empty
        common prefix with the input key.

        Parameters
        ----------
        key : str
            The key to search for a common prefix.

        Returns
        -------
        tuple
            A tuple (common_prefix, existing_prefix, child) where:
            - common_prefix (str): The longest common prefix between key
              and the first found child
            - existing_prefix (str): The prefix of the first found child
            - child (RadixNode): The child node, or None if no common prefix exists
            Returns ("", "", None) if no child shares a common prefix with key.
        """
        for existing_prefix, child in self.children.items():
            common_prefix = self._common_longest_prefix(key, existing_prefix)
            if len(common_prefix) > 0:
                return common_prefix, existing_prefix, child
        return "", "", None

    def _common_longest_prefix(self, key1, key2):
        """
        Find the longest common prefix between two strings.

        Compares the two strings character by character and returns the longest
        prefix that both strings share from the beginning.

        Parameters
        ----------
        key1 : str
            The first string.
        key2 : str
            The second string.

        Returns
        -------
        str
            The longest common prefix of key1 and key2. Returns empty string
            if no common prefix exists, or the shorter of the two strings if
            one is a prefix of the other.
        """
        min_length = min(len(key1), len(key2))
        for i in range(min_length):
            if key1[i] != key2[i]:
                return key1[:i]
        return key1[:min_length]

    def as_dict(self):
        """
        Convert the subtree rooted at this node to a nested dictionary.

        Recursively converts all children and their subtrees into a nested
        dictionary structure that represents the tree topology.

        Returns
        -------
        dict
            A nested dictionary where keys are prefixes and values are
            dictionaries representing child subtrees. Leaf nodes return
            empty dictionaries.
        """
        return {k: v.as_dict() for k, v in self.children.items()}

    @property
    def height(self):
        """
        Height of the subtree rooted at this node.
        """
        if self.children == {}:
            return 1
        return 1 + max(v.height for v in self.children.values())

    @property
    def key(self):
        """
        Full key string from the root to this node.
        """
        if self.parent is None:
            return self.prefix
        return self.parent.key + self.prefix

    @property
    def size(self):
        """
        Number of nodes in the subtree rooted at this node, including this node.
        """
        return 1 + sum(child.size for child in self.children.values())

    @property
    def total_chars(self):
        """
        Total number of characters in all prefixes in the subtree rooted at this node.

        This includes the prefix of this node plus all prefixes in its subtree.
        """
        return len(self.prefix) + sum(
            child.total_chars for child in self.children.values()
        )
