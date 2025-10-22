import uuid
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evaluator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    evaluated_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    sector_id = Column(UUID(as_uuid=True), ForeignKey("sectors.id"))
    score = Column(Integer, nullable=False)
    comments = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
