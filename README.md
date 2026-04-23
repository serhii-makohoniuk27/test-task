# Menu PDF Extractor (Python 3.14)

Minimal CLI tool that extracts structured menu items from a restaurant menu PDF and writes normalized JSON output.

## Project Structure

- `src/main.py`
- `src/pdf_parser.py`
- `src/extractor.py`
- `src/normalizer.py`
- `src/models.py`
- `src/utils.py`
- `data/`
- `output/`

## Dependencies

- `pdfplumber`
- `pydantic` v2

## Quick Start

```bash
python -m pip install pdfplumber "pydantic>=2,<3"
```

Put your PDF in `data/` (or anywhere) and run:

```bash
python src/main.py data/menu.pdf
```

Output is written to:

- `output/menu.json`

## Notes

- Uses `pathlib` for path handling.
- Uses modern type hints (`list[str]`, `dict[str, Any]`) and `Optional` from `typing`.
- Extraction is regex-based and intentionally minimal; adapt patterns in `src/extractor.py` for specific menu layouts.
