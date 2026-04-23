from __future__ import annotations

import re
from typing import Any, Optional


type RawItem = dict[str, Any]

_PRICE_LINE_RE = re.compile(
    r"^(?P<name>.+?)\s+(?P<currency>[\$€£])?(?P<price>\d+(?:\.\d{1,2})?)$"
)


def _parse_price(value: str) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def extract_raw_items(pages_text: list[str]) -> list[RawItem]:
    extracted: list[RawItem] = []

    for page_index, page_text in enumerate(pages_text, start=1):
        for line_index, line in enumerate(page_text.splitlines(), start=1):
            clean = line.strip()
            if not clean:
                continue

            match = _PRICE_LINE_RE.match(clean)
            if not match:
                continue

            name = match.group("name").strip(".- ")
            price = _parse_price(match.group("price"))
            currency_symbol = match.group("currency")

            if not name:
                continue

            extracted.append(
                {
                    "name": name,
                    "price": price,
                    "currency_symbol": currency_symbol,
                    "metadata": {
                        "page": str(page_index),
                        "line": str(line_index),
                    },
                }
            )

    return extracted
