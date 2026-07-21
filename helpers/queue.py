"""
Simple in-memory per-chat song queue.
For production with multiple workers, swap this for Redis/Mongo.
"""

from typing import Dict, List, Optional

_queues: Dict[int, List[dict]] = {}


def add_to_queue(chat_id: int, track: dict) -> int:
    """Add a track dict {title, url, stream_url, duration, requested_by} to the queue.
    Returns the position in queue (0 = now playing)."""
    _queues.setdefault(chat_id, [])
    _queues[chat_id].append(track)
    return len(_queues[chat_id]) - 1


def get_queue(chat_id: int) -> List[dict]:
    return _queues.get(chat_id, [])


def current_track(chat_id: int) -> Optional[dict]:
    q = _queues.get(chat_id)
    return q[0] if q else None


def pop_current(chat_id: int) -> Optional[dict]:
    """Remove the currently playing track and return the next one, if any."""
    q = _queues.get(chat_id)
    if not q:
        return None
    q.pop(0)
    return q[0] if q else None


def clear_queue(chat_id: int) -> None:
    _queues.pop(chat_id, None)


def is_active(chat_id: int) -> bool:
    return bool(_queues.get(chat_id))
