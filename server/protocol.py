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

    if command == "QUIT":
        return BYE
    
    return error("unknown command")
        
    
    