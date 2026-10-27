# telegram-news-parser (cleanyourtv)

Fetches posts from Telegram news channels and drops advertising.

- Ads are detected by rules (`#реклама`, `erid`, promo codes, invite links, several sales phrases).
- Channel plugs at the end of good posts ("Подписаться…", `@channel`) are stripped.

## Usage

```
pip install -r requirements.txt
export TG_API_ID=... TG_API_HASH=...   # from https://my.telegram.org
python -m cleanyourtv rbc_news meduzalive -n 200 -o news.json
```

Tune with `-t` (how many weak ad markers flag a post, default 3). Edit `cleanyourtv/filters.py` to add patterns.

## Tests

```
pip install pytest && pytest
```
