import asyncio
import yt_dlp

async def _run_yt_dlp(ydl_opts, url):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=False)
    )


async def get_audio_stream(video_id: str):
    url = f"https://youtube.com/watch?v={video_id}"

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True
    }

    info = await _run_yt_dlp(ydl_opts, url)
    return info["url"]


async def get_video_stream(video_id: str):
    url = f"https://youtube.com/watch?v={video_id}"

    ydl_opts = {
        "format": "best",
        "quiet": True,
        "noplaylist": True
    }

    info = await _run_yt_dlp(ydl_opts, url)
    return info["url"]
