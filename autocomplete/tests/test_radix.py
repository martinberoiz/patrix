from autocomplete.radix import RadixTree
import pytest


def test_radix_create():
    r = RadixTree((("computer", 1),))
    assert "computer" in r.root.children
    child = r.root.children["computer"]
    assert child.prefix == "computer"
    assert child.value == 1


def test_parent_relations():
    r = RadixTree((("computer", 1), ("computing", 2), ("compute", 3), ("screen", 4)))

    # Depth-first search to check parent-child relationships
    stack = [r.root]
    while stack:
        node = stack.pop()
        for child in node.children.values():
            assert child.parent == node
        stack.extend(node.children.values())


def test_radix_as_dict():
    r = RadixTree((("computer", 1),))
    assert r.as_dict() == {"computer": {}}

    r = RadixTree((("computer", 1), ("screen", 2)))
    assert r.as_dict() == {"computer": {}, "screen": {}}

    r = RadixTree((("computer", 1), ("compute", 2)))
    assert r.as_dict() == {"compute": {"": {}, "r": {}}}

    r = RadixTree((("computer", 1), ("computing", 2)))
    assert r.as_dict() == {"comput": {"er": {}, "ing": {}}}

    r = RadixTree((("computer", 1), ("computing", 2), ("compute", 3)))
    assert r.as_dict() == {"comput": {"e": {"": {}, "r": {}}, "ing": {}}}


def test_radix_insert():
    r = RadixTree((("computer", 1),))
    assert r.as_dict() == {"computer": {}}
    r.insert("computing", 2)
    assert r.as_dict() == {"comput": {"er": {}, "ing": {}}}
    r.insert("compute", 3)
    assert r.as_dict() == {"comput": {"e": {"": {}, "r": {}}, "ing": {}}}


def test_radix_duplicate():
    r = RadixTree((("computer", 1), ("computer", 2)))
    assert r.as_dict() == {"computer": {}}


def test_radix_empty_key():
    with pytest.raises(ValueError):
        RadixTree((("", 1), ("computer", 2)))


def test_radix_non_string_key():
    with pytest.raises(ValueError):
        RadixTree(((1, 1), ("computer", 2)))


def test_tree_height():
    r = RadixTree((("computer", 1), ("computing", 2), ("compute", 3)))
    assert r.height == 3


def test_key():
    r = RadixTree((("computer", 1), ("computing", 2), ("compute", 3)))
    assert r.root.key == ""
    assert r.root.children["comput"].key == "comput"
    assert r.root.children["comput"].children["e"].key == "compute"
    assert r.root.children["comput"].children["ing"].key == "computing"


def test_completions():
    r = RadixTree((("computer", 1), ("computing", 2), ("compute", 3), ("screen", 4)))
    assert r.completions("comp") == {"comput"}
    assert r.completions("comput") == {"compute", "computing"}
    assert r.completions("compute") == {"compute", "computer"}
    assert r.completions("computing") == set()
    assert r.completions("computer") == set()
    assert r.completions("s") == {"screen"}
