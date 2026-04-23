from __future__ import annotations

from pydantic import BaseModel, Field


class MenuItemResponse(BaseModel):
    name: str
    price: float | None = None
    currency: str = "USD"
    category: str | None = None
    description: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)


class MenuUploadResponse(BaseModel):
    items: list[MenuItemResponse]
    count: int
