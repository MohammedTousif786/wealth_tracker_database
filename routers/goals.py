from fastapi import APIRouter

router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
)


@router.get("/")
def get_goals():
    return {"message": "Goals endpoint working"}
