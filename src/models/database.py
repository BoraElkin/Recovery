from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String, DateTime, Boolean, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from ..database import Base

# User model
class UserDB(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    goals = relationship("GoalDB", back_populates="user")
    tracking_data = relationship("TrackingDB", back_populates="user")

# Import all models to ensure they're registered with Base
from .goals import GoalDB
from .tracking import TrackingDB
from .relapse import RelapseDB
from .buddy_match import BuddyMatch, BuddyPreferences
from .chat import ChatMessage 