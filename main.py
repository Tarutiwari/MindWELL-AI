
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from gemini_service import get_gemini_response
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # 0 = all logs, 1 = info, 2 = warnings, 3 = errors

 
from redis_service import store_temp_chat, get_temp_chat
from analysis_services import summarize_stress
from pinecone_service import store_vector
from database import save_chat_to_postgres, get_chats_by_user_and_duration
from database import transfer_redis_to_postgres
import uuid
from datetime import datetime



app = FastAPI()

# ✅ CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat/")
async def chat_with_user(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    message = data.get("message")
    if not message:
        return{"error":"Message is required"}

    # 1. Get Gemini response
    response = await get_gemini_response(message)

    # 2. Embed message for vector DB
    vector = await embed_message(message)

    # 3. Create chat object
    chat_data = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "message": message,
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    }

    # 4. Store in Redis or PostgreSQL
    if not user_id:
        store_temp_chat(chat_data)
    else:
         save_chat_to_postgres(user_id, chat_data)

    # 5. Store in Pinecone
    store_vector(chat_data["id"], vector, metadata=chat_data)

    return {
        "response": response,
        "status": "stored"
    }

@app.get("/report/")
def get_stress_report(user_id: str, duration: str = Query("3_days")):
    chats = get_chats_by_user_and_duration(user_id, duration)
    summary = summarize_stress(chats)
    return {
        "user_id": user_id,
        "duration": duration,
        "report": summary
    }

@app.get("/guest-chat/")
def get_guest_chat(chat_id: str):
    return get_temp_chat(chat_id)


@app.post("/login/")
def login_user(request:Request):
    data =  request.json()
    user_id = data.get("user_id")

    if not user_id:
        return{"error":"Misssing user_id"}
    
    transfer_redis_to_postgres(user_id)
    return{"message": f"Welcome back, user {user_id}!,your previous chats have been restored"}
