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
            category = data.get('category', 'General')
            
            print(f"Processing payment: {user_id} spent ${amount} on {category}")

            # --- NEW: BALANCE CHECK ---
            user_doc = await collection.find_one({"user_id": user_id})
            
            if not user_doc:
                print(f"User {user_id} not found!")
                continue

            current_balance = user_doc['wallet']['balance']

            if current_balance < amount:
                print(f"REJECTED: {user_id} has ${current_balance}, but tried to spend ${amount}")
                #Push a "FAILED" transaction to history
                await collection.update_one(
                    {"user_id": user_id},
                    {"$push": {"recent_transactions": {"$each": [{"amount": amount, "category": category, "status": "FAILED"}], "$slice": -10}}}
                )
                continue
            # --- END OF CHECK ---

            # 3. Update MongoDB (Decrease balance, Increase total_spent)
            transaction_record = {
                "amount": amount,
                "category": category,
                "timestamp": data.get('timestamp'),
                "status": "SUCCESS"
            }

            await collection.update_one(
                {"user_id": user_id},
                {
                    "$inc": {
                        "wallet.balance": -amount,
                        "analytics.total_spent": amount
                    },
                    "$push": {
                        "recent_transactions": {
                            "$each": [transaction_record],
                            "$slice": -10  # Keeps only the last 10 transactions
                        }
                    }
                }
            )
            print(f"Success: Updated Ledger for {user_id}")

    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_transactions())