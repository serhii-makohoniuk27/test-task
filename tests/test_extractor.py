from __future__ import annotations

from src.extractor import extract_raw_items
from src.utils import merge_description_lines


def test_category_detection_avoids_false_positive() -> None:
    lines = [
        "NOT A CATEGORY.",
        "Classic Burger $12",
        "House sauce",
    ]

    items = extract_raw_items(lines)

    assert len(items) == 1
    assert items[0]["dish_name"] == "Classic Burger"
    assert items[0]["category"] is None


def test_description_merges_multiline_text() -> None:
    lines = [
        "BURGERS",
        "Classic Burger $12",
        "100% beef patty",
        "house sauce",
        "toasted brioche bun",
    ]

    items = extract_raw_items(lines)

    assert len(items) == 1
    assert items[0]["description"] == "100% beef patty house sauce toasted brioche bun"
    assert merge_description_lines(["line one", "line two"]) == "line one line two"
