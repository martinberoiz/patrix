# Patrix

Patrix provides a `RadixTree` class
(aka [trie](https://en.wikipedia.org/wiki/Trie), [compressed prefix tree](https://en.wikipedia.org/wiki/Radix_tree), or compact prefix tree)
that behaves like a python dictionary
([`abc.MutableMapping`](https://docs.python.org/3.10/library/collections.abc.html#collections-abstract-base-classes) subclass)
but provides quick and efficient completion suggestions for partial word entries.

This is useful for building autocomplete systems of long lists of known strings that share common prefixes.
This is typical for hierarchical naming systems
like file paths, IP addresses, or domain names, but it is not limited to those examples.

## Features

- **Radix Tree Implementation**: Compressed prefix tree that reduces memory usage by sharing common prefixes
- **Completion Suggestions**: Prefix-based suggestions to complete partial entries
- **Memory Efficient**: Radix tree compression reduces storage requirements
- **Simple Mapping API**: Full python `dict` interface

## Quick Start

### Radix Tree Example

```python
>>> from patrix import RadixTree
>>> words = ("computer", "compute", "computing")
>>> r = RadixTree(words)
>>> # Display suggestions on how to continue a given query prefix
>>> r.completions("")
{'comput'}
>>> r.completions("comput")
{'compute', 'computing'}
>>> r.completions("compute") # The word 'compute' here is both a stem and a final word
{'compute', 'computer'}
>>> r.completions("p")
set()
```

Check the [usage](./usage.md) section for full examples.

A [Trie class](./api/trie.md) is also provided for educational purposes to understand prefix trees.

## License

MIT License - see LICENSE.txt for details.
