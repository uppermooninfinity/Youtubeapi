import secrets
import time
import threading

TOKENS = {}
LOCK = threading.Lock()

TOKEN_TTL = 120


def generate_token(video_id: str):
    token = secrets.token_hex(24)

    with LOCK:
        TOKENS[token] = {
            "video_id": video_id,
            "expires": time.time() + TOKEN_TTL
        }

    return token


def validate_token(token: str, video_id: str):
    with LOCK:
        data = TOKENS.get(token)

        if not data:
            return False

        if data["video_id"] != video_id:
            return False

        if time.time() > data["expires"]:
            TOKENS.pop(token, None)
            return False

        return True


def cleanup_tokens():
    while True:
        time.sleep(60)
        now = time.time()

        with LOCK:
            expired = [
                t for t, v in TOKENS.items()
                if v["expires"] < now
            ]

            for t in expired:
                TOKENS.pop(t, None)


threading.Thread(target=cleanup_tokens, daemon=True).start()
