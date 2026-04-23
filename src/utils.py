from __future__ import annotations

from pathlib import Path

from models import MenuDocument


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_menu_json(document: MenuDocument, output_path: Path) -> None:
    ensure_directory(output_path.parent)
    output_path.write_text(document.model_dump_json(indent=2), encoding="utf-8")
