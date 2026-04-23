from __future__ import annotations

from pathlib import Path
import tempfile

from fastapi.concurrency import run_in_threadpool
from fastapi import APIRouter, File, HTTPException, UploadFile

from src.core.config import settings
from src.schemas.menu import MenuItemResponse, MenuUploadResponse
from src.services.menu_service import process_menu

router = APIRouter(prefix="/menu", tags=["menu"])


@router.post("/upload", response_model=MenuUploadResponse)
async def upload_menu(file: UploadFile = File(...)) -> MenuUploadResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Invalid file type. Only PDF is supported.")

    raw_bytes = await file.read()
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(raw_bytes) > settings.max_upload_size_bytes:
        max_mb = settings.max_upload_size_bytes // (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"File is too large. Maximum size is {max_mb} MB.",
        )

    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(raw_bytes)
            temp_path = Path(tmp.name)

        items = await run_in_threadpool(process_menu, temp_path)
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

    response_items = [MenuItemResponse.model_validate(item.model_dump()) for item in items]
    return MenuUploadResponse(items=response_items, count=len(response_items))
