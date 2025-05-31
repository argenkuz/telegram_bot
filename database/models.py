# database/models.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(nullable=True)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    trial_end: Mapped[datetime]
    is_subscribed: Mapped[bool] = mapped_column(default=False)


    subscriptions = relationship("Subscription", back_populates="user")


class Keyword(Base):
    __tablename__ = "keywords"

    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str]
    category: Mapped[str]

class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]

    user = relationship("User", back_populates="subscriptions")
