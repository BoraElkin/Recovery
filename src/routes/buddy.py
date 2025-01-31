from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.buddy_matcher import BuddyMatcher
from ..models.buddy_match import BuddyMatch, BuddyPreferences
from ..models.chat import ChatMessage
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class BuddyPreferenceCreate(BaseModel):
    addiction_type: str
    recovery_stage: str
    preferred_contact_frequency: str
    timezone: str

@router.post("/preferences/")
def set_preferences(
    preferences: BuddyPreferenceCreate,
    db: Session = Depends(get_db)
):
    # Implementation
    pass

@router.get("/match/{user_id}")
def find_buddy(
    user_id: int,
    db: Session = Depends(get_db)
):
    matcher = BuddyMatcher(db)
    matches = matcher.find_match(user_id)
    if not matches:
        raise HTTPException(status_code=404, detail="No matches found")
    return matches

@router.post("/buddy/chat/{match_id}")
async def send_message(
    match_id: int,
    content: str,
    sender_id: int,
    db: Session = Depends(get_db)
):
    message = ChatMessage(
        match_id=match_id,
        sender_id=sender_id,
        content=content
    )
    db.add(message)
    db.commit()
    return message

@router.get("/buddy/chat/{match_id}")
async def get_chat_history(
    match_id: int,
    db: Session = Depends(get_db)
):
    messages = db.query(ChatMessage).filter(
        ChatMessage.match_id == match_id
    ).order_by(ChatMessage.timestamp.desc()).all()
    return messages 