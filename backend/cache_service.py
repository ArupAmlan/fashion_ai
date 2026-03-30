import redis
import json
import pickle
import hashlib
from typing import Optional, Any
import os

# Redis connection
_redis_client = None


def get_redis_client() -> Optional[redis.Redis]:
    """Get or create Redis client"""
    global _redis_client
    if _redis_client is None:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        try:
            _redis_client = redis.from_url(redis_url, decode_responses=False)
            _redis_client.ping()
        except (redis.ConnectionError, redis.ResponseError):
            print("Redis not available, caching disabled")
            _redis_client = None
    return _redis_client


def generate_cache_key(*args, **kwargs) -> str:
    """Generate a cache key from arguments"""
    key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
    return hashlib.md5(key_data.encode()).hexdigest()


async def get_cached_result(key: str) -> Optional[Any]:
    """Get cached result from Redis"""
    client = get_redis_client()
    if client is None:
        return None
    
    try:
        data = client.get(key)
        if data:
            return pickle.loads(data)
    except Exception as e:
        print(f"Cache get error: {e}")
    return None


async def set_cached_result(key: str, value: Any, expire_seconds: int = 3600) -> bool:
    """Set cached result in Redis"""
    client = get_redis_client()
    if client is None:
        return False
    
    try:
        serialized = pickle.dumps(value)
        client.setex(key, expire_seconds, serialized)
        return True
    except Exception as e:
        print(f"Cache set error: {e}")
        return False


async def delete_cached_result(key: str) -> bool:
    """Delete cached result from Redis"""
    client = get_redis_client()
    if client is None:
        return False
    
    try:
        client.delete(key)
        return True
    except Exception as e:
        print(f"Cache delete error: {e}")
        return False


class CacheDecorator:
    """Decorator for caching function results"""
    
    def __init__(self, expire_seconds: int = 3600, key_prefix: str = ""):
        self.expire_seconds = expire_seconds
        self.key_prefix = key_prefix
    
    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{self.key_prefix}:{generate_cache_key(func.__name__, *args, **kwargs)}"
            
            # Try to get from cache
            cached = await get_cached_result(cache_key)
            if cached is not None:
                return cached
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache the result
            await set_cached_result(cache_key, result, self.expire_seconds)
            
            return result
        
        return wrapper


def cached(expire_seconds: int = 3600, key_prefix: str = ""):
    """Decorator factory for caching"""
    return CacheDecorator(expire_seconds, key_prefix)
