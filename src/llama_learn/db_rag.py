import psycopg2
from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.readers.database import DatabaseReader

connection_string = "postgresql://postgres:postgres@localhost:5432/testdb"
db_name = "postgres"
conn = psycopg2.connect(connection_string)
conn.autocommit = True

reader = DatabaseReader(uri=connection_string, dbname=db_name)

query = "SELECT username, email FROM users LIMIT 5;"
documents = reader.load_data(query=query)

index = VectorStoreIndex.from_documents(documents)

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)

query_engine = RetrieverQueryEngine.from_args(retriever)
response = query_engine.query("what emails do you see?")
print(response)
