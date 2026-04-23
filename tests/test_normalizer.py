from __future__ import annotations

from src.normalizer import normalize_items


def test_price_normalization_handles_numeric_and_x_placeholder() -> None:
    raw_items = [
        {
            "category": "BURGERS",
            "dish_name": "Classic Burger",
            "raw_price": "$12.50",
            "description": "Beef patty",
        },
        {
            "category": "DRINKS",
            "dish_name": "Market Drink",
            "raw_price": "$X",
            "description": "Seasonal",
        },
    ]

    normalized = normalize_items(raw_items)

    assert len(normalized) == 2
    assert normalized[0].price == 12.5
    assert normalized[0].currency == "USD"
    assert normalized[1].price is None
    assert normalized[1].currency == "USD"
