from autocomplete import trie
import pytest


def test_trie():
    t = trie.Trie((("trie", 1), ("tree", 2), ("try", 3)))
    assert t.as_dict() == {"t": {"r": {"e": {"e": {}}, "i": {"e": {}}, "y": {}}}}


def test_trie_empty_key():
    with pytest.raises(ValueError):
        trie.Trie((("", 1), ("tree", 2), ("try", 3)))


def test_trie_non_string_key():
    with pytest.raises(ValueError):
        trie.Trie(((1, 1), ("tree", 2), ("try", 3)))
