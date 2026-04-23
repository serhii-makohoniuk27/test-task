from __future__ import annotations

import re
from typing import Any, Optional

from src.models import MenuItem


type RawItem = dict[str, Any]


def _parse_raw_price(raw_price: Optional[str]) -> tuple[Optional[float], str]:
    if not raw_price:
        return None, "USD"

    value = raw_price.strip()
    currency = "USD"
    if value.startswith("$"):
        currency = "USD"
    elif value.startswith("€"):
        currency = "EUR"
    elif value.startswith("£"):
        currency = "GBP"

    numeric = re.sub(r"^[\$€£]\s*", "", value)
    try:
        return float(numeric), currency
    except ValueError:
        # Handles placeholders like "$X" where no numeric value is available.
        return None, currency


def normalize_items(raw_items: list[RawItem]) -> list[MenuItem]:
    normalized: list[MenuItem] = []
    seen: set[tuple[str, Optional[float], str]] = set()

    for item in raw_items:
        name = str(item.get("dish_name", "")).strip()
        if not name:
            continue

        price, currency = _parse_raw_price(item.get("raw_price"))
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
