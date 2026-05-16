import redis
import time
import json
from typing import Optional

try:
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    r.ping()
except redis.ConnectionError as e:
    print(f"Failed to connect to Redis: {e}")
    r = None

CACHE_TTL = 3600


def set_cache(video_id: str, stream_url: str) -> None:
    if r is None:
        return
    
    data = {
        "url": stream_url,
        "time": time.time()
    }

    try:
        r.setex(video_id, CACHE_TTL, json.dumps(data))
    except redis.RedisError as e:
        print(f"Error setting cache: {e}")


def get_cache(video_id: str) -> Optional[str]:
    if r is None:
        return None
    
    try:
        data = r.get(video_id)

        if not data:
            return None

        parsed = json.loads(data)
        return parsed["url"]
    except (json.JSONDecodeError, KeyError, redis.RedisError) as e:
        print(f"Error getting cache: {e}")
        return None


def delete_cache(video_id: str) -> None:
    if r is None:
        return
    
    try:
        r.delete(video_id)
    except redis.RedisError as e:
        print(f"Error deleting cache: {e}")


def clear_all_cache() -> None:
    if r is None:
        return
    
    try:
        cursor = 0
        while True:
            cursor, keys = r.scan(cursor)
            if keys:
                r.delete(*keys)
            if cursor == 0:
                break
    except redis.RedisError as e:
        print(f"Error clearing cache: {e}")


def cache_exists(video_id: str) -> bool:
    if r is None:
        return False
    
    try:
        return r.exists(video_id) == 1
    except redis.RedisError as e:
        print(f"Error checking cache: {e}")
        return False
