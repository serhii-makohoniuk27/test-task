from __future__ import annotations

from typing import Any, Optional

from models import MenuItem


type RawItem = dict[str, Any]


def _currency_from_symbol(symbol: Optional[str]) -> str:
    match symbol:
        case "$":
            return "USD"
        case "€":
            return "EUR"
        case "£":
            return "GBP"
        case _:
            return "USD"


def normalize_items(raw_items: list[RawItem]) -> list[MenuItem]:
    normalized: list[MenuItem] = []
    seen: set[tuple[str, Optional[float], str]] = set()

    for item in raw_items:
        name = str(item.get("name", "")).strip()
        if not name:
            continue

        price_value = item.get("price")
        price: Optional[float] = float(price_value) if isinstance(price_value, (int, float)) else None
        currency = _currency_from_symbol(item.get("currency_symbol"))

        key = (name.lower(), price, currency)
        if key in seen:
            continue
        seen.add(key)

        metadata = item.get("metadata", {})
        safe_metadata = {str(k): str(v) for k, v in metadata.items()} if isinstance(metadata, dict) else {}

        normalized.append(
            MenuItem(
                name=name,
                price=price,
                currency=currency,
                metadata=safe_metadata,
            )
        )

    return normalized
