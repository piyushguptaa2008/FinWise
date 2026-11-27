import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()


def get_model():
    provider = os.getenv("AI_PROVIDER", "ollama").lower()

    if provider == "ollama":
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
            base_url="http://localhost:11434",
            temperature=0
        )

    raise ValueError(f"Unsupported AI provider: {provider}")