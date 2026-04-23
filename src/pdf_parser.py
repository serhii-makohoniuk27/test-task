from __future__ import annotations

import re
from pathlib import Path

import pdfplumber


def _normalize_text_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw_line in text.splitlines():
        clean = re.sub(r"\s+", " ", raw_line).strip()
        if not clean:
            continue

        # Join hard hyphen wraps (e.g., "home-" + "made") produced by PDF line breaks.
        if lines and lines[-1].endswith("-"):
            lines[-1] = f"{lines[-1][:-1]}{clean}"
            continue

        lines.append(clean)

    return lines


def parse_pdf_text(pdf_path: Path) -> list[str]:
    if not pdf_path.exists():
        raise FileNotFoundError(f"Input PDF does not exist: {pdf_path}")

    text_lines: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            middle_x = page.width / 2
            left_bbox = (0, 0, middle_x, page.height)
            right_bbox = (middle_x, 0, page.width, page.height)

            left_text = page.crop(left_bbox).extract_text() or ""
            right_text = page.crop(right_bbox).extract_text() or ""

            # Reading order for two-column menus: left column first, then right.
            text_lines.extend(_normalize_text_lines(left_text))
            text_lines.extend(_normalize_text_lines(right_text))

    return text_lines
