from __future__ import annotations

from src.models import MenuItem
from src.services.menu_service import cleanup_menu_items, group_items_by_category


def test_cleanup_menu_items_removes_duplicates_and_placeholder_description() -> None:
    items = [
        MenuItem(
            dish_id="BUR-001",
            name="Classic Burger",
            price=12.0,
            currency="USD",
            category="BURGERS",
            description="fpo description",
        ),
        MenuItem(
            dish_id="BUR-002",
            name="Classic Burger",
            price=12.0,
            currency="USD",
            category="BURGERS",
            description="Real description",
        ),
    ]

    cleaned = cleanup_menu_items(items)

    assert len(cleaned) == 1
    assert cleaned[0].name == "Classic Burger"
    assert cleaned[0].description is None


def test_cleanup_menu_items_normalizes_weird_characters() -> None:
    items = [
        MenuItem(
            dish_id="GEN-001",
            name="Fish � Chips",
            price=10.0,
            currency="USD",
            category="MAINS �",
            description="Crispy � flaky",
        )
    ]

    cleaned = cleanup_menu_items(items)

    assert len(cleaned) == 1
    assert cleaned[0].name == "Fish Chips"
    assert cleaned[0].category == "MAINS"
    assert cleaned[0].description == "Crispy flaky"


def test_group_items_by_category_groups_and_falls_back_to_uncategorized() -> None:
    items = [
        MenuItem(dish_id="BUR-001", name="Classic", category="BURGERS"),
        MenuItem(dish_id="SID-001", name="Fries", category="SIDES"),
        MenuItem(dish_id="GEN-001", name="Mystery", category=None),
    ]

    grouped = group_items_by_category(items)

    assert [group["name"] for group in grouped] == ["BURGERS", "SIDES", "UNCATEGORIZED"]
    assert len(grouped[0]["items"]) == 1
    assert len(grouped[1]["items"]) == 1
    assert len(grouped[2]["items"]) == 1
