from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine, select
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from backend.app.core.config import settings

Base = declarative_base()
engine = create_engine(settings.databaseUrl, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class UserRecord(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    city = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CompanionRecord(Base):
    __tablename__ = "companions"
    companion_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    categories = Column(String, nullable=False)
    interests = Column(String, nullable=False)
    price_per_hour = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    photo_url = Column(String, nullable=True)


class BookingRecord(Base):
    __tablename__ = "bookings"
    booking_id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    companion_id = Column(String, nullable=False)
    category = Column(String, nullable=False)
    booking_date = Column(DateTime(timezone=True), nullable=False)
    duration_hours = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


SEED_COMPANIONS = [
    {"companion_id": "cmp-001", "user_id": "usr-101", "name": "Анна", "city": "Москва", "age": 27, "categories": "прогулки|музеи", "interests": "искусство|кофе", "price_per_hour": 1200, "rating": 4.9, "photo_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330"},
    {"companion_id": "cmp-002", "user_id": "usr-102", "name": "Илья", "city": "Санкт-Петербург", "age": 31, "categories": "спорт|хобби", "interests": "бег|настолки", "price_per_hour": 950, "rating": 4.7, "photo_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e"},
    {"companion_id": "cmp-003", "user_id": "usr-103", "name": "Мария", "city": "Казань", "age": 25, "categories": "мероприятия|общение", "interests": "театр|языки", "price_per_hour": 1100, "rating": 4.8, "photo_url": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80"},
]


def initDb() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        if not session.execute(select(CompanionRecord)).first():
            session.add_all([CompanionRecord(**item) for item in SEED_COMPANIONS])
        if not session.get(UserRecord, "usr-201"):
            session.add(UserRecord(user_id="usr-201", email="customer@example.com", role="customer", city="Москва"))
        session.commit()


def getSession():
    with SessionLocal() as session:
        yield session
