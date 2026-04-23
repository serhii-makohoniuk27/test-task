from __future__ import annotations

import re
from typing import Optional

_PRICE_TOKEN_RE = re.compile(r"^(?P<symbol>[\$€£])\s*(?P<value>(?:\d+(?:\.\d{1,2})?)|X)$", re.IGNORECASE)


def clean_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def merge_description_lines(parts: list[str]) -> Optional[str]:
    if not parts:
        return None
    merged = clean_whitespace(" ".join(parts))
    return merged or None


def parse_price_token(raw_price: Optional[str]) -> tuple[Optional[float], str]:
    if not raw_price:
        return None, "USD"

    cleaned = clean_whitespace(raw_price)
    match = _PRICE_TOKEN_RE.match(cleaned)
    if not match:
        return None, "USD"

    symbol = match.group("symbol")
    currency = {"$": "USD", "€": "EUR", "£": "GBP"}.get(symbol, "USD")

    value = match.group("value")
    if value.upper() == "X":
        return None, currency

    return float(value), currency
