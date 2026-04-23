from __future__ import annotations

from pathlib import Path

import pdfplumber


def parse_pdf_text(pdf_path: Path) -> list[str]:
    if not pdf_path.exists():
        raise FileNotFoundError(f"Input PDF does not exist: {pdf_path}")

    pages_text: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pages_text.append(page.extract_text() or "")

    return pages_text
