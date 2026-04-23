from __future__ import annotations

import argparse
from pathlib import Path

from extractor import extract_raw_items
from models import MenuDocument
from normalizer import normalize_items
from pdf_parser import parse_pdf_text
from utils import save_menu_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract structured menu data from a restaurant PDF."
    )
    parser.add_argument(
        "input_pdf",
        type=Path,
        help="Path to the input menu PDF file.",
    )
    return parser


def run_pipeline(input_pdf: Path, output_json: Path) -> MenuDocument:
    pages_text = parse_pdf_text(input_pdf)
    raw_items = extract_raw_items(pages_text)
    items = normalize_items(raw_items)

    warnings: list[str] = []
    if not items:
        warnings.append("No menu items were detected.")

    document = MenuDocument(source_file=str(input_pdf), items=items, warnings=warnings)
    save_menu_json(document, output_json)
    return document


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    output_json = project_root / "output" / "menu.json"

    try:
        document = run_pipeline(args.input_pdf, output_json)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        return 1
    except Exception as exc:  # pragma: no cover
        print(f"Unexpected error: {exc}")
        return 2

    print(f"Extracted {len(document.items)} menu items.")
    print(f"Saved JSON to: {output_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
