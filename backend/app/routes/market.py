from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import User, Investment
from ..auth import get_current_user
from ..market_service import market_service

router = APIRouter(prefix="/api/market", tags=["Market"])

@router.get("/price/{symbol}")
async def get_price(symbol: str, current_user: User = Depends(get_current_user)):
    price_data = market_service.get_current_price(symbol.upper())
    if not price_data:
        return {"error": f"Could not fetch price for {symbol}"}
    return price_data

@router.post("/refresh-prices")
async def refresh_prices(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    investments = db.query(Investment).filter(Investment.user_id == current_user.id).all()
    if not investments:
        return {"message": "No investments", "updated": 0}
    
    symbols = list(set([inv.symbol for inv in investments]))
    prices = market_service.get_multiple_prices(symbols)
    updated = 0
    
    for inv in investments:
        price_data = prices.get(inv.symbol)
        if price_data and price_data.get('price'):
            inv.last_price = price_data['price']
            inv.current_value = float(inv.units) * float(price_data['price'])
            inv.last_price_at = datetime.utcnow()
            updated += 1
    
    db.commit()
    return {"message": f"Updated {updated} investments", "updated": updated, "total": len(investments)}