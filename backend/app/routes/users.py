from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserResponse, UserUpdate
from ..models import User
from ..auth import get_current_user

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_profile(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user_update.name:
        current_user.name = user_update.name
    if user_update.risk_profile:
        current_user.risk_profile = user_update.risk_profile
    if user_update.kyc_status:
        current_user.kyc_status = user_update.kyc_status
    db.commit()
    db.refresh(current_user)
    return current_user