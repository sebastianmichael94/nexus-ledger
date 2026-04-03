from django.http import JsonResponse
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def get_user_profile(request, user_id):
    # 1. Create the client inside the view to avoid "Closed Loop" errors
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["nexus_db"]
    collection = db["profiles"]
    
    try:
        # 2. Fetch the data
        user_data = await collection.find_one({"user_id": user_id})
        
        if user_data:
            user_data.pop('_id', None) # Clean up for JSON
            return JsonResponse(user_data, safe=False)
        
        return JsonResponse({"error": "User not found"}, status=404)
    
    finally:
        # 3. Always close the connection
        client.close()