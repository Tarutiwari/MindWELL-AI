import json
from database import get_chats_by_user_and_duration
from pinecone_service import embed_and_store
chats= get_chats_by_user_and_duration(user_id ,"3_days")
chat_json = json.dumps(chats)

def process_chat_data(user_id,message, stres_level):
    metadata={
        "user_id": user_id,
        "stress_level": stres_level,
        "source":"chatbot"
    }

def rule_based_stress(message: str) -> str:
    message = message.lower()
    if "tired" in message or "anxious" in message:
        return "High"
    elif "okay" in message or "fine" in message:
        return "Medium"
    else:
        return "Low"

def summarize_stress(chats: list) -> dict:
    summary = {"Low": 0, "Medium": 0, "High": 0}
    for chat in chats:
        level = chat.get("stress_level", "Unknown")
        if level in summary:
            summary[level] += 1
    return summary

