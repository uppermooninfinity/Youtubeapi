import redis
import time
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

CACHE_TTL = 3600


def set_cache(video_id: str, stream_url: str):
    data = {
        "url": stream_url,
        "time": time.time()
    }

    r.setex(video_id, CACHE_TTL, json.dumps(data))


def get_cache(video_id: str):
    data = r.get(video_id)

    if not data:
        return None

    try:
        parsed = json.loads(data)
        return parsed["url"]
    except:
        return None


def delete_cache(video_id: str):
    r.delete(video_id)


def clear_all_cache():
    for key in r.keys():
        r.delete(key)


def cache_exists(video_id: str):
    return r.exists(video_id) == 1
