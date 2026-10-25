from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Create embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Some sample text
texts = [
    "Machine learning allows computers to learn from data.",
    "Deep learning uses neural networks.",
    "Artificial intelligence is used in many different fields."
]

# Create FAISS vector database
vectorstore = FAISS.from_texts(
    texts,
    embeddings
)

# Save the vector database
vectorstore.save_local("vectorstore")

print("FAISS vector database created successfully!")