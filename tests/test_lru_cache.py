from cache.lru_cache import LRUCache
import time

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
    cache.set("c", 3)           # MRU -> c, a <- LRU
    assert cache.get("b") is None # b was evicted
    assert cache.get("a") == 1
    assert cache.get("c") == 3
    
def test_key_expires_after_ttl():
    cache = LRUCache(max_size=3)
    cache.set("session", "abc", ttl=1) # expiry set to 1 second
    assert cache.get("session") == "abc"
    time.sleep(1.1)
    assert cache.get("session") is None

def test_key_without_ttl_does_not_expire():
    cache = LRUCache(max_size=3)
    cache.set("a", 1)
    time.sleep(1.1)
    assert cache.get("a") == 1
    
def test_set_updates_existing_key_with_new_ttl():
    cache = LRUCache(max_size=2)
    cache.set("session", "old", ttl=1)
    time.sleep(0.5)
    cache.set("session", "new", ttl=2) # reset expiry, adds 2 seconds
    time.sleep(1.1) # would be expired if old ttl is still applied
    assert cache.get("session") == "new"
    
def test_set_update_without_ttl_clears_expiry():
    cache = LRUCache(max_size=3)
    cache.set("a", 1, ttl=1)   # would expire in 1 second
    cache.set("a", 2)          # update value, no ttl → never expires
    time.sleep(1.1)
    assert cache.get("a") == 2