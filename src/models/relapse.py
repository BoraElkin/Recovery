from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from ..database import Base
from pydantic import BaseModel
from typing import Optional
from datetime import date

class RelapseDB(Base):
    __tablename__ = "relapses"

    relapse_id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.goal_id"))
    initial_quit_date = Column(Date)
    last_relapse_date = Column(Date)
    total_sober_days = Column(Integer)
    longest_streak = Column(Integer)
    notes = Column(String, nullable=True)

    goal = relationship("GoalDB", back_populates="relapses")

class Relapse(BaseModel):
    relapse_id: Optional[int]
    goal_id: int
    initial_quit_date: date
    last_relapse_date: date
    total_sober_days: int
    longest_streak: int
    notes: Optional[str] 