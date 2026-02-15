import os
from pathlib import Path

from dotenv import load_dotenv

from smolagents import CodeAgent, InferenceClientModel, Tool


class CalcTool(Tool):
    name = "calc"
    description = """
    simple calculator tool that doubles the input number.
    """
    inputs = {
        "number": {
            "type": "integer",
            "description": "the number to be doubled",
        }
    }
    output_type = "integer"

    def forward(self, number: int) -> int:
        return number * 2


load_dotenv(Path(__file__).resolve().parents[2] / ".env")

# デフォルトで Qwen/Qwen3-Next-80B-A3B-Thinking が使用されますが、必要に応じてモデルを指定できます。
# 環境変数 HF_TOKEN から Hugging Face API トークンを取得して、InferenceClientModel に渡すことができます。
model = InferenceClientModel(token=os.environ["HUGGINGFACE_API_KEY"])
agent = CodeAgent(tools=[CalcTool()], model=model, stream_outputs=True)

agent.run("calculate 5 * 2 using the calc tool.")
