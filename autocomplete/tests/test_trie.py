from autocomplete import trie

def test_trie():
    t = trie.Trie((("trie", 1), ("tree", 2), ("try", 3)))
    assert t.as_dict() == {'t': {'r': {'e': {'e': {}}, 'i': {'e': {}}, 'y': {}}}}
