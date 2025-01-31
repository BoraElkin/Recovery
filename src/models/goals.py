from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from ..database import Base
from pydantic import BaseModel
from typing import Optional
from datetime import date
import enum

class GoalStatus(enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class GoalType(enum.Enum):
    CONSUMPTION_REDUCTION = "consumption_reduction"
    MONEY_SAVING = "money_saving"
    STREAK = "streak"
    LIFESTYLE = "lifestyle"

class WithdrawalSymptom(enum.Enum):
    ANXIETY = "anxiety"
    DEPRESSION = "depression"
    INSOMNIA = "insomnia"
    IRRITABILITY = "irritability"
    CRAVINGS = "cravings"
    FATIGUE = "fatigue"
    HEADACHE = "headache"
    NAUSEA = "nausea"

class GoalDB(Base):
    __tablename__ = "goals"

    goal_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    description = Column(String)
    goal_type = Column(String)
    target_value = Column(Float)
    current_value = Column(Float)
    start_date = Column(Date)
    target_date = Column(Date)
    status = Column(String, default=GoalStatus.NOT_STARTED.value)

    user = relationship("UserDB", back_populates="goals")
    withdrawal_timeline = relationship("WithdrawalTimelineDB", back_populates="goal")
    relapses = relationship("RelapseDB", back_populates="goal")

class Goal(BaseModel):
    goal_id: Optional[int]
    user_id: int
    description: str
    goal_type: GoalType
    target_value: float
    current_value: Optional[float] = 0.0
    start_date: date
    target_date: date
    status: GoalStatus = GoalStatus.NOT_STARTED

    def update_progress(self, new_value: float) -> None:
        self.current_value = new_value
        if self.current_value >= self.target_value:
            self.status = GoalStatus.COMPLETED
        elif self.current_value > 0:
            self.status = GoalStatus.IN_PROGRESS

    def check_deadline(self) -> bool:
        if date.today() > self.target_date and self.status != GoalStatus.COMPLETED:
            self.status = GoalStatus.FAILED
            return False
        return True

    class Config:
        use_enum_values = True 