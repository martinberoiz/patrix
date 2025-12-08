# Usage Guide

This guide provides examples and common use cases for the `RadixTree` implementation in Patrix.

## Create a new Radix Tree

Initialize a RadixTree with an iterable of entries.
Entries can be bare strings (with default value `None`), or a `(key, value)` tuple.

```python
from patrix import RadixTree

# Create a radix tree with initial data
# values are optional, but if provided, enter them as (key, value) tuples
entries = [
    ("computer", 1),
    "compute"
]
r = RadixTree(entries)
r["computing"] = 3  # insert a new word
r["compute"] = 2  # update the value of an existing word
```

Initialize from a dictionary or an iterable of words:

```python
entries = {
    "computer": 1,
    "compute": 2,
    "computing": 3
}
r = RadixTree(entries.items())
words = ["computer", "compute", "computing"]
r = RadixTree(words)
```

## Suggest Word Completions

Display possible completions for a given query prefix:

```python
>>> r.completions()
{'comput'}
>>> r.completions("comput")
{'compute', 'computing'}
>>> # The word 'compute' is both a prefix and a final word
>>> r.completions("compute")
{'compute', 'computer'}
>>> r.completions("p")  # no words start with 'p'
set()
```

## Store the Tree

The tree can be serialized to a nested dictionary representation to be stored on disk or sent over the network.

```python
import json
>>> channels = {
...    "H1:PEM-CS_ACC": {"sampling": 8192, "dtype": "float"},
...    "H1:PEM-EX_LOW": {"sampling": 256, "dtype": "int"},
...    "H1:PEM-VAU": {"sampling": 8192, "dtype": "float"},
...    "H1:PEM-CS_MIC": {"sampling": 16384, "dtype": "float"},
... }
>>> r = RadixTree(channels.items())
>>> # This will work as long as the node values
>>> # can be serialized as json-encodable objects.
>>> with open("tree.json", "w") as f:
...    json.dump(r.asdict(), f, indent=2)
```

To load the tree from a dictionary, use the `from_dict` class method:

```python
>>> with open("tree.json", "r") as f:
>>>     s = json.load(f)
>>> r = RadixTree.from_dict(s)
>>> "H1:PEM-CS_ACC" in r
True
```

## Access Tree Properties

Access tree metrics:

```python
>>> r = RadixTree(("computer", "computing", "compute"))
>>> r.height  # Height of the tree
3
>>> r.size  # Number of nodes
6
>>> r.total_chars  # Total characters in all of the prefixes in the tree
11
```

The radix tree compresses common prefixes, reducing memory usage,
but the level of compression will strongly depend on how many common prefixes are shared by the entries.

```python
>>> r = RadixTree(("computer", "computing", "compute"))
>>> total_chars = sum(map(len, r.keys()))
>>> compression = 1 - r.total_chars / total_chars
>>> compression  # 54% compression rate
0.5416666666666667
```

## Use the Tree as a Regular Dictionary

RadixTree implements the python dictionary interface, subclassing from `collections.abc.MutableMapping`.
All the standard dictionary methods are supported with the notable difference that the insertion order is not preserved.

```python
>>> r = RadixTree((("computer", 1), "compute", ("computing", 3)))
>>> "compute" in r  # checks for membership
True
>>> r.pop("computer")  # pop an entry
2
>>> r |= {"computer": 2}  # update the tree with a dictionary
>>> len(r), list(r)
(3, ['compute', 'computer', 'computing'])
>>> r.pop("nokey")
KeyError: 'nokey'
>>> r.pop("nokey", 0)
0
>>> # iterate on the tree entries
>>> list(filter(lambda k: k.startswith("compute"), r.keys()))
['compute', 'computer']
>>> list(filter(lambda v: v > 1, r.values()))
[2, 3]
>>> list(filter(lambda kv: kv[1] > 1, r.items()))
[('compute', 2), ('computing', 3)]
>>> s = r.copy()  # shallow copy the tree
>>> r.clear()  # clear the tree
```
