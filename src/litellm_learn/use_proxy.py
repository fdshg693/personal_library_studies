# 事前にlitellm --config path/to/config.yaml --detailed_debugでプロキシサーバーを起動しておくこと

import openai  # openai v1.0.0+

client = openai.OpenAI(api_key="anything", base_url="http://localhost:4000")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "1+1"}],
)

print(response.choices[0].message.content)
