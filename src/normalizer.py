from __future__ import annotations

from collections import defaultdict
from typing import Any, Optional

from src.models import MenuItem
from src.utils import parse_price_token


type RawItem = dict[str, Any]

_CATEGORY_CODE_MAP: dict[str, str] = {
    "BURGERS": "BUR",
    "SIDES": "SID",
    "DRINK MENU": "DRI",
    "LEADING OFF": "LEA",
    "WINGS": "WIN",
    "SLIDER TOWERS": "SLI",
    "SIGNATURE SAUCES": "SAU",
    "SIGNATURE RUBS": "RUB",
}


def _category_code(category: Optional[str]) -> str:
    if not category:
        return "GEN"
    return _CATEGORY_CODE_MAP.get(category.strip().upper(), "GEN")


def normalize_items(raw_items: list[RawItem]) -> list[MenuItem]:
    normalized: list[MenuItem] = []
    seen: set[tuple[str, Optional[float], str]] = set()
    sequence_by_code: dict[str, int] = defaultdict(int)

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

        code = _category_code(category if isinstance(category, str) else None)
        sequence_by_code[code] += 1
        dish_id = f"{code}-{sequence_by_code[code]:03d}"

        normalized.append(
            MenuItem(
                dish_id=dish_id,
                name=name,
                price=price,
                currency=currency,
                category=str(category).strip() if isinstance(category, str) and category.strip() else None,
                description=str(description).strip() if isinstance(description, str) and description.strip() else None,
            )
        )

    return normalized
