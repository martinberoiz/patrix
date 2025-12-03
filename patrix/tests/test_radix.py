from patrix import RadixTree
import pytest


def test_init():
    r = RadixTree((("computer", 1),))
    assert "computer" in r.root.children
    child = r.root.children["computer"]
    assert child.prefix == "computer"
    assert child.value == 1

    # Test loading from list of strings
    r = RadixTree(["computer", "computing", "compute"])
    assert "comput" in r.root.children

    # Test loading from list of key-value pairs
    r = RadixTree((("computer", 1), ("computing", 2), ("compute", 3)))
    assert "comput" in r.root.children

    # Test loading from list of mixed strings and key-value pairs
    r = RadixTree((("computer", 1), "computing", ("compute", 2)))
    assert "comput" in r.root.children

    # Test loading from list of mixed strings and key-value pairs
    r = RadixTree((("computer", 1), "computing", ("compute", 2)))
    assert "comput" in r.root.children


def test_parent_relations():
    r = RadixTree(["computer", "computing", "compute", "screen"])

    # Depth-first search to check parent-child relationships
    stack = [r.root]
    while stack:
        node = stack.pop()
        for child in node.children.values():
            assert child.parent == node
        stack.extend(node.children.values())


def test_as_dict():
    r = RadixTree(("computer",))
    assert r.as_dict() == {"computer": {}}

    r = RadixTree(("computer", "screen"))
    assert r.as_dict() == {"computer": {}, "screen": {}}

    r = RadixTree(("computer", "compute"))
    assert r.as_dict() == {"compute": {"": {}, "r": {}}}

    r = RadixTree(("computer", "computing"))
    assert r.as_dict() == {"comput": {"er": {}, "ing": {}}}

    r = RadixTree(("computer", "computing", "compute"))
    assert r.as_dict() == {"comput": {"e": {"": {}, "r": {}}, "ing": {}}}


def test_insert():
    r = RadixTree(("computer",))
    assert r.as_dict() == {"computer": {}}
    r.insert("computing", 2)
    assert r.as_dict() == {"comput": {"er": {}, "ing": {}}}
    r.insert("compute", 3)
    assert r.as_dict() == {"comput": {"e": {"": {}, "r": {}}, "ing": {}}}


def test_duplicate():
    r = RadixTree((("computer", 1), ("computer", 2)))
    assert r.as_dict() == {"computer": {}}


def test_empty_key():
    with pytest.raises(ValueError):
        RadixTree((("", 1), ("computer", 2)))


def test_non_string_key():
    with pytest.raises(ValueError):
        RadixTree(((1, 1), ("computer", 2)))


def test_height():
    r = RadixTree((("computer", 1), ("computing", 2), ("compute", 3)))
    assert r.height == 3


def test_key():
    r = RadixTree((("computer", 1), ("computing", 2), ("compute", 3)))
    assert r.root.key == ""
    assert r.root.children["comput"].key == "comput"
    assert r.root.children["comput"].children["e"].key == "compute"
    assert r.root.children["comput"].children["ing"].key == "computing"


def test_completions():
    r = RadixTree(["computer", "computing", "compute", "screen"])
    assert r.completions("comp") == {"comput"}
    assert r.completions("comput") == {"compute", "computing"}
    assert r.completions("compute") == {"compute", "computer"}
    assert r.completions("computing") == set()
    assert r.completions("computer") == set()
    assert r.completions("s") == {"screen"}
    assert r.completions("a") == set()


def test_size():
    r = RadixTree((("computer", 1), ("computing", 2), ("compute", 3)))
    assert r.size == 6


def test_total_chars():
    r = RadixTree((("computer", 1), ("computing", 2), ("compute", 3)))
    assert r.total_chars == 11


def test_siblings():
    r = RadixTree((("computer", 1), ("computing", 2), ("compute", 3)))
    node = r.root.children["comput"].children["e"]
    assert len(node.siblings) == 2
    assert "e" in node.siblings
    assert "ing" in node.siblings
