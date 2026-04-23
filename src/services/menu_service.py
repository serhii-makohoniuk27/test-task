from __future__ import annotations

from pathlib import Path

from src.extractor import extract_raw_items
from src.models import MenuItem
from src.normalizer import normalize_items
from src.pdf_parser import parse_pdf_text


def process_menu(pdf_path: Path) -> list[MenuItem]:
    lines = parse_pdf_text(pdf_path)
    raw_items = extract_raw_items(lines)
    return normalize_items(raw_items)
