import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from ledger_worker.models import UserProfile, Wallet, UserAnalytics

async def init_database():
    # 1. Connect to MongoDB (Standard port from our Docker setup)
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["nexus_db"]
    collection = db["profiles"]

    # 2. Create a dummy user profile
    # Note: In a real app, this would happen during 'Sign Up'
    new_user = UserProfile(
        user_id="USER_001",
        name="Sebastian Michael",
        email="sebastian.michael94@gmail.com",
        wallet=Wallet(balance=5000.0), # Starting with $5000
        analytics=UserAnalytics()
    )

    # 3. Insert into MongoDB
    # We use 'model_dump' to convert the Pydantic object to a Dictionary for Mongo
    result = await collection.update_one(
        {"user_id": new_user.user_id}, 
        {"$set": new_user.model_dump()}, 
        upsert=True
    )
    
    print(f"User Initialized! ID: {new_user.user_id}")
    client.close()

if __name__ == "__main__":
    asyncio.run(init_database())