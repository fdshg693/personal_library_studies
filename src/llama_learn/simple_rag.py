from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

# OPENAI_API_KEYの設定が必要

# CWDを`src\llama_learn`にすること
# そうしないと、dataフォルダが見つからない
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("What is my name?")
print(response)
