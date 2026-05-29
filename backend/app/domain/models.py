from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    customer = "customer"
    companion = "companion"


class BookingStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    completed = "completed"
    cancelled = "cancelled"


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: UserRole
    city: str = "Москва"


class CompanionProfile(BaseModel):
    companionId: str
    userId: str
    name: str
    city: str
    age: int = Field(ge=18, le=100)
    categories: list[str]
    interests: list[str]
    pricePerHour: float = Field(gt=0)
    rating: float = Field(ge=1, le=5)
    photoUrl: Optional[str] = None


class BookingCreate(BaseModel):
    customerId: str
    companionId: str
    category: str
    bookingDate: datetime
    durationHours: int = Field(gt=0, le=12)


class Booking(BaseModel):
    bookingId: str
    customerId: str
    companionId: str
    category: str
    bookingDate: datetime
    durationHours: int
    status: BookingStatus
    amount: float
    createdAt: datetime


class Review(BaseModel):
    reviewId: str
    bookingId: str
    customerId: str
    companionId: str
    rating: int = Field(ge=1, le=5)
    text: str
    createdAt: datetime


class EventEnvelope(BaseModel):
    eventId: str
    eventType: str
    eventTime: datetime
    payload: dict
