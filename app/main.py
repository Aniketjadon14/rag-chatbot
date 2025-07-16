from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import RAGSystem

app = FastAPI()
rag = RAGSystem()

# 👇 Yaha daal do
@app.on_event("startup")
async def startup_event():
    rag.ingest_documents()
    rag.create_embeddings()

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(query: Query):
    answer = rag.generate_answer(query.question)
    return {"answer": answer}
