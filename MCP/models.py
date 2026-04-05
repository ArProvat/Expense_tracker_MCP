from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
import uuid

Base = declarative_base()

class User(Base): # Class names are usually Capitalized in Python (PEP8)
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    # Fix: Added lambda to ensure it generates a new time on every insert
    create_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    Extra_metadata = Column(JSON, nullable=True)
    expenses = relationship("Expense", back_populates="user")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'), index=True)
    amount = Column(Integer, nullable=False)
    category = Column(String, nullable=True)
    subcategory = Column(String, nullable=True)
    description = Column(String, nullable=True)
    # Fix: Added lambdas here as well
    date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    create_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    Extra_metadata = Column(JSON, nullable=True)
    user = relationship("User", back_populates="expenses")