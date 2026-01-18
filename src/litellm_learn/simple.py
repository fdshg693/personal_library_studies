from litellm import completion
import os

# uv runを使う場合は、.envファイルから環境変数が自動的に読み込まれるため、以下の行は不要です。
# os.environ["OPENAI_API_KEY"] = "your-openai-key"

# OpenAI
response = completion(
    model="openai/gpt-4o", messages=[{"role": "user", "content": "1+1"}]
)

print(response.choices[0].message.content)
