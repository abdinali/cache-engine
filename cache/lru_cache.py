import time 

class Node:
    def __init__(self, key, value, ttl=None):
        self.key = key
        self.value = value 
        self.prev = None 
        self.next = None
        self.expires_at = time.time() + ttl if ttl is not None else None

class LRUCache:
    def __init__(self, max_size):
        if max_size < 1:
            raise ValueError("max_size must be at least 1.")
        self.max_size = max_size
        self._store = {}

        self._head = Node(None, None)
        self._tail = Node(None, None)
        
        self._head.next = self._tail 
        self._tail.prev = self._head

    # public methods
    def set(self, key, value, ttl=None):
        if key in self._store:
            node = self._store[key]
            node.value = value 
            node.expires_at = time.time() + ttl if ttl is not None else None
            self._move_to_front(node)
            return
        if self.is_full():
            self._evict_lru()
        node = Node(key, value, ttl)
        self._store[key] = node
        self._add_to_front(node)
    
    def get(self, key):
        if key not in self._store:
            return None
        node = self._store[key]
        if node.expires_at is not None and self.is_node_expired(node):
            self.delete(key)
            return None
        self._move_to_front(node)
        return node.value

    def delete(self, key):
        if key not in self._store:
            return False 
        node = self._store.pop(key)
        self._remove_node(node)
        return True

    # private helper methods
    def _add_to_front(self, node):
        node.prev = self._head 
        node.next = self._head.next
        self._head.next.prev = node 
        self._head.next = node
            
    def _move_to_front(self, node):
        self._remove_node(node)
        self._add_to_front(node)
        
    def _remove_node(self, node):
        node.prev.next = node.next 
        node.next.prev = node.prev
        node.next = None 
        node.prev = None
        
    def _evict_lru(self):
        lru = self._tail.prev
        self.delete(lru.key)
        
    # utility methods
    def is_full(self):
        return len(self._store) >= self.max_size

    def is_node_expired(self, node):
        return time.time() > node.expires_at