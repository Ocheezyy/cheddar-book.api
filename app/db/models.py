from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from uuid import UUID


class Business(SQLModel, table=True):
    __tablename__ = "businesses"

    id: Optional[UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    owner_id: UUID = Field(foreign_key="users.id")

    staff: List["Staff"] = Relationship(back_populates="business")
    services: List["Service"] = Relationship(back_populates="business")


class Staff(SQLModel, table=True):
    __tablename__ = "staff"

    id: Optional[UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    business_id: UUID = Field(foreign_key="businesses.id")
    name: str
    role: Optional[str] = None

    business: Business = Relationship(back_populates="staff")


class Service(SQLModel, table=True):
    __tablename__ = "services"

    id: Optional[UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    business_id: UUID = Field(foreign_key="businesses.id")
    name: str
    duration_minutes: int
    price: float

    business: Business = Relationship(back_populates="services")


class Booking(SQLModel, table=True):
    __tablename__ = "bookings"

    id: Optional[UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    business_id: UUID = Field(foreign_key="businesses.id")
    customer_id: UUID = Field(foreign_key="users.id")
    service_id: UUID = Field(foreign_key="services.id")
    customer_name: Optional[str]
    customer_email: Optional[str]
    service: str
    start_time: datetime
    end_time: datetime

    business: Business = Relationship()
    service: Service = Relationship()
    staff: Staff = Relationship()
