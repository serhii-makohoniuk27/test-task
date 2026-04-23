from __future__ import annotations

from pathlib import Path
from collections import OrderedDict

from src.extractor import extract_raw_items
from src.models import MenuItem
from src.normalizer import normalize_items


def process_menu(pdf_path: Path) -> list[MenuItem]:
    from src.pdf_parser import parse_pdf_text

    lines = parse_pdf_text(pdf_path)
    raw_items = extract_raw_items(lines)
    normalized_items = normalize_items(raw_items)
    return cleanup_menu_items(normalized_items)


def _clean_text(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned = value.replace("\ufffd", " ")
    cleaned = " ".join(cleaned.split())
    return cleaned or None


def cleanup_menu_items(items: list[MenuItem]) -> list[MenuItem]:
    cleaned_items: list[MenuItem] = []
    seen: set[tuple[str, float | None, str, str]] = set()

    for item in items:
        name = _clean_text(item.name)
        if not name:
            continue

        category = _clean_text(item.category)
        description = _clean_text(item.description)
        if description and description.lower() == "fpo description":
            description = None

        dedupe_key = (
            name.lower(),
            item.price,
            item.currency,
            (category or "").lower(),
        )
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)

        cleaned_items.append(
            item.model_copy(
                update={
                    "name": name,
                    "category": category,
                    "description": description,
                }
            )
        )

    return cleaned_items


def group_items_by_category(items: list[MenuItem]) -> list[dict[str, object]]:
    grouped: OrderedDict[str, list[MenuItem]] = OrderedDict()

    for item in items:
        category_name = (item.category or "UNCATEGORIZED").strip() or "UNCATEGORIZED"
        grouped.setdefault(category_name, []).append(item)

    return [{"name": name, "items": grouped_items} for name, grouped_items in grouped.items()]
