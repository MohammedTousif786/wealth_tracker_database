from fastapi import APIRouter, Depends
import schemas
from oauth2 import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me", response_model=schemas.UserResponse)
def get_profile(current_user=Depends(get_current_user)):
    return current_user
