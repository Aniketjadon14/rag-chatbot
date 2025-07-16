import os
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from app.utils import parse_pdf, parse_docx, parse_txt
from app.config import OPENAI_API_KEY
import chromadb

client = OpenAI(api_key=OPENAI_API_KEY)
model = SentenceTransformer('all-MiniLM-L6-v2')

class RAGSystem:
    def __init__(self):
        self.text_chunks = []
        self.filenames = []
        self.client = chromadb.PersistentClient(path="./.chroma")
        self.collection = self.client.get_or_create_collection(name="documents")

    def chunk_text(self, text, max_words=100):
        words = text.split()
        chunks = []
        for i in range(0, len(words), max_words):
            chunk = " ".join(words[i:i+max_words])
            if len(chunk.strip()) > 20:
                chunks.append(chunk)
        return chunks

    def ingest_documents(self, folder_path="data"):
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
            # 🔥 Use better chunking
            chunks = self.chunk_text(text, max_words=100)
            for chunk in chunks:
                self.text_chunks.append(chunk)
                self.filenames.append(file)

    def create_embeddings(self):
        ids = [f"doc_{i}" for i in range(len(self.text_chunks))]
        embeddings = model.encode(self.text_chunks).tolist()
        metadatas = [{"filename": f} for f in self.filenames]
        self.collection.add(
            ids=ids,
            documents=self.text_chunks,
            metadatas=metadatas,
            embeddings=embeddings
        )

    def retrieve(self, query, top_k=3):
        query_emb = model.encode([query]).tolist()[0]
        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=top_k
        )
        docs_and_sources = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            docs_and_sources.append((doc, meta["filename"]))
        return docs_and_sources

    def generate_answer(self, query):
        docs = self.retrieve(query)
        context = "\n\n".join([f"Source: {fname}\nContent: {chunk}" for chunk, fname in docs])
        prompt = f"""Use the context below to answer the question. 
Always cite the source filename after each point using (Source: filename).

Context:
{context}

Question: {query}
Answer:"""
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        print("Response:", response.choices[0].message.content)
        return response.choices[0].message.content
