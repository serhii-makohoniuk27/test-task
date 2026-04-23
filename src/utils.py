from __future__ import annotations

import re
from typing import Optional

_PRICE_TOKEN_RE = re.compile(r"(?P<symbol>[\$€£])\s*(?P<value>\d+(?:\.\d{1,2})?|X)", re.IGNORECASE)
_PRICE_IN_LINE_RE = re.compile(r"\$\s*(\d+|X)", re.IGNORECASE)


def clean_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def merge_description_lines(parts: list[str]) -> Optional[str]:
    valid_parts = [clean_whitespace(part) for part in parts if _is_description_line(part)]
    valid_parts = [part for part in valid_parts if part]
    if not valid_parts:
        return None
    merged = clean_whitespace(" ".join(valid_parts))
    return merged or None


def parse_price_token(raw_price: Optional[str]) -> tuple[Optional[float], str]:
    if not raw_price:
        return None, "USD"

    cleaned = clean_whitespace(raw_price)
    match = _PRICE_TOKEN_RE.search(cleaned)
    if not match:
        return None, "USD"

    symbol = match.group("symbol")
    currency = {"$": "USD", "€": "EUR", "£": "GBP"}.get(symbol, "USD")

    value = match.group("value")
    if value.upper() == "X":
        return None, currency

    try:
        return float(value), currency
    except (TypeError, ValueError):
        return None, currency


def extract_price_segments(line: str) -> list[tuple[str, str | None]]:
    clean_line = clean_whitespace(line)
    if not clean_line:
        return []

    matches = list(_PRICE_IN_LINE_RE.finditer(clean_line))
    if not matches:
        return []

    segments: list[tuple[str, str | None]] = []
    name_start = 0

    for match in matches:
        name = clean_whitespace(clean_line[name_start:match.start()])
        price = clean_whitespace(match.group(0))
        if name:
            segments.append((name, price))
        name_start = match.end()

    return segments


def is_category(line: str) -> bool:
    clean_line = clean_whitespace(line)
    if len(clean_line) <= 3:
        return False
    if clean_line.endswith((".", ",", ";", ":")):
        return False
    if "$" in clean_line:
        return False
    if clean_line != clean_line.upper():
        return False

    allowed = sum(ch.isalpha() or ch.isspace() or ch in "&/-'" for ch in clean_line)
    return (allowed / len(clean_line)) >= 0.8


def is_dish_line(line: str) -> bool:
    return "$" in clean_whitespace(line)


def _is_description_line(line: str) -> bool:
    clean_line = clean_whitespace(line)
    if not clean_line:
        return False
    if is_dish_line(clean_line):
        return False
    if is_category(clean_line):
        return False
    return True
