from __future__ import annotations

import re
from typing import Any, Optional

from src.utils import clean_whitespace, merge_description_lines


type RawItem = dict[str, Any]

_PRICE_TOKEN_RE = r"[\$€£]\s*(?:\d+(?:\.\d{1,2})?|X)"
_DISH_WITH_PRICE_RE = re.compile(rf"^(?P<name>.+?)\s*(?:\.{2,}|\s+)\s*(?P<price>{_PRICE_TOKEN_RE})$", re.IGNORECASE)
_PRICE_ONLY_RE = re.compile(rf"^(?P<price>{_PRICE_TOKEN_RE})$", re.IGNORECASE)
_CATEGORY_ALLOWED_RE = re.compile(r"^[A-Z0-9 &'/\-]+$")


def _clean_line(value: str) -> str:
    return clean_whitespace(value)


def _is_category_header(line: str, next_line: Optional[str]) -> bool:
    if not line:
        return False
    if line != line.upper():
        return False
    if not any(ch.isalpha() for ch in line):
        return False
    if len(line.split()) > 4:
        return False
    if len(line) > 32:
        return False
    if line.endswith((".", ",", ";", ":")):
        return False
    if _PRICE_ONLY_RE.match(line):
        return False
    if not _CATEGORY_ALLOWED_RE.match(line):
        return False
    if not next_line:
        return True

    # Reduce false positives: category headers are usually followed by dish-like lines.
    return bool(_DISH_WITH_PRICE_RE.match(next_line) or _looks_like_dish_name(next_line))


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
    return merge_description_lines(parts)


def _next_non_empty_line(lines: list[str], start_index: int) -> Optional[str]:
    for index in range(start_index + 1, len(lines)):
        candidate = _clean_line(lines[index])
        if candidate:
            return candidate
    return None


def _looks_like_standalone_title(line: str) -> bool:
    words = [w for w in line.split() if any(ch.isalpha() for ch in w)]
    if not words:
        return False

    titled_words = sum(1 for word in words if word[:1].isupper())
    return titled_words / len(words) >= 0.6


def _should_start_new_no_price_dish(line: str, current_dish: RawItem, description_parts: list[str]) -> bool:
    if not _looks_like_dish_name(line):
        return False
    if _DISH_WITH_PRICE_RE.match(line):
        return False
    if not description_parts:
        return False

    dish_name = str(current_dish.get("dish_name", ""))
    if line.lower() == dish_name.lower():
        return False

    if not _looks_like_standalone_title(line):
        return False

    return True


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

    for index, raw_line in enumerate(lines):
        line = _clean_line(raw_line)
        if not line:
            continue

        next_line = _next_non_empty_line(lines, index)
        if _is_category_header(line, next_line):
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
            if _should_start_new_no_price_dish(line, current_dish, description_parts):
                finalize_current_dish()
                current_dish = {
                    "category": current_category,
                    "dish_name": line,
                    "raw_price": None,
                    "description": None,
                }
                continue

            description_parts.append(line)

    finalize_current_dish()

    return extracted
