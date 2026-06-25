import threading 

from cache.lru_cache import LRUCache
from server.protocol import handle_command 
from server.responses import BYE, MISS, error, ok

def test_get_hit():
    cache = LRUCache(max_size=2)
    cache.set("a", 1)
    lock = threading.Lock()
    assert handle_command(cache, "GET a", lock) == ok("1")

def test_get_miss():
    cache = LRUCache(max_size=2)
    cache.set("a", 1)
    lock = threading.Lock()
    assert handle_command(cache, "GET abc", lock) == MISS
    
