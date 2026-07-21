"""
Resolves a search query or URL into a playable audio stream using yt-dlp.
"""

import asyncio
from typing import Optional

import yt_dlp

from config import COOKIES_FILE, DURATION_LIMIT_MIN

YDL_OPTS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
    "geo_bypass": True,
    "nocheckcertificate": True,
}
if COOKIES_FILE:
    YDL_OPTS["cookiefile"] = COOKIES_FILE


def _extract(query: str) -> dict:
    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        info = ydl.extract_info(query, download=False)
        if "entries" in info:  # search result list
            info = info["entries"][0]
        return info


async def resolve_track(query: str) -> Optional[dict]:
    """Run the blocking yt-dlp extraction in a thread and return track info."""
    loop = asyncio.get_event_loop()
    try:
        info = await loop.run_in_executor(None, _extract, query)
    except Exception as e:
        print(f"[youtube] extraction failed: {e}")
        return None

    duration = info.get("duration") or 0
    if duration and duration > DURATION_LIMIT_MIN * 60:
        return None

    return {
        "title": info.get("title", "Unknown title"),
        "url": info.get("webpage_url", query),
        "stream_url": info.get("url"),
        "duration": duration,
        "thumbnail": info.get("thumbnail"),
    }
