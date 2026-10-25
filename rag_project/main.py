from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

import os
from dotenv import load_dotenv
from google import genai

import ollama

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = SentenceTransformer("all-MiniLM-L6-v2")

dimension = 384

index = faiss.IndexFlatL2(dimension)

stored_chunks = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Load FAISS database
vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "RAG Document Question Answering API is running"
    }


# Ask endpoint
@app.post("/ask")
def ask_question(question: str):

    # 1. Search FAISS
    results = vectorstore.similarity_search(
        question,
        k=3
    )

    # 2. Get relevant text
    context = "\n\n".join(
        result.page_content
        for result in results
    )

    # 3. Create prompt
    prompt = f"""
    Answer the question using only the information
    provided in the context below.

    If the answer is not present in the context,
    say:
    "I could not find the answer in the document."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    # 4. Send to Ollama
    response = ollama.chat(
        model="llama3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # 5. Return answer
    return {
        "question": question,
        "answer": response.message.content
    }

def split_text(text, chunk_size=500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks

# Upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    # Save the uploaded PDF
    contents = await file.read()

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(contents)

    # Read PDF
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    # Split text into chunks
    chunks = split_text(text)
    stored_chunks.extend(chunks)

    # Create embeddings
    embeddings = model.encode(chunks)

    # Convert to numpy array
    embeddings = np.array(embeddings).astype("float32")

    # Store embeddings in FAISS
    index.add(embeddings)

    return {
    "message": "PDF uploaded successfully",
    "text_length": len(text),
    "number_of_chunks": len(chunks),
    "embedding_shape": embeddings.shape,
    "vectors_stored": index.ntotal
}

from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    question: str = Field(..., max_length=400)


@app.post("/search")
async def search(question: SearchRequest):

    # Convert question into embedding
    question_embedding = model.encode([question.question])

    question_embedding = np.array(question_embedding).astype("float32")

    # Search FAISS
    distances, indices = index.search(question_embedding, 3)

    # Get relevant chunks
    results = []

    for i in indices[0]:
        if i < len(stored_chunks):
            results.append(stored_chunks[i])

    # Combine retrieved chunks
    context = "\n\n".join(results)

    # Create prompt
    prompt = f"""
    You are a helpful document question-answering assistant.

    Answer the user's question using ONLY the information
    provided in the context below.

    Context:
    {context}

    Question:
    {question.question}

    If the answer cannot be found in the context,
    say:
    "I could not find the answer in the uploaded document."
    """

    # Generate answer using Gemini
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    answer = interaction.output_text

    return {
        "question": question.question,
        "answer": answer,
        "sources": results
    }