from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import GoalCreate, GoalUpdate, GoalResponse
from ..models import User, Goal
from ..auth import get_current_user

router = APIRouter(prefix="/api/goals", tags=["Goals"])

@router.post("/", response_model=GoalResponse, status_code=201)
async def create_goal(goal: GoalCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_goal = Goal(user_id=current_user.id, goal_type=goal.goal_type, target_amount=goal.target_amount, 
                    target_date=goal.target_date, monthly_contribution=goal.monthly_contribution)
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal

@router.get("/", response_model=List[GoalResponse])
async def get_goals(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Goal).filter(Goal.user_id == current_user.id).all()

@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(goal_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal(goal_id: int, goal_update: GoalUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    if goal_update.target_amount:
        goal.target_amount = goal_update.target_amount
    if goal_update.target_date:
        goal.target_date = goal_update.target_date
    if goal_update.monthly_contribution:
        goal.monthly_contribution = goal_update.monthly_contribution
    if goal_update.status:
        goal.status = goal_update.status
    
    db.commit()
    db.refresh(goal)
    return goal

@router.delete("/{goal_id}", status_code=204)
async def delete_goal(goal_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal)
    db.commit()