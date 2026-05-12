from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import StreamingResponse

import os
import asyncio
import logging
import time
import redis
import subprocess

from yt_dlp import YoutubeDL
from utils import generate_token, validate_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("youtube-api")

app = FastAPI()

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

download_lock = asyncio.Lock()

RATE_LIMIT = {}
LIMIT = 20
WINDOW = 60


def rate_limit(ip):
    now = time.time()
    RATE_LIMIT[ip] = [t for t in RATE_LIMIT.get(ip, []) if now - t < WINDOW]
    if len(RATE_LIMIT.get(ip, [])) >= LIMIT:
        return False
    RATE_LIMIT.setdefault(ip, []).append(now)
    return True


def get_stream_url(video_id):
    cached = r.get(video_id)
    if cached:
        return cached

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://youtube.com/watch?v={video_id}", download=False)
        url = info["url"]

    r.setex(video_id, 3600, url)
    return url


def ffmpeg_stream(url):
    cmd = [
        "ffmpeg",
        "-i", url,
        "-f", "mp3",
        "-vn",
        "pipe:1"
    ]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)


@app.get("/")
async def root():
    return {"status": "online", "service": "ffmpeg streaming api"}


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "redis": r.ping(),
        "cache_keys": len(r.keys())
    }


@app.get("/stream/{video_id}")
async def stream(
    video_id: str,
    type: str,
    x_download_token: str = Header(None),
    request: Request = None
):
    ip = request.client.host

    if not rate_limit(ip):
        raise HTTPException(429, "Too many requests")

    if not validate_token(x_download_token, video_id):
        raise HTTPException(403, "Invalid token")

    if len(video_id) != 11:
        raise HTTPException(400, "Invalid video id")

    logger.info(f"Streaming {video_id} ({type})")

    async with download_lock:

        try:
            stream_url = get_stream_url(video_id)

            process = ffmpeg_stream(stream_url)

            return StreamingResponse(
                process.stdout,
                media_type="audio/mpeg"
            )

        except Exception as e:
            logger.error(f"Stream failed: {e}")
            raise HTTPException(500, "Streaming failed")
