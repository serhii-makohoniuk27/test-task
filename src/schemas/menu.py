from __future__ import annotations

from pydantic import BaseModel, Field


class MenuItemResponse(BaseModel):
    dish_id: str
    name: str
    price: float | None = None
    currency: str = "USD"
    category: str | None = None
    description: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)


class CategoryResponse(BaseModel):
    name: str
    items: list[MenuItemResponse]


class MenuUploadResponse(BaseModel):
    categories: list[CategoryResponse]
    total_items: int
