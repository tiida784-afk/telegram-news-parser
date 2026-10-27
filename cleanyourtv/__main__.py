import argparse
import asyncio

from .parser import run


def main():
    ap = argparse.ArgumentParser(prog="cleanyourtv", description="Fetch Telegram news and drop ads.")
    ap.add_argument("channels", nargs="+", help="channel usernames, e.g. rbc_news")
    ap.add_argument("-n", "--limit", type=int, default=100, help="posts per channel")
    ap.add_argument("-t", "--threshold", type=int, default=3, help="weak-marker count that flags an ad")
    ap.add_argument("-o", "--out", default="news.json")
    a = ap.parse_args()
    asyncio.run(run(a.channels, a.limit, a.threshold, a.out))


main()
