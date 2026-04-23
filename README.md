# Menu PDF Extractor API (Python 3.14)

Minimal FastAPI service that extracts structured menu items from restaurant menu PDFs.

## Project Structure

- `src/main.py`
- `src/api/routes/menu.py`
- `src/services/menu_service.py`
- `src/core/config.py`
- `src/schemas/menu.py`
- `src/pdf_parser.py`
- `src/extractor.py`
- `src/normalizer.py`
- `src/models.py`
- `data/`
- `output/`

## Dependencies

- `pdfplumber`
- `pydantic` v2
- `fastapi`
- `uvicorn`
- `python-multipart`

## Quick Start

```bash
python -m pip install -r requirements.txt
```

Run API:

```bash
uvicorn src.main:app --reload
```

## Endpoint

- `POST /api/v1/menu/upload`

Upload a PDF file using `multipart/form-data` with field name `file`.

Response:

- `200`: list of menu items
- `400`: invalid file type or empty upload
- `422`: no menu items found
