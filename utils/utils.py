import os
from sentence_transformers import SentenceTransformer
import chromadb
import fitz
from docx import Document

def parse_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# ✅ NEW Chroma Persistent client
client = chromadb.PersistentClient(path="./.chroma")
collection = client.get_or_create_collection("knowledge_base")
model = SentenceTransformer('all-MiniLM-L6-v2')

text_chunks = []
filenames = []

folder_path = f"/home/aniketjadon/rag-test/data"
for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    if file.endswith(".pdf"):
        text = parse_pdf(file_path)
    elif file.endswith(".docx"):
        text = parse_docx(file_path)
    elif file.endswith(".txt"):
        text = parse_txt(file_path)
    else:
        continue
    text_chunks.append(text)
    filenames.append(file)

ids = [f"doc_{i}" for i in range(len(text_chunks))]
embeddings = model.encode(text_chunks).tolist()
metadatas = [{"filename": f} for f in filenames]

collection.add(
    ids=ids,
    documents=text_chunks,
    metadatas=metadatas,
    embeddings=embeddings
)

print("✅ Knowledge base embedded and stored in ChromaDB.")
