# 🧠 RAG Chatbot with FastAPI + Streamlit

This project demonstrates a Retrieval-Augmented Generation (RAG) chatbot built using:

- **FastAPI** for the backend API
- **Streamlit** for the frontend interface
- **ChromaDB** for semantic document storage and retrieval
- **Sentence-Transformers** for embeddings
- **RAG** for retrieved contextual
- **OpenAI GPT-4** for generating answers from retrieved chunks

---

## ✅ Features

- Upload documents (PDF, DOCX, TXT) to a `data/` folder
- Chunks are embedded using SentenceTransformers
- GPT-4 uses retrieved chunks to generate contextual answers
- UI allows you to ask questions and view the source documents
- Option to open source PDF files in a new browser tab

---

## 📦 Libraries Used

| Library                  | Purpose                                  |
|--------------------------|------------------------------------------|
| `fastapi`                | Backend API                              |
| `streamlit`              | Frontend UI                              |
| `openai`                 | GPT-4 integration                        |
| `chromadb`               | Vector storage for retrieval             |
| `sentence-transformers` | Embedding generator                      |
| `python-docx`, `PyMuPDF`| Parsing DOCX and PDF documents           |



**Clone the repo**:
```bash

git clone https://github.com/yourname/rag-chatbot.git
cd rag-chatbot
```



**Create and activate a virtual environment**

```bash
conda create -n rag-chatbot python=3.10
conda activate rag-chatbot
```
**Create .env file**
```bash
Create a .env file in the root directory and add:
 Set your OpenAI API key
Or update app/config.py with your key.
```
**Install all depe:**

```bash
pip install -r requirements.txt
```

**Run FastAPI backend**
```bash

uvicorn app.main:app --reload

```
**UI**
```bash
cd ui
streamlit run app.py
```

 **Sample Queries to Test**

```bash

 "Who is Aniket Jadon?"

"What AI projects has he worked on?"

"Tell me about the JSPL chatbot"

"What is AnginaX Agentic AI?"

```



