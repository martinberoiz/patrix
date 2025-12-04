from patrix import Trie
import pytest


def test_init():
    t = Trie((("trie", 1), ("tree", 2), ("try", 3)))
    assert t.asdict() == {"t": {"r": {"e": {"e": {}}, "i": {"e": {}}, "y": {}}}}


def test_empty_key():
    with pytest.raises(ValueError):
        Trie((("", 1), ("tree", 2), ("try", 3)))


def test_non_string_key():
    with pytest.raises(ValueError):
        Trie(((1, 1), ("tree", 2), ("try", 3)))


def test_search():
    t = Trie((("trie", 1), ("tree", 2), ("try", 3)))
    assert "e" in t.search("tri").children
    assert "e" in t.search("tre").children
    assert t.search("try").value == 3
    assert t.search("trio") is None
    assert t.search("notaword") is None

    with pytest.raises(ValueError):
        t.search("")
    with pytest.raises(ValueError):
        t.search(1)


def test_get_key():
    t = Trie((("trie", 1), ("tree", 2), ("try", 3)))
    assert t.search("tri").get_key() == "tri"
    assert t.search("tre").get_key() == "tre"
    assert t.search("try").get_key() == "try"


def test_insert():
    t = Trie((("trie", 1), ("tree", 2), ("try", 3)))
    t.insert("trio", 4)
    assert t.asdict() == {
        "t": {"r": {"e": {"e": {}}, "i": {"e": {}, "o": {}}, "y": {}}}
    }
