# database/models.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Column, BigInteger
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String)
    registered_at = Column(DateTime, default=datetime.utcnow)
    
    # Add the subscription fields to the model
    trial_end = Column(DateTime, nullable=True)
    is_subscribed = Column(Boolean, default=False) 
    subscription_end = Column(DateTime, nullable=True)
    
    # Add referral system fields
    referrer_id = Column(BigInteger, nullable=True)
    referral_count = Column(Integer, default=0)
    activated_referrals = Column(Integer, default=0)
    referral_rewards_earned = Column(Integer, default=0)
    referral_rewards_used = Column(Integer, default=0)
    is_activated_referral = Column(Boolean, default=False)

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
