from sqlalchemy import Column, Integer, Float, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..database import Base
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import date

class TrackingDB(Base):
    __tablename__ = "tracking_data"

    tracking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    date = Column(Date)
    consumption_amount = Column(Float)
    money_saved = Column(Float)
    associated_habits = Column(JSON)  # Stores related habits data
    mood_score = Column(Integer)  # 1-10 scale
    triggers_encountered = Column(JSON)  # Store triggers faced that day
    coping_strategies_used = Column(JSON)  # Store strategies used

    user = relationship("UserDB", back_populates="tracking_data")

class TrackingData(BaseModel):
    tracking_id: Optional[int]
    user_id: int
    date: date
    consumption_amount: float
    money_saved: float
    associated_habits: Dict[str, float]  # e.g., {"takeout": 25.50, "smoking": 10.00}
    mood_score: Optional[int]
    triggers_encountered: Optional[Dict[str, str]]  # e.g., {"stress": "work deadline"}
    coping_strategies_used: Optional[Dict[str, bool]]  # e.g., {"meditation": true}

    def calculate_total_savings(self) -> float:
        """Calculate total savings including associated habits"""
        associated_costs = sum(self.associated_habits.values())
        return self.money_saved + associated_costs

    def update_mood(self, score: int) -> None:
        """Update mood score (1-10)"""
        if 1 <= score <= 10:
            self.mood_score = score

    def add_trigger(self, trigger_type: str, description: str) -> None:
        """Add a trigger encountered"""
        if self.triggers_encountered is None:
            self.triggers_encountered = {}
        self.triggers_encountered[trigger_type] = description

    def add_coping_strategy(self, strategy: str, successful: bool) -> None:
        """Record a coping strategy used"""
        if self.coping_strategies_used is None:
            self.coping_strategies_used = {}
        self.coping_strategies_used[strategy] = successful

    class Config:
        arbitrary_types_allowed = True 