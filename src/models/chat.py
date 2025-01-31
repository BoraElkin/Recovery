from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from ..database import Base
from datetime import datetime

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    message_id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("buddy_matches.match_id"))
    sender_id = Column(Integer, ForeignKey("users.user_id"))
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow) 