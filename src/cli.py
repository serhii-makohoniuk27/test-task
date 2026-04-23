from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.models import MenuItem
from src.services.menu_service import group_items_by_category, process_menu


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract structured menu items from a PDF file."
    )
    parser.add_argument("input_pdf", type=Path, help="Path to the input menu PDF")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output") / "menu.json",
        help="Path to output JSON file (default: output/menu.json)",
    )
    return parser


def run_cli(input_pdf: Path, output_path: Path) -> int:
    items = process_menu(input_pdf)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    grouped = group_items_by_category(items)

    categories: list[dict[str, object]] = []
    for group in grouped:
        category_name = str(group["name"])
        category_items = group["items"]
        formatted_items = [_format_assignment_item(item, category_name) for item in category_items]
        categories.append({"name": category_name, "items": formatted_items})

    payload = {"categories": categories, "total_items": len(items)}
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"Extracted {len(items)} menu items")
    print(f"Saved output to: {output_path}")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        return run_cli(args.input_pdf, args.output)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        return 1
    except Exception as exc:  # pragma: no cover
        print(f"Unexpected error: {exc}")
        return 2


def _format_assignment_item(item: MenuItem, category_name: str) -> dict[str, object | None]:
    return {
        "category": category_name,
        "dish_name": item.name,
        "price": item.price,
        "description": item.description,
        "dish_id": item.dish_id,
    }


if __name__ == "__main__":
    raise SystemExit(main())
