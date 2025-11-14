# gemini_service.py
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")


async def get_gemini_response(message: str) -> str:
    response = model.generate_content(message)
    return response.text

async def classify_stress(message: str) -> str:
    prompt = f"Classify the stress level of this message: '{message}'. Reply with Low, Medium, or High."
    result = model.generate_content(prompt)
    return result.text.strip()

