from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse

import os
import asyncio
import logging

from downloader import download_audio, download_video
from utils import generate_token, validate_token

from cookie_manager import CookieManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("youtube-api")

app = FastAPI()

os.makedirs("downloads", exist_ok=True)


cookie_manager = CookieManager()
cookie_manager.start_auto_refresh()

download_lock = asyncio.Lock()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "private music api"
    }

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "downloads": len(os.listdir("downloads")),
        "cookie_file": os.path.exists("cookies.txt")
    }

@app.get("/download")
async def download(url: str, type: str):
    token = generate_token(url)

    return {
        "download_token": token,
        "video_id": url,
        "type": type
    }

def is_valid_id(video_id: str):
    return isinstance(video_id, str) and len(video_id) == 11

@app.get("/stream/{video_id}")
async def stream(
    video_id: str,
    type: str,
    x_download_token: str = Header(None)
):
    # token check
    if not validate_token(x_download_token, video_id):
        raise HTTPException(403, "Invalid token")

    # id validation
    if not is_valid_id(video_id):
        raise HTTPException(400, "Invalid video id")

    logger.info(f"Streaming request: {video_id} ({type})")

    async with download_lock:

        try:
            if type == "audio":
                file_path = await download_audio(video_id)

                return FileResponse(
                    path=file_path,
                    media_type="audio/mpeg",
                    filename=f"{video_id}.mp3"
                )

            elif type == "video":
                file_path = await download_video(video_id)

                return FileResponse(
                    path=file_path,
                    media_type="video/mp4",
                    filename=f"{video_id}.mp4"
                )

            raise HTTPException(400, "Invalid type")

        except Exception as e:
            logger.error(f"Download failed: {e}")
            raise HTTPException(500, f"Download failed: {str(e)}")
