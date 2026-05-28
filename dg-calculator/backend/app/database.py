import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME", "dg_calculator")]
calculations = db["calculations"]

def save_calculation(inputs: dict, result: dict) -> str:
    doc = {
        "inputs": inputs,
        "result": result,
        "created_at": datetime.utcnow()
    }
    inserted = calculations.insert_one(doc)
    return str(inserted.inserted_id)

def get_recent_calculations(limit: int = 10) -> list:
    docs = calculations.find().sort("created_at", -1).limit(limit)
    result = []
    for doc in docs:
        doc["_id"] = str(doc["_id"])
        doc["created_at"] = doc["created_at"].isoformat()
        result.append(doc)
    return result