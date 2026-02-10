from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Recommendation
from ..auth import get_current_user
from ..simulation_service import simulation_service

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("/generate")
async def generate_recommendation(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    allocation = simulation_service.generate_allocation_recommendation(current_user.risk_profile.value, 35)
    
    text = f"""Based on {current_user.risk_profile.value} risk profile:
{allocation['description']}

Recommended:
- Stocks: {allocation['stocks']}%
- Bonds: {allocation['bonds']}%
- Cash: {allocation['cash']}%
"""
    
    rec = Recommendation(user_id=current_user.id, title=f"Allocation - {current_user.risk_profile.value.title()}",
                        recommendation_text=text, suggested_allocation=allocation)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec