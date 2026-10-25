from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Create the embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load the FAISS database
vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

# Ask a question
question = "What is machine learning?"

# Search for the most relevant chunks
results = vectorstore.similarity_search(
    question,
    k=3
)

# Display the results
for i, result in enumerate(results):
    print(f"\n--- Result {i + 1} ---")
    print(result.page_content)