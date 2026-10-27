"""Fetch posts from Telegram channels (Telethon) and filter out ads."""
import json
import os
from typing import Iterable, Iterator

from .filters import classify, clean


def filter_posts(posts: Iterable[dict], weak_threshold: int = 3) -> Iterator[dict]:
    """Yield non-ad posts (dicts with 'text') with promo footers removed."""
    for post in posts:
        text = post.get("text") or ""
        if not text.strip() or classify(text, weak_threshold).is_ad:
            continue
        cleaned = clean(text)
        if cleaned:
            yield {**post, "text": cleaned}


async def fetch(channels, limit=100):
    from telethon import TelegramClient  # imported lazily so filters work without it

    client = TelegramClient(
        "cleanyourtv", int(os.environ["TG_API_ID"]), os.environ["TG_API_HASH"]
    )
    async with client:
        for ch in channels:
            async for m in client.iter_messages(ch, limit=limit):
                if m.message:
                    yield {
                        "channel": ch,
                        "id": m.id,
                        "date": m.date.isoformat(),
                        "text": m.message,
                    }


async def run(channels, limit, weak_threshold, out):
    raw = [p async for p in fetch(channels, limit)]
    kept = list(filter_posts(raw, weak_threshold))
    with open(out, "w", encoding="utf-8") as f:
        json.dump(kept, f, ensure_ascii=False, indent=2)
    print(f"{len(raw)} fetched, {len(raw) - len(kept)} dropped as ads/empty, {len(kept)} saved to {out}")
