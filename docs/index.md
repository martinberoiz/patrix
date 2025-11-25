# Patrix

Patrix is a package for building autocomplete systems
of long lists of known strings that share common prefixes.
This is typical for hierarchical naming systems
like file paths, IP addresses, or domain names, but it is not limited to those examples.
Patrix provides quick and efficient completion suggestions for partial word entries.

Patrix provides implementations for a standard trie (prefix tree) and a radix tree
(also known as compressed prefix tree, or compact prefix tree) data structures.
These data structures are designed to be efficient for partial word completion.

## Features

- **Trie Implementation**: Standard prefix tree data structure with one character per node
- **Radix Tree Implementation**: Compressed prefix tree that reduces memory usage by sharing common prefixes
- **Completion Suggestions**: Prefix-based suggestions to complete partial entries
- **Memory Efficient**: Radix tree compression reduces storage requirements
- **Simple API**: Easy-to-use interface for autocomplete functionality

## Quick Start

### Trie Example

```python
>>> from patrix import Trie
>>> t = Trie((("trie", 1), ("try", 2), ("tree", 3)))
>>> t.as_dict()
{'t': {'r': {'i': {'e': {}}, 'y': {}, 'e': {'e': {}}}}}
```

### Radix Tree Example

```python
>>> from patrix import RadixTree
>>> r = RadixTree((("computer", 1), ("compute", 2), ("computing", 3)))
>>> r.completions("comput")
{'compute', 'computing'}
>>> r.insert("computation", 4)
>>> r.completions("comput")
{'compute', 'computing', 'computation'}
>>> r.as_dict()
{'comput': {'e': {'': {}, 'r': {}}, 'ing': {}, 'ation': {}}}
```

## License

MIT License - see LICENSE.txt for details.
