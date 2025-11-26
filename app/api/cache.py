from functools import lru_cache

CACHE = {}

def cache_get(key: str):
    return CACHE.get(key)

def cache_set(key: str, value):
    CACHE[key] = value


# Se quiser depois, posso mudar para Redis e TTL configurável.