from litellm import completion, ModelResponse
# import os

# uv runを使う場合は、.envファイルから環境変数が自動的に読み込まれるため、以下の行は不要です。
# os.environ["OPENAI_API_KEY"] = "your-openai-key"

response: ModelResponse = completion(
    model="openai/gpt-4o",
    messages=[
        {
            "content": "1+1",
            "role": "user",
        }
    ],
    stream=True,
)

for i, chunk in enumerate(response):
    # flush=Trueでバッファリングを防止して、リアルタイムに出力
    print((chunk["choices"][0]["delta"]["content"]), end="", flush=True)
