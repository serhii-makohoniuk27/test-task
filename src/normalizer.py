from __future__ import annotations

from typing import Any, Optional

from src.models import MenuItem
from src.utils import parse_price_token


type RawItem = dict[str, Any]


def normalize_items(raw_items: list[RawItem]) -> list[MenuItem]:
    normalized: list[MenuItem] = []
    seen: set[tuple[str, Optional[float], str]] = set()

    for item in raw_items:
        name = str(item.get("dish_name", "")).strip()
        if not name:
            continue

        price, currency = parse_price_token(item.get("raw_price"))
        category = item.get("category")
        description = item.get("description")

        key = (name.lower(), price, currency)
        if key in seen:
            continue
        seen.add(key)

        normalized.append(
            MenuItem(
                name=name,
                price=price,
                currency=currency,
                category=str(category).strip() if isinstance(category, str) and category.strip() else None,
                description=str(description).strip() if isinstance(description, str) and description.strip() else None,
            )
        )

    return normalized
