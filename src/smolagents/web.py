import os
from pathlib import Path

from dotenv import load_dotenv

from smolagents import CodeAgent, InferenceClientModel, WebSearchTool

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

# デフォルトで Qwen/Qwen3-Next-80B-A3B-Thinking が使用されますが、必要に応じてモデルを指定できます。
# 環境変数 HF_TOKEN から Hugging Face API トークンを取得して、InferenceClientModel に渡すことができます。
model = InferenceClientModel(token=os.environ["HUGGINGFACE_API_KEY"])
agent = CodeAgent(tools=[WebSearchTool()], model=model, stream_outputs=True)

agent.run("日本の2026年2月の現時点の人口は？")
