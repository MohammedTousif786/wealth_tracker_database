from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import SimulationCreate, SimulationResponse
from ..models import User, Simulation, Goal, Investment
from ..auth import get_current_user
from ..simulation_service import simulation_service

router = APIRouter(prefix="/api/simulations", tags=["Simulations"])

@router.post("/", response_model=SimulationResponse, status_code=201)
async def create_simulation(sim: SimulationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    results = simulation_service.run_what_if_scenario({}, sim.assumptions)
    new_sim = Simulation(user_id=current_user.id, goal_id=sim.goal_id, scenario_name=sim.scenario_name,
                        assumptions=sim.assumptions, results=results)
    db.add(new_sim)
    db.commit()
    db.refresh(new_sim)
    return new_sim

@router.get("/", response_model=List[SimulationResponse])
async def get_simulations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Simulation).filter(Simulation.user_id == current_user.id).order_by(Simulation.created_at.desc()).all()

@router.post("/goal/{goal_id}/project")
async def project_goal(goal_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    investments = db.query(Investment).filter(Investment.user_id == current_user.id).all()
    current_savings = sum(float(inv.current_value) for inv in investments)
    
    projection = simulation_service.calculate_goal_projection(
        target_amount=float(goal.target_amount),
        monthly_contribution=float(goal.monthly_contribution),
        target_date=goal.target_date,
        current_savings=current_savings
    )
    return projection