from litellm import embedding, EmbeddingResponse

response: EmbeddingResponse = embedding(model="text-embedding-ada-002", input=["a"])

embedding: list[float] = response.data[0]["embedding"]

print("dimensions:", len(embedding))
print("first 5 values:", embedding[:5])
# dimensions: 1536
# first 5 values: [0.004804602, -0.015059402, 0.0076588206, -0.012782823, -0.029711058]
