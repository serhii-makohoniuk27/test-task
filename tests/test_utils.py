from __future__ import annotations

from src.utils import extract_price_segments, is_category, is_dish_line


def test_extract_price_segments_splits_multiple_items() -> None:
    line = "4 WINGS & 4 SAUCES $X 8 WINGS & 8 SAUCES $X"

    segments = extract_price_segments(line)

    assert segments == [
        ("4 WINGS & 4 SAUCES", "$X"),
        ("8 WINGS & 8 SAUCES", "$X"),
    ]


def test_is_category_and_is_dish_line() -> None:
    assert is_category("DRINK MENU") is True
    assert is_category("All American Burger") is False
    assert is_dish_line("ALL AMERICAN BURGER $17") is True
