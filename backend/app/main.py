from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import auth, users, goals, investments, market, simulations, recommendations

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wealth Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(goals.router)
app.include_router(investments.router)
app.include_router(market.router)
app.include_router(simulations.router)
app.include_router(recommendations.router)

@app.get("/")
def root():
    return {"message": "Wealth Tracker API", "version": "1.0.0", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "healthy"}