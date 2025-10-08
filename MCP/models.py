from sqlalchemy.orm import declarative_base ,relationship
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
import uuid

Base = declarative_base()

class user(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    create_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    Extra_metadata = Column(JSON, nullable=True)
    expenses = relationship("expense", back_populates="user")

class expense(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String,ForeignKey('users.id'), index=True)
    amount = Column(Integer, nullable=False)
    category = Column(String, nullable=True)
    subcategory = Column(String, nullable=True)
    description = Column(String, nullable=True)
    date = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    create_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    Extra_metadata = Column(JSON, nullable=True)
    user = relationship("user", back_populates="expenses")
