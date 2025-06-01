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
    trial_end: Mapped[str] = mapped_column(nullable=True)
    is_subscribed: Mapped[bool] = mapped_column(default=False)

    # ➕ Для реферальной системы:
    referral_count: Mapped[int] = mapped_column(default=0)
    activated_referrals: Mapped[int] = mapped_column(default=0)
    referrer_id: Mapped[int] = mapped_column(nullable=True)

    subscriptions = relationship("Subscription", back_populates="user")


class Keyword(Base):
    __tablename__ = "keywords"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # добавили ID как PK

    telegram_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"), nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    word: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)



class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]

    user = relationship("User", back_populates="subscriptions")
