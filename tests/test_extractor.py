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


def test_description_merge_normalizes_line_break_spacing() -> None:
    lines = [
        "BURGERS",
        "ALL AMERICAN BURGER $17",
        "brioche bun ",
        "  with sauce",
    ]

    items = extract_raw_items(lines)

    assert len(items) == 1
    assert items[0]["description"] == "brioche bun with sauce"


def test_splits_multiple_items_in_single_line() -> None:
    lines = [
        "WINGS",
        "4 WINGS & 4 SAUCES $X 8 WINGS & 8 SAUCES $X",
    ]

    items = extract_raw_items(lines)

    assert len(items) == 2
    assert items[0]["dish_name"] == "4 WINGS & 4 SAUCES"
    assert items[0]["raw_price"] == "$X"
    assert items[0]["description"] == ""
    assert items[1]["dish_name"] == "8 WINGS & 8 SAUCES"
    assert items[1]["raw_price"] == "$X"


def test_signature_sections_are_items_without_description() -> None:
    lines = [
        "SIGNATURE SAUCES",
        "GARLIC PARMESAN",
        "SMOKY BBQ",
    ]

    items = extract_raw_items(lines)

    assert len(items) == 2
    assert items[0] == {
        "category": "SIGNATURE SAUCES",
        "dish_name": "GARLIC PARMESAN",
        "raw_price": None,
        "description": "",
    }
    assert items[1]["dish_name"] == "SMOKY BBQ"
