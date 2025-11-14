# redis_service.py
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def store_temp_chat(chat_data: dict):
    key = f"guest_chat:{chat_data['id']}"
    r.setex(key, 60 * 60 * 48, json.dumps(chat_data))  # 48 hours TTL

def get_temp_chat(chat_id: str):
    data = r.get(f"guest_chat:{chat_id}")
    return json.loads(data) if data else None
