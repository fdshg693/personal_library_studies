"""
Anthropicプロバイダーである必要があるため、Anthropic APIキーを設定してください。
Anthropicのドキュメント: https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool
"""

from litellm import completion

# Web fetch tool
tools = [
    {
        "type": "web_fetch_20250910",
        "name": "web_fetch",
        "max_uses": 5,
    }
]

messages = [
    {
        "role": "user",
        "content": "Please analyze the content at  https://news.ycombinator.com and summarize the main points in a few sentences.",
    }
]

response = completion(
    model="anthropic/claude-3-5-haiku-latest",
    messages=messages,
    tools=tools,
)

print(response.choices[0].message.content)
