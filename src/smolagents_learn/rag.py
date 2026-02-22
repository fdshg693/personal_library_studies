import os
from pathlib import Path

from dotenv import load_dotenv

from smolagents import CodeAgent, InferenceClientModel

# 「"open": open,」を「.venv\Lib\site-packages\smolagents\local_python_executor.py」 の BASE_PYTHON_TOOLS に追加する必要があります。
# また、「./data/number.md」にアクセスするために、このスクリプトを src/smolagents/ ディレクトリで実行する必要があります。
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

model = InferenceClientModel(token=os.environ["HUGGINGFACE_API_KEY"])
agent = CodeAgent(tools=[], model=model, stream_outputs=True)

agent.run("`./data/number.md` に書いてある数字を教えてください。")
