# utils.py

import secrets
import time

TOKENS = {}


def generate_token(video_id: str):
    token = secrets.token_hex(24)

    TOKENS[token] = {
        "video_id": video_id,
        "expires": time.time() + 120
    }

    return token


def validate_token(token: str, video_id: str):
    data = TOKENS.get(token)

    if not data:
        return False

    if data["video_id"] != video_id:
        return False

    if time.time() > data["expires"]:
        TOKENS.pop(token, None)
        return False

    return True
