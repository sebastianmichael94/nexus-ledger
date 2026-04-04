import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

async def initialize_database():
    # 1. Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["nexus_db"]
    collection = db["profiles"]

    # 2. Define the Fresh User Data
    default_user = {
        "user_id": "USER_001",
        "name": "Sebastian Michael",
        "email": "sebastian.michael94@gmail.com",
        "kyc_status": "Verified",
        "wallet": {
            "balance": 5000.0,
            "currency": "USD",
            "last_updated": datetime.now()
        },
        "analytics": {
            "total_spent": 0.0,
            "favorite_category": "None"
        },
        "recent_transactions": []
    }

    # 3. Wipe and Re-insert
    print("🧹 Cleaning up old data...")
    await collection.delete_many({"user_id": "USER_001"})
    
    print("🏦 Inserting fresh ledger for USER_001...")
    await collection.insert_one(default_user)
    
    print("✅ Success: Database Reset to $5000.00")
    client.close()

if __name__ == "__main__":
    asyncio.run(initialize_database())