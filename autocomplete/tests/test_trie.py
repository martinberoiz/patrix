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


def test_trie_search():
    t = trie.Trie((("trie", 1), ("tree", 2), ("try", 3)))
    assert "e" in t.search("tri").children
    assert "e" in t.search("tre").children
    assert t.search("try").value == 3
    assert t.search("trio") is None


def test_get_key():
    t = trie.Trie((("trie", 1), ("tree", 2), ("try", 3)))
    assert t.search("tri").get_key() == "tri"
    assert t.search("tre").get_key() == "tre"
    assert t.search("try").get_key() == "try"
