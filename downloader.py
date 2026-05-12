# downloader.py

import os
import asyncio
import yt_dlp

DOWNLOAD_DIR = "downloads"


async def download_audio(video_id: str):
    final_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")

    if os.path.exists(final_path):
        return final_path

    url = f"https://youtube.com/watch?v={video_id}"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"downloads/{video_id}.%(ext)s",
        "quiet": True,
        "noplaylist": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "external_downloader": "aria2c",
        "external_downloader_args": [
            "-x", "16",
            "-k", "1M"
        ],
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }],
    }

    loop = asyncio.get_event_loop()

    await loop.run_in_executor(
        None,
        lambda: yt_dlp.YoutubeDL(ydl_opts).download([url])
    )

    return final_path


async def download_video(video_id: str):
    final_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")

    if os.path.exists(final_path):
        return final_path

    url = f"https://youtube.com/watch?v={video_id}"

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": f"downloads/{video_id}.%(ext)s",
        "cookiefile": "cookies.txt",
        "quiet": True,
        "noplaylist": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "external_downloader": "aria2c",
        "external_downloader_args": [
            "-x", "16",
            "-k", "1M"
        ],
    }

    loop = asyncio.get_event_loop()

    await loop.run_in_executor(
        None,
        lambda: yt_dlp.YoutubeDL(ydl_opts).download([url])
    )

    return final_path
