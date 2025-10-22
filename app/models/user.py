from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum
from app.db.base import Base

class RoleEnum(str, enum.Enum):
    admin = "admin"
    employee = "employee"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(SQLEnum(RoleEnum, name="roleenum"), default=RoleEnum.employee, nullable=False)
    sector_id = Column(UUID(as_uuid=True), ForeignKey("sectors.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
