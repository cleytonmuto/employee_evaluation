# app/schemas/evaluation.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class EvaluationCreate(BaseModel):
    evaluated_id: UUID
    score: int
    comments: Optional[str] = None

class EvaluationUpdate(BaseModel):
    score: Optional[int] = None
    comments: Optional[str] = None

class EvaluationOut(BaseModel):
    id: UUID
    evaluator_id: UUID
    evaluated_id: UUID
    score: int
    comments: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
