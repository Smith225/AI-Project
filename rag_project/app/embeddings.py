from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

text = "Machine learning allows computers to learn from data."

vector = embeddings.embed_query(text)

print("Embedding length:", len(vector))
print("First 10 values:", vector[:10])