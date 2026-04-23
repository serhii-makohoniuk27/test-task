from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class MenuItem(BaseModel):
    name: str
    price: Optional[float] = None
    currency: str = "USD"
    category: Optional[str] = None
    description: Optional[str] = None
    metadata: dict[str, str] = Field(default_factory=dict)


class MenuDocument(BaseModel):
    source_file: str
    items: list[MenuItem]
    warnings: list[str] = Field(default_factory=list)
