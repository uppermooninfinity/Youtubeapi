
import os
import asyncio
import yt_dlp

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def _run_yt_dlp(ydl_opts, url):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        lambda: yt_dlp.YoutubeDL(ydl_opts).download([url])
    )


def _find_file(video_id, ext):
    path = os.path.join(DOWNLOAD_DIR, f"{video_id}.{ext}")
    if os.path.exists(path):
        return path

    # fallback (yt-dlp sometimes changes extension slightly)
    for file in os.listdir(DOWNLOAD_DIR):
        if file.startswith(video_id):
            return os.path.join(DOWNLOAD_DIR, file)

    return path


async def download_audio(video_id: str):
    url = f"https://youtube.com/watch?v={video_id}"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_DIR}/{video_id}.%(ext)s",
        "cookiefile": "cookies.txt",
        "quiet": True,
        "noplaylist": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }],
    }

    await _run_yt_dlp(ydl_opts, url)

    return _find_file(video_id, "mp3")


async def download_video(video_id: str):
    url = f"https://youtube.com/watch?v={video_id}"

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": f"{DOWNLOAD_DIR}/{video_id}.%(ext)s",
        "cookiefile": "cookies.txt",
        "quiet": True,
        "noplaylist": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
    }

    await _run_yt_dlp(ydl_opts, url)

    return _find_file(video_id, "mp4")
