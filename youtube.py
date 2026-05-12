from yt_dlp import YoutubeDL


YDL_OPTS_AUDIO = {
    "format": "bestaudio/best",
    "quiet": True,
    "noplaylist": True,
    "geo_bypass": True,
    "nocheckcertificate": True
}

YDL_OPTS_VIDEO = {
    "format": "best",
    "quiet": True,
    "noplaylist": True,
    "geo_bypass": True,
    "nocheckcertificate": True
}


def _extract(video_id: str, opts: dict):
    url = f"https://youtube.com/watch?v={video_id}"

    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get("url")


def get_stream_url(video_id: str):
    try:
        return _extract(video_id, YDL_OPTS_AUDIO)
    except Exception:
        return None


def get_video_stream_url(video_id: str):
    try:
        return _extract(video_id, YDL_OPTS_VIDEO)
    except Exception:
        return None
