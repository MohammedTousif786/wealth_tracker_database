from fastapi import FastAPI
from backend.database import Base, engine

from backend.routers.auth import router as auth_router
from backend.routers.users import router as users_router
from backend.routers.goals import router as goals_router


app = FastAPI(title="Wealth Tracker API")

# create database tables
Base.metadata.create_all(bind=engine)

# include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(goals_router)


@app.get("/")
def root():
    return {"message": "Wealth Tracker API Running"}
