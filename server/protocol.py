from server.responses import BYE, MISS, NOT_FOUND, error, ok

def handle_command(cache, line, lock):
    parts = line.strip().split()
    if len(parts) == 0:
        return error("empty command.")

    command = parts[0].upper()

    if command == "GET":
        if len(parts) < 2:
            return error("usage: GET key.")

        key = parts[1]
        
        with lock:
            value = cache.get(key)
        
        if value is None:
            return MISS 
        
        return ok(value)        
    
    if command == "SET":
        if len(parts) < 3:
            return error("usage: SET key value [ttl].")
        
        key = parts[1]
        value = parts[2]
        ttl = None 
        if len(parts) > 3:
            try:
                ttl = int(parts[3])
            except ValueError:
                return error("invalid ttl")

        with lock:
            cache.set(key, value, ttl)
        
        return ok()

    if command == "DELETE":
        if len(parts) < 2:
            return error("usage: DELETE key.")
        
        key = parts[1]

        with lock:
            res = cache.delete(key)
        
        if not res:
            return NOT_FOUND 
        
        return ok()


    if command == "QUIT":
        return BYE
    
    return error("unknown command.")
        
    
    