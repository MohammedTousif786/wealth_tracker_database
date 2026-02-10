from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime, date
from enum import Enum

class RiskProfileEnum(str, Enum):
    conservative = "conservative"
    moderate = "moderate"
    aggressive = "aggressive"

class KYCStatusEnum(str, Enum):
    unverified = "unverified"
    verified = "verified"

class GoalTypeEnum(str, Enum):
    retirement = "retirement"
    home = "home"
    education = "education"
    custom = "custom"

class GoalStatusEnum(str, Enum):
    active = "active"
    paused = "paused"
    completed = "completed"

class AssetTypeEnum(str, Enum):
    stock = "stock"
    etf = "etf"
    mutual_fund = "mutual_fund"
    bond = "bond"
    cash = "cash"

class TransactionTypeEnum(str, Enum):
    buy = "buy"
    sell = "sell"
    dividend = "dividend"
    contribution = "contribution"
    withdrawal = "withdrawal"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    risk_profile: Optional[RiskProfileEnum] = RiskProfileEnum.moderate

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    risk_profile: Optional[RiskProfileEnum] = None
    kyc_status: Optional[KYCStatusEnum] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    risk_profile: RiskProfileEnum
    kyc_status: KYCStatusEnum
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None

class GoalCreate(BaseModel):
    goal_type: GoalTypeEnum
    target_amount: float = Field(gt=0)
    target_date: date
    monthly_contribution: float = Field(ge=0)

class GoalUpdate(BaseModel):
    target_amount: Optional[float] = Field(None, gt=0)
    target_date: Optional[date] = None
    monthly_contribution: Optional[float] = Field(None, ge=0)
    status: Optional[GoalStatusEnum] = None

class GoalResponse(BaseModel):
    id: int
    user_id: int
    goal_type: GoalTypeEnum
    target_amount: float
    target_date: date
    monthly_contribution: float
    status: GoalStatusEnum
    created_at: datetime
    class Config:
        from_attributes = True

class InvestmentCreate(BaseModel):
    asset_type: AssetTypeEnum
    symbol: str
    units: float = Field(gt=0)
    avg_buy_price: float = Field(gt=0)

class InvestmentUpdate(BaseModel):
    units: Optional[float] = Field(None, gt=0)
    avg_buy_price: Optional[float] = Field(None, gt=0)

class InvestmentResponse(BaseModel):
    id: int
    user_id: int
    asset_type: AssetTypeEnum
    symbol: str
    units: float
    avg_buy_price: float
    cost_basis: float
    current_value: float
    last_price: float
    last_price_at: Optional[datetime]
    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    symbol: str
    type: TransactionTypeEnum
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)
    fees: Optional[float] = Field(0, ge=0)

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    symbol: str
    type: TransactionTypeEnum
    quantity: float
    price: float
    fees: float
    executed_at: datetime
    class Config:
        from_attributes = True

class RecommendationCreate(BaseModel):
    title: str
    recommendation_text: str
    suggested_allocation: Optional[Dict[str, Any]] = None

class RecommendationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    recommendation_text: str
    suggested_allocation: Optional[Dict[str, Any]]
    created_at: datetime
    class Config:
        from_attributes = True

class SimulationCreate(BaseModel):
    goal_id: Optional[int] = None
    scenario_name: str
    assumptions: Dict[str, Any]

class SimulationResponse(BaseModel):
    id: int
    user_id: int
    goal_id: Optional[int]
    scenario_name: str
    assumptions: Dict[str, Any]
    results: Dict[str, Any]
    created_at: datetime
    class Config:
        from_attributes = True