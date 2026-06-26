import threading 

from cache.lru_cache import LRUCache
from server.protocol import handle_command 
from server.responses import BYE, MISS, NOT_FOUND, error, ok

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

def test_set_then_get():
    cache = LRUCache(max_size=2)
    lock = threading.Lock()
    assert handle_command(cache, "SET k1 v2", lock) == ok()
    assert handle_command(cache, "GET k1", lock) == ok("v2")

def test_set_invalid_ttl():
    cache = LRUCache(max_size=2)
    lock = threading.Lock()
    assert handle_command(cache, "SET user 42 abc", lock) == error("invalid ttl")

def test_delete_existing_key():
    cache = LRUCache(max_size=2)
    lock = threading.Lock()
    assert handle_command(cache, "SET tennis ball", lock) == ok()
    assert handle_command(cache, "GET tennis", lock) == ok("ball")
    assert handle_command(cache, "DELETE tennis", lock) == ok()

def test_delete_missing_key():
    cache = LRUCache(max_size=2)
    lock = threading.Lock()
    assert handle_command(cache, "DELETE golf", lock) == NOT_FOUND

def test_quit_returns_bye():
    cache = LRUCache(max_size=2)
    lock = threading.Lock()
    assert handle_command(cache, "QUIT", lock) == BYE

def test_unknown_command():
    cache = LRUCache(max_size=2)
    lock = threading.Lock()
    assert handle_command(cache, "XYZ key", lock) == error("unknown command.")