from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.domain.models import Booking, BookingCreate, BookingStatus, CompanionProfile
from backend.app.infra.database import BookingRecord, CompanionRecord, UserRecord


class SqlAlchemyRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def register_user(self, email: str, role: str, city: str) -> str:
        user_id = f"usr-{uuid4().hex[:10]}"
        self.session.add(UserRecord(user_id=user_id, email=email, role=role, city=city))
        self.session.commit()
        return user_id

    def list_companions(self, city: str | None = None, category: str | None = None) -> list[CompanionProfile]:
        query = select(CompanionRecord)
        if city:
            query = query.where(CompanionRecord.city == city)
        records = list(self.session.scalars(query))
        if category:
            records = [record for record in records if category.lower() in record.categories.lower().split("|")]
        return [self._toCompanion(record) for record in records]

    def create_booking(self, payload: BookingCreate) -> Booking:
        companion = self.session.get(CompanionRecord, payload.companionId)
        if companion is None:
            raise ValueError(f"Unknown companion {payload.companionId}")
        record = BookingRecord(
            booking_id=f"bkg-{uuid4().hex[:10]}",
            customer_id=payload.customerId,
            companion_id=payload.companionId,
            category=payload.category,
            booking_date=payload.bookingDate,
            duration_hours=payload.durationHours,
            status=BookingStatus.pending.value,
            amount=companion.price_per_hour * payload.durationHours,
            created_at=datetime.now(timezone.utc),
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return self._toBooking(record)

    def list_bookings(self) -> list[Booking]:
        return [self._toBooking(record) for record in self.session.scalars(select(BookingRecord))]

    @staticmethod
    def _toCompanion(record: CompanionRecord) -> CompanionProfile:
        return CompanionProfile(companionId=record.companion_id, userId=record.user_id, name=record.name, city=record.city, age=record.age, categories=record.categories.split("|"), interests=record.interests.split("|"), pricePerHour=record.price_per_hour, rating=record.rating, photoUrl=record.photo_url)

    @staticmethod
    def _toBooking(record: BookingRecord) -> Booking:
        return Booking(bookingId=record.booking_id, customerId=record.customer_id, companionId=record.companion_id, category=record.category, bookingDate=record.booking_date, durationHours=record.duration_hours, status=BookingStatus(record.status), amount=record.amount, createdAt=record.created_at)
