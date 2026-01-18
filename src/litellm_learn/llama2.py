from litellm import completion, ModelResponse

model = "meta-llama/Llama-3.2-3B-Instruct"
messages = [
    {"role": "user", "content": "1+1"},
]
response: ModelResponse = completion(
    model=model, messages=messages, custom_llm_provider="huggingface"
)
print(response.choices[0].message.content)
