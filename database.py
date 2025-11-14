# database.py
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timedelta
from config import DATABASE_URL
import redis
import json

# ✅ PostgreSQL setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# ✅ Redis setup
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# ✅ Chat model
class Chat(Base):
    __tablename__ = "chats"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    message = Column(Text)
    response = Column(Text)
    stress_level = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ✅ Save chat to PostgreSQL
def save_chat_to_postgres(user_id: str, chat_data: dict):
    session = SessionLocal()
    try:
        chat = Chat(
            id=chat_data["id"],
            user_id=user_id,
            message=chat_data["message"],
            response=chat_data["response"],
            stress_level=chat_data.get("stress_level", "Unknown"),
            timestamp=datetime.utcnow()
        )
        session.add(chat)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"❌ Error saving chat: {e}")
    finally:
        session.close()

# ✅ Transfer temporary Redis chats to PostgreSQL
def transfer_redis_to_postgres(user_id: str):
    session = SessionLocal()
    try:
        keys = r.keys("guest_chat:*")
        for key in keys:
            data = r.get(key)
            if data:
                chat_data = json.loads(data)
                chat = Chat(
                    id=chat_data["id"],
                    user_id=user_id,
                    message=chat_data["message"],
                    response=chat_data["response"],
                    stress_level=chat_data.get("stress_level", "Unknown"),
                    timestamp=datetime.utcnow()
                )
                session.add(chat)
                r.delete(key)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"❌ Error transferring from Redis: {e}")
    finally:
        session.close()

# ✅ Fetch chats by user and duration
def get_chats_by_user_and_duration(user_id: str, duration: str = "3_days"):
    session = SessionLocal()
    now = datetime.utcnow()
    start_time = now - timedelta(days=7 if duration == "7_days" else 3)
    try:
        chats = session.query(Chat).filter(
            Chat.user_id == user_id,
            Chat.timestamp >= start_time
        ).all()
        return [
            {
                "message": chat.message,
                "response": chat.response,
                "stress_level": chat.stress_level,
                "timestamp": chat.timestamp.isoformat()
            }
            for chat in chats
        ]
    except Exception as e:
        print(f"❌ Error fetching chats: {e}")
        return []
    finally:
        session.close()
