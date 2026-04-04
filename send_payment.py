import asyncio
import json
from aiokafka import AIOKafkaProducer

async def send_transaction(user_id, amount, category):
    # 1. Connect to the Kafka container
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    
    try:
        # 2. Create the "Event" data
        event = {
            "user_id": user_id,
            "amount": amount,
            "category": category,
            "timestamp": "2026-04-03T14:30:00"
        }
        
        # 3. Send it to the 'transactions' topic
        print(f"--- Sending ${amount} transaction for {user_id} ---")
        await producer.send_and_wait("transactions", json.dumps(event).encode('utf-8'))
        print("Success: Event published to Kafka!")
        
    finally:
        await producer.stop()

if __name__ == "__main__":
    # Let's simulate a $50.00 Coffee purchase
    asyncio.run(send_transaction("USER_001", 10000.0, "Rent"))