from __future__ import annotations

from pathlib import Path
import tempfile

from fastapi import APIRouter, File, HTTPException, UploadFile

from src.schemas.menu import MenuItemResponse
from src.services.menu_service import process_menu

router = APIRouter(prefix="/menu", tags=["menu"])


@router.post("/upload", response_model=list[MenuItemResponse])
async def upload_menu(file: UploadFile = File(...)) -> list[MenuItemResponse]:
    if file.content_type not in {"application/pdf", "application/x-pdf"}:
        raise HTTPException(status_code=400, detail="Invalid file type. Upload a PDF.")

    raw_bytes = await file.read()
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(raw_bytes)
            temp_path = Path(tmp.name)

        items = process_menu(temp_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to process menu: {exc}") from exc
    finally:
        await file.close()
        if temp_path is not None and temp_path.exists():
            temp_path.unlink(missing_ok=True)

    if not items:
        raise HTTPException(status_code=422, detail="No menu items found in PDF.")

    return [MenuItemResponse.model_validate(item.model_dump()) for item in items]
