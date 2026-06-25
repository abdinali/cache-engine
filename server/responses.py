OK = "OK"
MISS = "MISS"
NOT_FOUND = "NOT_FOUND"
ERROR_PREFIX = "ERROR"
BYE = "BYE"

def ok(value=None):
    if value is None:
        return OK 
    return f"OK {value}"

def error(message):
    return f"{ERROR_PREFIX} {message}"