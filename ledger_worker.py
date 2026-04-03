import asyncio
import json
from aiokafka import AIOKafkaConsumer
from motor.motor_asyncio import AsyncIOMotorClient

async def consume_transactions():
    # 1. Connect to both Kafka and MongoDB
    consumer = AIOKafkaConsumer(
        "transactions",
        bootstrap_servers='localhost:9092',
        group_id="ledger-group" # This ensures we don't process the same payment twice
    )
    
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["nexus_db"]
    collection = db["profiles"]

    await consumer.start()
    print("--- Ledger Worker Started: Watching for Payments... ---")

    try:
        async for msg in consumer:
            # 2. Parse the Kafka message
            data = json.loads(msg.value.decode('utf-8'))
            user_id = data['user_id']
            amount = data['amount']
            
            print(f"Processing payment: {user_id} spent ${amount}")

            # 3. Update MongoDB (Decrease balance, Increase total_spent)
            await collection.update_one(
                {"user_id": user_id},
                {
                    "$inc": {
                        "wallet.balance": -amount,  # Subtract from balance
                        "analytics.total_spent": amount # Add to total spent
                    }
                }
            )
            print(f"Success: Updated Ledger for {user_id}")

    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_transactions())