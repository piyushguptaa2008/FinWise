
import os

from dotenv import load_dotenv

load_dotenv()


def get_model():

    provider = os.getenv(
        "AI_PROVIDER", "ollama"
    ).lower()

    if provider == "ollama":

        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=os.getenv(
                "OLLAMA_MODEL", "qwen2.5:7b"
            ),
            base_url="http://localhost:11434",
            temperature=0
        )

    if provider == "llama_cpp":

        from cloud_model import CloudChatModel

        return CloudChatModel()

    raise ValueError(
        f"Unsupported AI provider: {provider}"
    )
