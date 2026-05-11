# main.py

from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException
from fastapi.responses import FileResponse

from downloader import download_audio
from downloader import download_video

from utils import generate_token
from utils import validate_token

app = FastAPI()


@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "private music api"
    }


@app.get("/download")
async def download(url: str, type: str):
    token = generate_token(url)

    return {
        "download_token": token,
        "video_id": url,
        "type": type
    }


@app.get("/stream/{video_id}")
async def stream(
    video_id: str,
    type: str,
    x_download_token: str = Header(None)
):
    if not validate_token(x_download_token, video_id):
        raise HTTPException(403, "Invalid token")

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
