from __future__ import annotations

import re
from typing import Any, Optional


type RawItem = dict[str, Any]

_PRICE_TOKEN_RE = r"\$[A-Za-z0-9]+(?:\.\d{1,2})?"
_DISH_WITH_PRICE_RE = re.compile(
    rf"^(?P<name>.+?)\s*(?:\.{2,}|\s+)\s*(?P<price>{_PRICE_TOKEN_RE})$"
)
_PRICE_ONLY_RE = re.compile(rf"^(?P<price>{_PRICE_TOKEN_RE})$")
_CATEGORY_ALLOWED_RE = re.compile(r"^[A-Z0-9 &'/\-]+$")


def _clean_line(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _is_category_header(line: str) -> bool:
    if not line:
        return False
    if line != line.upper():
        return False
    if not any(ch.isalpha() for ch in line):
        return False
    if _PRICE_ONLY_RE.match(line):
        return False
    return bool(_CATEGORY_ALLOWED_RE.match(line))


def _looks_like_dish_name(line: str) -> bool:
    if not line:
        return False
    words = line.split()
    if len(words) > 8:
        return False
    if line.endswith((".", ",", ";", ":")):
        return False
    alpha_ratio = sum(ch.isalpha() for ch in line) / max(len(line), 1)
    return alpha_ratio >= 0.45


def _merge_description(parts: list[str]) -> Optional[str]:
    if not parts:
        return None
    merged = _clean_line(" ".join(parts))
    return merged or None


def extract_raw_items(lines: list[str]) -> list[RawItem]:
    extracted: list[RawItem] = []
    current_category: Optional[str] = None
    current_dish: Optional[RawItem] = None
    description_parts: list[str] = []

    def finalize_current_dish() -> None:
        nonlocal current_dish, description_parts
        if current_dish is None:
            return

        current_dish["description"] = _merge_description(description_parts)
        extracted.append(current_dish)
        current_dish = None
        description_parts = []

    for raw_line in lines:
        line = _clean_line(raw_line)
        if not line:
            continue

        if _is_category_header(line):
            finalize_current_dish()
            current_category = line
            continue

        dish_with_price = _DISH_WITH_PRICE_RE.match(line)
        if dish_with_price:
            finalize_current_dish()
            current_dish = {
                "category": current_category,
                "dish_name": _clean_line(dish_with_price.group("name").strip(".- ")),
                "raw_price": dish_with_price.group("price"),
                "description": None,
            }
            continue

        if current_dish is None and _looks_like_dish_name(line):
            current_dish = {
                "category": current_category,
                "dish_name": line,
                "raw_price": None,
                "description": None,
            }
            continue

        if current_dish is not None:
            description_parts.append(line)

    finalize_current_dish()

    return extracted
