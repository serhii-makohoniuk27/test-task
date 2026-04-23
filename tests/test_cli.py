from __future__ import annotations

import json
from pathlib import Path

from src.cli import run_cli
from src.models import MenuItem


def test_run_cli_writes_assignment_shape(monkeypatch, tmp_path: Path) -> None:
    sample_items = [
        MenuItem(
            dish_id="BUR-001",
            name="ALL AMERICAN BURGER",
            price=17.0,
            category="BURGERS",
            description="7 oz. steakburger",
        )
    ]

    monkeypatch.setattr("src.cli.process_menu", lambda _: sample_items)

    output_path = tmp_path / "menu.json"
    exit_code = run_cli(Path("dummy.pdf"), output_path)

    assert exit_code == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert payload["total_items"] == 1
    assert payload["categories"][0]["name"] == "BURGERS"
    item = payload["categories"][0]["items"][0]
    assert item == {
        "category": "BURGERS",
        "dish_name": "ALL AMERICAN BURGER",
        "price": 17.0,
        "description": "7 oz. steakburger",
        "dish_id": "BUR-001",
    }
