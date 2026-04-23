from __future__ import annotations

from fastapi import FastAPI

from src.api.routes.menu import router as menu_router
from src.core.config import API_PREFIX, APP_TITLE, APP_VERSION


app = FastAPI(title=APP_TITLE, version=APP_VERSION)
app.include_router(menu_router, prefix=API_PREFIX)
