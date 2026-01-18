from litellm import completion

response = completion(
    model="openai/gpt-4o-search-preview",
    messages=[
        {
            "role": "user",
            "content": "今日の東京の天気は？",
        }
    ],
    web_search_options={
        "search_context_size": "low"  # Options: "low", "medium", "high"
    },
)

print(response.choices[0].message.content)
