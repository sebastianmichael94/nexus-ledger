from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class TransactionHistory(BaseModel):
    transaction_id: str
    amount: float
    timestamp: datetime
    category: str 

class Wallet(BaseModel):
    balance: float = 0.0
    currency: str = "USD"
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class UserAnalytics(BaseModel):
    total_spent: float = 0.0
    favorite_category: str = "None"

class UserProfile(BaseModel):
    user_id: str  
    name: str
    email: str
    kyc_status: str = "Verified"
    wallet: Wallet
    analytics: UserAnalytics
    recent_transactions: List[TransactionHistory] = []