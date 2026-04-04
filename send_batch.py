import asyncio
import json
from aiokafka import AIOKafkaProducer
from datetime import datetime

async def send_batch_transactions():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    
    # Define a list of different transactions to test your logic
    transactions = [
        {"user_id": "USER_001", "amount": 500.0, "category": "Starbucks"},
        {"user_id": "USER_001", "amount": 121.0, "category": "Groceries"},
        {"user_id": "USER_001", "amount": 10.0, "category": "Rent"}, # Should be REJECTED
        {"user_id": "USER_001", "amount": 25.0, "category": "Gas"},
        {"user_id": "USER_001", "amount": 8020.0, "category": "Luxury Watch"} # Should be REJECTED
    ]

    try:
        print(f"🚀 Sending {len(transactions)} transactions to Kafka...")
        
        for tx in transactions:
            # Add a timestamp to each
            tx['timestamp'] = datetime.now().isoformat()
            
            # Send to the 'transactions' topic
            await producer.send_and_wait("transactions", json.dumps(tx).encode('utf-8'))
            print(f"  📤 Sent: {tx['category']} for ${tx['amount']}")
            
    finally:
        await producer.stop()
        print("✅ Batch sending complete.")

if __name__ == "__main__":
    asyncio.run(send_batch_transactions())