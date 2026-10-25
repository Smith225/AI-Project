import ollama

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# --------------------------------
# Step 1: Load the embedding model
# --------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------
# Step 2: Load FAISS vector database
# --------------------------------

vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)


# --------------------------------
# Step 3: Ask the user a question
# --------------------------------

question = input("Ask a question about the PDF: ")


# --------------------------------
# Step 4: Search FAISS
# --------------------------------

results = vectorstore.similarity_search(
    question,
    k=3
)


# --------------------------------
# Step 5: Combine retrieved chunks
# --------------------------------

context = "\n\n".join(
    result.page_content
    for result in results
)


# --------------------------------
# Step 6: Create prompt for LLM
# --------------------------------

prompt = f"""
Answer the question using only the information provided in the context below.

If the answer is not present in the context, say:
"I could not find the answer in the document."

Context:
{context}

Question:
{question}

Answer:
"""


# --------------------------------
# Step 7: Send prompt to Ollama
# --------------------------------

response = ollama.chat(
    model="llama3:8b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)


# --------------------------------
# Step 8: Display answer
# --------------------------------

print("\nAnswer:")
print(response.message.content)
