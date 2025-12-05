# Patrix

Patrix provides a radix tree class (aka trie, compressed prefix tree, or compact prefix tree)
that behaves mostly like a python dictionary
but provides quick and efficient completion suggestions for partial word entries.

This is useful for building autocomplete systems of long lists of known strings that share common prefixes.
This is typical for hierarchical naming systems
like file paths, IP addresses, or domain names, but it is not limited to those examples.

## Features

- **Radix Tree Implementation**: Compressed prefix tree that reduces memory usage by sharing common prefixes
- **Completion Suggestions**: Prefix-based suggestions to complete partial entries
- **Memory Efficient**: Radix tree compression reduces storage requirements
- **Simple API**: The API follows python's `dict` interface as much as possible, with some additions.

## Quick Start

### Radix Tree Example

```python
>>> from patrix import RadixTree
>>> # Entries can be a list of strings or key-value tuples
>>> r = RadixTree(("computer", "compute", ("computing", 1)))
>>> r.asdict()
{'comput': {'e': {'': {}, 'r': {}}, 'ing': {}}}
>>> s = RadixTree.from_dict({'comput': {'e': {'': {}, 'r': {}}, 'ing': {}}})
>>> s.asdict()
{'comput': {'e': {'': {}, 'r': {}}, 'ing': {}}}
```

Display suggestions on how to continue a given query prefix

```python
>>> r.completions("c")
{'comput'}
>>> r.completions("comput")
{'compute', 'computing'}
>>> r.completions("compute") # The word 'compute' here is both a stem and a final word
{'compute', 'computer'}
>>> r.completions("p")
set()
```

Check the [usage](./usage.md) section for more examples.

## License

MIT License - see LICENSE.txt for details.
