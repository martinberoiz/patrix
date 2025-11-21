# Autocomplete

A python package that uses a compressed prefix tree (aka trie or radix tree)
to store a dictionary of "correct" words and provides suggestions to complete partial words.

It is used in autocomplete systems to provide suggestions to users based on the words they have typed.

## Trie example

```python
>>> from autocomplete import trie
>>> t = trie.Trie((("trie", 1), ("try", 2), ("tree", 3)))
>>> t.as_dict()
{'t': {'r': {'i': {'e': {}}, 'y': {}, 'e': {'e': {}}}}}
```
