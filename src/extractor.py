from __future__ import annotations

from typing import Any, Optional

from src.utils import (
    clean_whitespace,
    extract_price_segments,
    is_category,
    is_dish_line,
    merge_description_lines,
)


type RawItem = dict[str, Any]
_NO_PRICE_LIST_CATEGORIES = {"SIGNATURE SAUCES", "SIGNATURE RUBS"}


def _clean_line(value: str) -> str:
    return clean_whitespace(value)


def _is_category_header(line: str, next_line: Optional[str]) -> bool:
    if not is_category(line):
        return False

    if line in _NO_PRICE_LIST_CATEGORIES:
        return True

    if not next_line:
        return True
    return is_dish_line(next_line) or not is_category(next_line)


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


def _should_start_new_no_price_dish(line: str, current_dish: RawItem, description_parts: list[str]) -> bool:
    if not _looks_like_dish_name(line):
        return False
    if is_dish_line(line):
        return False
    if not description_parts:
        return False

    dish_name = str(current_dish.get("dish_name", ""))
    if line.lower() == dish_name.lower():
        return False

    words = [word for word in line.split() if any(ch.isalpha() for ch in word)]
    if not words:
        return False
    title_like_words = sum(1 for word in words if word[:1].isupper())
    if title_like_words / len(words) < 0.6:
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

        current_dish["description"] = _merge_description(description_parts) or ""
        extracted.append(current_dish)
        current_dish = None
        description_parts = []

    for index, raw_line in enumerate(lines):
        line = _clean_line(raw_line)
        if not line:
            continue

        if current_category in _NO_PRICE_LIST_CATEGORIES and line not in _NO_PRICE_LIST_CATEGORIES:
            finalize_current_dish()
            extracted.append(
                {
                    "category": current_category,
                    "dish_name": line,
                    "raw_price": None,
                    "description": "",
                }
            )
            continue

        next_line = _next_non_empty_line(lines, index)
        if _is_category_header(line, next_line):
            finalize_current_dish()
            current_category = line
            continue

        if is_dish_line(line):
            segments = extract_price_segments(line)
            if not segments:
                continue

            finalize_current_dish()

            if len(segments) > 1:
                for dish_name, raw_price in segments:
                    extracted.append(
                        {
                            "category": current_category,
                            "dish_name": _clean_line(dish_name.strip(".- ")),
                            "raw_price": raw_price,
                            "description": "",
                        }
                    )
                continue

            dish_name, raw_price = segments[0]
            current_dish = {
                "category": current_category,
                "dish_name": _clean_line(dish_name.strip(".- ")),
                "raw_price": raw_price,
                "description": "",
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
                    "description": "",
                }
                continue
            if not is_dish_line(line) and not is_category(line):
                description_parts.append(line)

    finalize_current_dish()

    return extracted
