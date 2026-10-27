from cleanyourtv.filters import classify, clean
from cleanyourtv.parser import filter_posts


def test_strong_marker_is_ad():
    assert classify("Новый телевизор! #реклама erid: 2VtzqwP").is_ad
    assert classify("Используйте промокод TV10").is_ad


def test_weak_markers_need_several():
    assert not classify("Магазин объявил скидку на сезон").is_ad
    assert classify("Скидки! Купи сейчас, закажи и получи бонус").is_ad


def test_news_kept_and_footer_stripped():
    text = "Правительство утвердило бюджет.\n\nПодписаться на канал\n@newschannel"
    assert not classify(text).is_ad
    assert clean(text) == "Правительство утвердило бюджет."


def test_filter_posts():
    posts = [{"text": "Новость дня"}, {"text": "Реклама. erid: abc"}, {"text": "  "}]
    assert [p["text"] for p in filter_posts(posts)] == ["Новость дня"]
