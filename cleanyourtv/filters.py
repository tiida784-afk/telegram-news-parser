"""Rule-based ad detection and cleaning for Telegram news posts (RU/EN)."""
import re
from dataclasses import dataclass

# Strong markers: any one of these means the whole post is an ad
# (Russian law requires "реклама" labelling and an erid token).
STRONG = [
    r"#реклама", r"#ad\b", r"\berid\b", r"на правах рекламы",
    r"рекламодатель", r"партн[её]рский материал", r"\bpromo(?:ted)?\b",
    r"промокод", r"\bпромо\b", r"^\s*реклама\b", r"\bsponsored\b",
]
# Weak markers: need several to flag a post.
WEAK = [
    r"скидк\w+", r"акци[яию]", r"купи\w*", r"закажи\w*", r"розыгрыш",
    r"подписывайся|подписывайтесь|подпишись", r"только сегодня",
    r"бесплатн\w+", r"курс\w* по", r"кэшбэк|кешбэк", r"бонус",
    r"\bbuy now\b", r"\bdiscount\b", r"\bgiveaway\b",
]
# Footer lines that are self-promotion / channel plugs, stripped from otherwise good posts.
FOOTER = re.compile(
    r"(подписаться|подписывайтесь|подписывайся|прислать новость|"
    r"наш (?:чат|канал)|мы в (?:max|телеграм|telegram|vk)|читайте нас|"
    r"@\w+\s*$|https?://t\.me/\+\S+|t\.me/joinchat)",
    re.I,
)
INVITE_LINK = re.compile(r"t\.me/(?:\+|joinchat/)\S+", re.I)

_strong = [re.compile(p, re.I | re.M) for p in STRONG]
_weak = [re.compile(p, re.I) for p in WEAK]


@dataclass
class Verdict:
    is_ad: bool
    score: int
    reasons: list


def classify(text: str, weak_threshold: int = 3) -> Verdict:
    """Return whether the post is an ad. Score: strong=10, weak=1, invite link=2."""
    reasons = [p.pattern for p in _strong if p.search(text)]
    score = 10 * len(reasons)
    weak = [p.pattern for p in _weak if p.search(text)]
    score += len(weak)
    reasons += weak
    if INVITE_LINK.search(text):
        score += 2
        reasons.append("invite-link")
    return Verdict(score >= 10 or len(weak) >= weak_threshold, score, reasons)


def clean(text: str) -> str:
    """Strip trailing channel plugs / promo lines from a non-ad post."""
    lines = text.rstrip().splitlines()
    while lines and (not lines[-1].strip() or FOOTER.search(lines[-1])):
        lines.pop()
    return "\n".join(lines).strip()
