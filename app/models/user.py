import uuid
import enum
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base


class RoleEnum(str, enum.Enum):
    ADMIN  = "admin"
    EMPLOYEE = "employee"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(
        SQLEnum(RoleEnum, name="roleenum"),
        default=RoleEnum.EMPLOYEE.value,
        nullable=False,
    )
    sector_id = Column(UUID(as_uuid=True), ForeignKey("sectors.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
