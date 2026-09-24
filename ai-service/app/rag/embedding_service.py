from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_EMBEDDING_MODEL_NAME")

if not key:
    raise ValueError("Configured GEMINI_API_KEY is not correct")

client = genai.Client(api_key=key)

if not model:
    raise ValueError("Configured GEMINI_EMBEDDING_MODEL_NAME is not correct")


def embedding_content(chunk: str) -> list[float]:
    try :
        result = client.models.embed_content(
            model=model,
            contents=chunk,
            config=genai.types.EmbedContentConfig(output_dimensionality=768)
        )
        embedding = result.embeddings[0].values
        return embedding

    except Exception as ex :
        raise




