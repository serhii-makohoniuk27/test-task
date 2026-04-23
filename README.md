# Menu PDF Extractor (Python 3.12+)

Prototype extractor that parses restaurant menu PDFs, normalizes dish data, and exports JSON through CLI and FastAPI.

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

## Reproduce Results

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Run tests:

```bash
python -m pytest -q
```

3. Run CLI extraction (replace input path with your PDF):

```bash
python -m src.cli data/menu.pdf --output output/menu.json
```

4. Run API:

```bash
uvicorn src.main:app --reload
```

5. Upload PDF to API:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/menu/upload" -F "file=@data/menu.pdf"
```

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

API response (`200`):

```json
{
	"categories": [
		{
			"name": "BURGERS",
			"items": [
				{
					"dish_id": "BUR-001",
					"name": "ALL AMERICAN BURGER",
					"price": 17.0,
					"currency": "USD",
					"category": "BURGERS",
					"description": "7 oz. steakburger, choice of cheese",
					"metadata": {}
				}
			]
		}
	],
	"total_items": 1
}
```

CLI output (`output/menu.json`):

```json
{
	"categories": [
		{
			"name": "BURGERS",
			"items": [
				{
					"category": "BURGERS",
					"dish_name": "ALL AMERICAN BURGER",
					"price": 17.0,
					"description": "7 oz. steakburger, choice of cheese",
					"dish_id": "BUR-001"
				}
			]
		}
	],
	"total_items": 1
}
```

Errors:

- `400`: invalid file type or empty upload
- `413`: file too large
- `422`: no menu items found
