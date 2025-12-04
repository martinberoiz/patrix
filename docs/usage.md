# Usage Guide

This guide provides examples and common use cases for both the Trie and RadixTree implementations in Patrix.

## Radix Tree

A radix tree (compressed trie) compresses common prefixes, making it more memory-efficient while maintaining fast operations.

### Creating a Radix Tree

Initialize a RadixTree with a collection of key-value pairs:

```python
from patrix import RadixTree

# Create a radix tree with initial data
# values are optional, but if provided, enter them as tuples (word, value)
r = RadixTree((("computer", 1), "compute"))
```

Insert a new word into the radix tree:

```python
>>> r.insert("computing")
>>> r.asdict()
{'comput': {'e': {'': {}, 'r': {}}, 'ing': {}}}
```

### Getting Completions

Display suggestions on how to continue a given query prefix:

```python
>>> r.completions("c")
{'comput'}
>>> r.completions("comput")
{'compute', 'computing'}
>>> r.completions("compute")  # The word 'compute' is both a stem and a final word
{'compute', 'computer'}
>>> r.completions("p")
set()
```

### Visualizing the Radix Tree

Convert the radix tree to a nested dictionary representation:

```python
>>> r = RadixTree(("computer", "compute", "computing"))
>>> r.asdict()
{'comput': {'e': {'': {}, 'r': {}}, 'ing': {}}}
```

### Compression Rate

The radix tree compresses common prefixes, reducing memory usage:

```python
>>> r.total_chars
11
>>> len("computer" + "computing" + "compute")
24
>>> 1 - 11 / 24  # 54% compression rate
0.5416666666666667
>>> r.size  # nodes in the tree
6
```

### Tree Properties

Access tree metrics:

```python
>>> r.height  # Height of the tree
3
>>> r.size  # Number of nodes
6
>>> r.total_chars  # Total characters in all prefixes
11
```

## Trie

A standard trie (prefix tree) stores one character per node, making it simple but potentially more memory-intensive than a radix tree.

### Creating a Trie

Initialize a Trie with a collection of key-value pairs:

```python
from patrix import trie

# Create a trie with initial data
t = trie.Trie((("trie", 1), ("try", 2), ("tree", 3)))
```

### Searching for Words

Search for a word in the trie:

```python
>>> t.search("tri")
<patrix.trie.TrieNode object at 0x7f952c171c10>
>>> t.search("tri").get_key()
'tri'
>>> t.search("trio") is None
True
```

### Inserting Words

Add a new word to the trie:

```python
>>> t.insert("trio", 4)
>>> t.asdict()
{'t': {'r': {'e': {'e': {}}, 'i': {'e': {}, 'o': {}}, 'y': {}}}}
```

### Visualizing the Trie

Convert the trie to a nested dictionary representation:

```python
>>> t = trie.Trie((("trie", 1), ("try", 2), ("tree", 3)))
>>> t.asdict()
{'t': {'r': {'i': {'e': {}}, 'y': {}, 'e': {'e': {}}}}}
```


## Comparison: Trie vs Radix Tree

### When to Use Trie

- Simple use cases where memory is not a concern
- Need to traverse character-by-character
- Educational purposes to understand prefix trees

### When to Use Radix Tree

- Memory efficiency is important
- Working with many words that share common prefixes
- Building autocomplete systems for production
- Need compression metrics

### Memory Comparison

The radix tree compresses common prefixes, significantly reducing memory usage when many words share prefixes. For example, with words like "computer", "compute", and "computing", the radix tree stores the common prefix "comput" once, while a trie would store each character separately.

## Common Use Cases

### Autocomplete System

```python
from patrix import RadixTree

# Build a dictionary of words with their frequencies
words = [
    "python",
    "programming",
    "program",
    "project",
    "package",
]

# Create radix tree
autocomplete = RadixTree(words)

# Get suggestions as user types
def get_suggestions(prefix):
    return autocomplete.completions(prefix)

# Example usage
print(get_suggestions("p"))      # {'pro', 'python', 'package'}
print(get_suggestions("pro"))    # {'program', 'project'}
print(get_suggestions("program"))   # {'program', 'programming'}
```

### Word Dictionary

```python
from patrix import Trie

words = [
    ("hello", "greeting"),
    ("help", "assistance"),
    ("helicopter", "aircraft"),
]

# Create a dictionary
dictionary = Trie(words)


# Check if word exists
def word_exists(word):
    node = dictionary.search(word)
    return node is not None and node.value is not None


# Get word definition
def get_definition(word):
    node = dictionary.search(word)
    return node.value if node and node.value else None

print(word_exists("hello"))  # True
print(word_exists("he"))  # False
print(word_exists("hi"))  # False
print(get_definition("hello"))  # 'greeting'
print(get_definition("help"))  # 'assistance'
```
