from uuid import UUID
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "customer"
    OWNER = "owner"
    STAFF = "staff"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[UUID] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    role: UserRole = Field(default=UserRole.CUSTOMER)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
