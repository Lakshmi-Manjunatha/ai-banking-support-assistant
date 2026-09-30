import inspect
import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key :
    raise ValueError("Configured GEMINI_API_KEY is not correct")

api_model = os.getenv("GEMINI_EMBEDDING_MODEL_NAME")

if not api_model :
    raise ValueError("Configured GEMINI_EMBEDDING_MODEL_NAME is not correct")

embedding_dimension = os.getenv("EMBEDDING_DIMENSION")

if not embedding_dimension:
    raise ValueError("EMBEDDING_DIMENSION is not configured")


embeddings = GoogleGenerativeAIEmbeddings(model=api_model,
                                          google_api_key = api_key,
                                          output_dimensionality=int(embedding_dimension))





