from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL_NAME")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured")

if not model:
    raise ValueError("GEMINI_MODEL_NAME is not configured")

client = genai.Client(api_key=api_key)

def ask_llm(question: str) -> str :
    response = client.models.generate_content(
        model=model,
        contents=question
    )
    return response.text
