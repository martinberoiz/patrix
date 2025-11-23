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

Search for a word in the trie:

```python
>>> t.search("tri")
<autocomplete.trie.TrieNode object at 0x7f952c171c10>
>>> t.search("tri").get_key()
'tri'
>>> t.search("trio") is None
True
```

Add a new word to the trie:

```python
>>> t.insert("trio", 4)
>>> t.as_dict()
{'t': {'r': {'e': {'e': {}}, 'i': {'e': {}, 'o': {}}, 'y': {}}}}
```

## Radix tree example

```python
>>> from autocomplete import radix
>>> r = radix.RadixTree((("computer", 1), ("compute", 2), ("computing", 3)))
>>> r.as_dict()
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
