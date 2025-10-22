# app/schemas/sector.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class SectorCreate(BaseModel):
    name: str
    description: Optional[str] = None

class SectorOut(SectorCreate):
    id: UUID

    class Config:
        from_attributes = True
