from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.tracking import TrackingDB
from ..models.goals import GoalDB
from ..models.relapse import RelapseDB
from typing import List, Dict
from datetime import datetime, timedelta

router = APIRouter()

def calculate_total_savings(tracking_data: List[TrackingDB]) -> float:
    return sum(entry.amount_saved for entry in tracking_data)

def calculate_current_streak(relapses: List[RelapseDB]) -> int:
    if not relapses:
        return 0
    sorted_relapses = sorted(relapses, key=lambda x: x.date, reverse=True)
    return (datetime.now().date() - sorted_relapses[0].date).days

def calculate_goals_progress(goals: List[GoalDB]) -> dict:
    return {goal.id: goal.current_progress for goal in goals}

def generate_consumption_trends(tracking_data: List[TrackingDB]) -> dict:
    trends = {}
    for entry in tracking_data:
        month_key = entry.date.strftime("%Y-%m")
        trends[month_key] = trends.get(month_key, 0) + entry.amount_saved
    return trends

@router.get("/stats/{user_id}")
def get_user_stats(
    user_id: int,
    db: Session = Depends(get_db)
):
    # Get tracking data
    tracking_data = db.query(TrackingDB).filter(
        TrackingDB.user_id == user_id
    ).all()
    
    # Get goals
    goals = db.query(GoalDB).filter(
        GoalDB.user_id == user_id
    ).all()
    
    # Get relapse data
    relapses = db.query(RelapseDB).filter(
        RelapseDB.goal_id.in_([goal.goal_id for goal in goals])
    ).all()
    
    return {
        "tracking_data": tracking_data,
        "goals": goals,
        "relapses": relapses
    }

@router.get("/dashboard/{user_id}")
async def get_dashboard_data(user_id: int, db: Session = Depends(get_db)):
    tracking_data = db.query(TrackingDB).filter(TrackingDB.user_id == user_id).all()
    goals = db.query(GoalDB).filter(GoalDB.user_id == user_id).all()
    relapses = db.query(RelapseDB).filter(RelapseDB.user_id == user_id).all()
    
    return {
        "savings": calculate_total_savings(tracking_data),
        "streak": calculate_current_streak(relapses),
        "goals_progress": calculate_goals_progress(goals),
        "consumption_trends": generate_consumption_trends(tracking_data)
    } 