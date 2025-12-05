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


def test_parent_relations():
    r = RadixTree(["computer", "computing", "compute", "screen"])

    # Depth-first search to check parent-child relationships
    stack = [r.root]
    while stack:
        node = stack.pop()
        for child in node.children.values():
            assert child.parent == node
        stack.extend(node.children.values())


def test_asdict():
    r = RadixTree(("computer",))
    assert r.asdict() == {"computer": {}}

    r = RadixTree(("computer", "screen"))
    assert r.asdict() == {"computer": {}, "screen": {}}

    r = RadixTree(("computer", "compute"))
    assert r.asdict() == {"compute": {"": {}, "r": {}}}

    r = RadixTree(("computer", "computing"))
    assert r.asdict() == {"comput": {"er": {}, "ing": {}}}

    r = RadixTree(("computer", "computing", "compute"))
    assert r.asdict() == {"comput": {"e": {"": {}, "r": {}}, "ing": {}}}


def test_insert():
    r = RadixTree(("computer",))
    assert r.asdict() == {"computer": {}}
    r.insert("computing", 2)
    assert r.asdict() == {"comput": {"er": {}, "ing": {}}}
    r.insert("compute", 3)
    assert r.asdict() == {"comput": {"e": {"": {}, "r": {}}, "ing": {}}}


def test_insertion_order():
    r = RadixTree(("compute", "computer", "computing"))
    s = RadixTree(("computer", "compute", "computing"))
    assert r.asdict() == s.asdict()


def test_duplicate():
    r = RadixTree((("computer", 1), ("computer", 2)))
    assert r.asdict() == {"computer": {}}


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


def test_from_dict():
    r = RadixTree(["computer", "computing", "compute", "screen"])
    s = RadixTree.from_dict(r.asdict())
    assert s.asdict() == r.asdict()


def test_getitem():
    r = RadixTree((("computer", 1), ("computing", 2), ("compute", 3)))
    assert r["computer"] == 1
    assert r["computing"] == 2
    assert r["compute"] == 3
    assert r.get("computer") == 1
    assert r.get("computing") == 2
    assert r.get("compute") == 3
    assert r.get("comput", "fallback") == "fallback"


def test_contains():
    r = RadixTree(["computer", "computing", "compute"])
    assert "computer" in r
    assert "computing" in r
    assert "compute" in r
    assert "comput" not in r


def test_setitem():
    r = RadixTree()
    r["computer"] = 1
    assert r["computer"] == 1
    r["computing"] = 2
    assert r["computing"] == 2
    r["compute"] = 3
    assert r["compute"] == 3


def test_pop():
    r = RadixTree(
        [("computer", 1), ("compute", 2), ("computing", 3), ("deletethis", 4)]
    )
    assert r.pop("deletethis") == 4
    assert r.asdict() == {"comput": {"e": {"r": {}, "": {}}, "ing": {}}}

    assert r.pop("computer") == 1
    assert r.asdict() == {"comput": {"ing": {}, "e": {}}}
    
    assert r.pop("compute") == 2
    assert r.asdict() == {"computing": {}}

    assert r.pop("computing") == 3
    assert r.asdict() == {}

    # Swap compute & computer order
    r = RadixTree(
        [("computer", 1), ("compute", 2), ("computing", 3)]
    )
    assert r.pop("compute") == 2
    assert r.asdict() == {"comput": {"er": {}, "ing": {}}}
    
    assert r.pop("computer") == 1
    assert r.asdict() == {"computing": {}}

    assert r.pop("computing") == 3
    assert r.asdict() == {}

    # Test for default key
    r = RadixTree(
        [("computer", 1), ("compute", 2), ("computing", 3)]
    )
    assert r.pop("notakey", 0) == 0
