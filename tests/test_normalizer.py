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


def test_price_normalization_handles_spacing_none_and_malformed() -> None:
    raw_items = [
        {
            "category": "SIDES",
            "dish_name": "Fries",
            "raw_price": "$ 17",
            "description": "Crispy",
        },
        {
            "category": "SIDES",
            "dish_name": "Coleslaw",
            "raw_price": None,
            "description": "Fresh",
        },
        {
            "category": "SIDES",
            "dish_name": "Mystery",
            "raw_price": "$oops",
            "description": "Unknown",
        },
    ]

    normalized = normalize_items(raw_items)

    assert normalized[0].price == 17.0
    assert normalized[1].price is None
    assert normalized[2].price is None


def test_dish_id_generation_by_category_and_fallback() -> None:
    raw_items = [
        {
            "category": "BURGERS",
            "dish_name": "Classic Burger",
            "raw_price": "$10",
            "description": "",
        },
        {
            "category": "BURGERS",
            "dish_name": "Cheese Burger",
            "raw_price": "$11",
            "description": "",
        },
        {
            "category": "UNKNOWN CATEGORY",
            "dish_name": "Surprise",
            "raw_price": "$X",
            "description": "",
        },
    ]

    normalized = normalize_items(raw_items)

    assert normalized[0].dish_id == "BUR-001"
    assert normalized[1].dish_id == "BUR-002"
    assert normalized[2].dish_id == "GEN-001"
