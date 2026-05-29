import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.app.domain.models import BookingCreate, EventEnvelope, UserCreate
from backend.app.infra.database import getSession
from backend.app.infra.events import EventPublisher
from backend.app.infra.repository import SqlAlchemyRepository

router = APIRouter()
publisher = EventPublisher()
logger = logging.getLogger(__name__)


def repository(session: Session = Depends(getSession)) -> SqlAlchemyRepository:
    return SqlAlchemyRepository(session)


@router.get("/health")
def health(session: Session = Depends(getSession)) -> dict:
    session.execute(text("SELECT 1"))
    return {"status": "ok", "service": "companion-api", "database": "ok"}


@router.post("/auth/register")
def register(payload: UserCreate, repo: SqlAlchemyRepository = Depends(repository)) -> EventEnvelope:
    userId = repo.register_user(payload.email, payload.role.value, payload.city)
    event = publisher.publish("user_registered", {"userId": userId, "email": payload.email, "role": payload.role.value, "city": payload.city})
    logger.info("user_registered userId=%s role=%s", userId, payload.role.value)
    return event


@router.get("/companions")
def listCompanions(city: str | None = None, category: str | None = None, repo: SqlAlchemyRepository = Depends(repository)) -> list[dict]:
    return [item.model_dump() for item in repo.list_companions(city=city, category=category)]


@router.post("/bookings")
def createBooking(payload: BookingCreate, repo: SqlAlchemyRepository = Depends(repository)) -> dict:
    try:
        booking = repo.create_booking(payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    publisher.publish("booking_created", booking.model_dump(mode="json"))
    logger.info("booking_created bookingId=%s companionId=%s", booking.bookingId, booking.companionId)
    return booking.model_dump(mode="json")


@router.get("/bookings")
def listBookings(repo: SqlAlchemyRepository = Depends(repository)) -> list[dict]:
    return [item.model_dump(mode="json") for item in repo.list_bookings()]


@router.get("/events/export")
def exportEvents() -> list[dict]:
    return mockEvents()


@router.get("/mock/events")
def mockEvents() -> list[dict]:
    now = datetime.now(timezone.utc).isoformat()
    return [
        {"eventType": "user_registered", "eventTime": now, "payload": {"userId": "usr-301", "role": "customer", "city": "Москва"}},
        {"eventType": "booking_created", "eventTime": now, "payload": {"bookingId": "bkg-301", "companionId": "cmp-001", "customerId": "usr-301", "status": "pending", "rating": 5, "amount": 2400}},
        {"eventType": "message_sent", "eventTime": now, "payload": {"chatId": "chat-1", "senderId": "usr-301", "receiverId": "cmp-001", "responseTimeSeconds": 180}},
        {"eventType": "review_added", "eventTime": now, "payload": {"reviewId": "rev-301", "rating": 5, "companionId": "cmp-001"}},
    ]
