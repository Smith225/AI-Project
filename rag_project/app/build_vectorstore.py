from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# --------------------------------
# Step 1: Read the PDF
# --------------------------------

pdf_path = "documents/sample.pdf"

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    text += page.extract_text()

print("PDF text extracted successfully.")


# --------------------------------
# Step 2: Split the text
# --------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(text)

print("Number of chunks:", len(chunks))


# --------------------------------
# Step 3: Create embeddings
# --------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded.")


# --------------------------------
# Step 4: Create FAISS database
# --------------------------------

vectorstore = FAISS.from_texts(
    chunks,
    embeddings
)

print("FAISS database created.")


# --------------------------------
# Step 5: Save FAISS database
# --------------------------------

vectorstore.save_local("vectorstore")

print("Vector database saved successfully.")