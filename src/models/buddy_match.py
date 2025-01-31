from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from ..database import Base
from datetime import datetime

class BuddyMatch(Base):
    __tablename__ = "buddy_matches"

    match_id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.user_id"))
    user2_id = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    chat_enabled = Column(Boolean, default=True)

class BuddyPreferences(Base):
    __tablename__ = "buddy_preferences"

    preference_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    addiction_type = Column(String)
    recovery_stage = Column(String)
    preferred_contact_frequency = Column(String)
    timezone = Column(String) 