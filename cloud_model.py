
import json
import os

from pathlib import Path
from functools import lru_cache
from threading import RLock

from llama_cpp import Llama
from huggingface_hub import hf_hub_download

from langchain_core.language_models.chat_models import (
    BaseChatModel
)

from langchain_core.messages import (
    AIMessage,
    ToolMessage
)

from langchain_core.outputs import (
    ChatGeneration,
    ChatResult
)

from langchain_core.utils.function_calling import (
    convert_to_openai_tool
)


MODEL_LOCK = RLock()

MODEL_REPO = "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
MODEL_FILENAME = "qwen2.5-1.5b-instruct-q4_k_m.gguf"


def get_model_path():

    # Option 1: Custom model path
    configured_path = os.getenv("GGUF_MODEL_PATH")

    if configured_path:

        path = Path(configured_path).expanduser()

        if not path.is_file():
            raise FileNotFoundError(
                f"Configured model not found: {path}"
            )

        return str(path)

    # Option 2: Existing local Ollama model
    root = Path.home() / ".ollama" / "models"

    manifest_path = (
        root / "manifests" / "registry.ollama.ai"
        / "library" / "qwen2.5" / "1.5b"
    )

    if manifest_path.exists():

        manifest = json.loads(
            manifest_path.read_text()
        )

        for layer in manifest["layers"]:

            if layer["mediaType"] == \
                    "application/vnd.ollama.image.model":

                model_path = (
                    root / "blobs" /
                    layer["digest"].replace(":", "-")
                )

                if model_path.is_file():

                    print("Using existing local model")

                    return str(model_path)

    # Option 3: Automatic cloud model download
    print("Downloading Qwen GGUF model...")

    model_path = hf_hub_download(
        repo_id=MODEL_REPO,
        filename=MODEL_FILENAME
    )

    print("Cloud model ready")

    return model_path


@lru_cache(maxsize=1)
def load_model():

    return Llama(
        model_path=get_model_path(),
        n_ctx=4096,
        n_threads=2,
        n_gpu_layers=0,
        chat_format="chatml-function-calling",
        verbose=False
    )


class CloudChatModel(BaseChatModel):

    @property
    def _llm_type(self):
        return "finwise-llama-cpp"

    def bind_tools(self, tools, **kwargs):

        formatted_tools = [
            convert_to_openai_tool(tool)
            for tool in tools
        ]

        return self.bind(
            tools=formatted_tools,
            **kwargs
        )

    def _generate(
        self,
        messages,
        stop=None,
        run_manager=None,
        **kwargs
    ):

        formatted_messages = []

        for message in messages:

            if isinstance(message, ToolMessage):

                formatted_messages.append({
                    "role": "tool",
                    "content": str(message.content),
                    "tool_call_id": message.tool_call_id
                })

            elif isinstance(message, AIMessage):

                item = {
                    "role": "assistant",
                    "content": message.content or ""
                }

                if message.tool_calls:

                    item["tool_calls"] = [
                        {
                            "id": call["id"],
                            "type": "function",
                            "function": {
                                "name": call["name"],
                                "arguments": json.dumps(
                                    call["args"]
                                )
                            }
                        }
                        for call in message.tool_calls
                    ]

                formatted_messages.append(item)

            else:

                role = {
                    "human": "user",
                    "system": "system"
                }.get(message.type, "user")

                formatted_messages.append({
                    "role": role,
                    "content": str(message.content)
                })

        options = {
            "messages": formatted_messages,
            "temperature": 0,
            "max_tokens": 512
        }

        if kwargs.get("tools"):

            options["tools"] = kwargs["tools"]
            options["tool_choice"] = "auto"

        if stop:
            options["stop"] = stop

        with MODEL_LOCK:

            response = load_model().create_chat_completion(
                **options
            )

        output = response["choices"][0]["message"]

        tool_calls = []

        for call in output.get("tool_calls") or []:

            tool_calls.append({
                "name": call["function"]["name"],
                "args": json.loads(
                    call["function"]["arguments"]
                ),
                "id": call["id"],
                "type": "tool_call"
            })

        message = AIMessage(
            content=output.get("content") or "",
            tool_calls=tool_calls
        )

        return ChatResult(
            generations=[
                ChatGeneration(message=message)
            ]
        )
