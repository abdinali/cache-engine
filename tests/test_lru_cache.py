from cache.lru_cache import LRUCache

def test_set_and_get():
    cache = LRUCache(max_size=4)
    cache.set("a", 5)
    assert cache.get("a") == 5

def test_get_missing_key_returns_none():
    cache = LRUCache(max_size=4)
    assert cache.get("a") is None 

def test_delete_removes_key():
    cache = LRUCache(max_size=4)
    cache.set("a", 3)
    assert cache.delete("a") is True 
    assert cache.get("a") is None

def test_delete_missing_key_return_false():
    cache = LRUCache(max_size=3)
    cache.set("a", 5)
    assert cache.delete("b") is False

def test_evicts_least_recently_used_when_full():
    cache = LRUCache(max_size=2)
    cache.set("a", 1)           # MRU -> a <- LRU
    cache.set("b", 2)           # MRU -> b, a <- LRU
    cache.get("a")              # MRU -> a, b <- LRU
    cache.set("c", 3)           # MRU -> c, a, b <- LRU
    assert cache.get("b") is None # b was evicted
    assert cache.get("a") == 1
    assert cache.get("c") == 3