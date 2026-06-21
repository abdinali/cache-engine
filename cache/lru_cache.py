class LRUCache:
    def __init__(self, max_size):
        if max_size < 1:
            raise ValueError("max_size must be at least 1.")
        self.max_size = max_size
        self._store = {}

    def set(self, key, value):
        self._store[key] = value
    
    def get(self, key):
        if key not in self._store:
            return None
        return self._store[key]

    def delete(self, key):
        return self._store.pop(key, None) is not None
    