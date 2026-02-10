from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import InvestmentCreate, InvestmentResponse
from ..models import User, Investment
from ..auth import get_current_user

router = APIRouter(prefix="/api/investments", tags=["Investments"])

@router.post("/", response_model=InvestmentResponse, status_code=201)
async def create_investment(inv: InvestmentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cost_basis = float(inv.units) * float(inv.avg_buy_price)
    new_inv = Investment(user_id=current_user.id, asset_type=inv.asset_type, symbol=inv.symbol.upper(),
                        units=inv.units, avg_buy_price=inv.avg_buy_price, cost_basis=cost_basis,
                        current_value=cost_basis, last_price=inv.avg_buy_price)
    db.add(new_inv)
    db.commit()
    db.refresh(new_inv)
    return new_inv

@router.get("/", response_model=List[InvestmentResponse])
async def get_investments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Investment).filter(Investment.user_id == current_user.id).all()

@router.get("/portfolio/summary")
async def portfolio_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    investments = db.query(Investment).filter(Investment.user_id == current_user.id).all()
    total_value = sum(float(i.current_value) for i in investments)
    total_cost = sum(float(i.cost_basis) for i in investments)
    allocation = {}
    for inv in investments:
        allocation[inv.asset_type.value] = allocation.get(inv.asset_type.value, 0) + float(inv.current_value)
    
    return {
        "total_value": round(total_value, 2),
        "total_cost": round(total_cost, 2),
        "total_gain_loss": round(total_value - total_cost, 2),
        "total_gain_loss_pct": round((total_value - total_cost) / total_cost * 100, 2) if total_cost > 0 else 0,
        "allocation": allocation,
        "num_positions": len(investments)
    }

@router.delete("/{id}", status_code=204)
async def delete_investment(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    inv = db.query(Investment).filter(Investment.id == id, Investment.user_id == current_user.id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investment not found")
    db.delete(inv)
    db.commit()