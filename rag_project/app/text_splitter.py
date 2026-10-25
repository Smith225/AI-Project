from pdf_reader import read_pdf
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = read_pdf("documents/sample.pdf")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(text)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk)