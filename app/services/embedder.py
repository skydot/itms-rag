import requests
from fastapi import HTTPException

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "nomic-embed-text"


def get_embedding(text: str):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": text
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()["embedding"]
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Ollama embedding service is not running")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")
