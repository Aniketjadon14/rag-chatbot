from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import RAGSystem
import mimetypes
import os
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException

app = FastAPI()
rag = RAGSystem()

@app.on_event("startup")
async def startup_event():
    rag.ingest_documents()
    rag.create_embeddings()

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(query: Query):
    answer = rag.generate_answer(query.question)
    docs = rag.get_last_retrieved_docs() 
    return {"answer": answer,
            "sources": [{"filename": fname, "chunk": doc} for doc, fname in docs]
        }
        

@app.get("/retrieved-docs")
def get_retrieved_docs():
    docs = rag.get_last_retrieved_docs()
    return {"docs": [{"content": doc, "filename": fname} for doc, fname in docs]}


@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = f"./data/{filename}"
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/pdf',
            headers={"Content-Disposition": f'inline; filename="{filename}"'}
        )
    raise HTTPException(status_code=404, detail="File not found")
