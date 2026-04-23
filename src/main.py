from __future__ import annotations

from fastapi import FastAPI

from src.api.routes.menu import router as menu_router
from src.core.config import settings


app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)
app.include_router(menu_router, prefix=settings.api_prefix)
