# app/main.py
import os
from pathlib import Path
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_vertexai import ChatVertexAI
from fastapi import FastAPI
from pydantic import BaseModel




emb_v = VertexAIEmbeddings(
    model_name="gemini-embedding-001",
    project="bank-report-rag",
    location="us-central1",
)
                       
vec_path = Path("data/processed/chroma_td2024_vertex")
vectordb_v = Chroma(
    persist_directory=str(vec_path),
     collection_name="bank_reports",  
    embedding_function=emb_v
)


llm = ChatVertexAI(
    model = "gemini-2.5-pro",
    temperature=0
)


def answer_question(question, bank="TD", year=2024, k=5, show_snippets=True):
    retriever = vectordb_v.as_retriever(
        search_kwargs={"k":k, "filter":{"$and": [
        {"bank": "TD"},
        {"year": 2024}
        ]
        }}
    )

    docs = retriever.invoke(question)   

  
    seen = set()
    unique_docs = []
    for d in docs:
        md = d.metadata or {}
        key = (md.get("pdf_page"), md.get("chunk_id"))
        if key in seen:
            continue
        seen.add(key)
        unique_docs.append(d)

    context_blocks = []
    sources = []

    for d in unique_docs:
        md = d.metadata or {}
        pg = md.get("pdf_page")
        cid = md.get("chunk_id")
        text = d.page_content

        context_blocks.append(f"[page {pg} | chunk {cid}]\n{text}")

        src = {"pdf_page": pg, "chunk_id": cid}
        if show_snippets:
            src["snippet"] = text[:220].replace("\n", " ") + "..."
        sources.append(src)

    context = "\n\n---\n\n".join(context_blocks)

    prompt = f"""You are a helpful analyst reading a bank annual report.
            Use ONLY the provided context.
            If the answer is not in the context, say: "I do not know based on the provided text."

            QUESTION:
            {question}

            CONTEXT:
            {context}

            Return:
            1) Answer (short, clear)
            2) Bullet list of key evidence (1-4 bullets)
            """

    resp = llm.invoke(prompt)
    return {"answer": resp.content, "sources": sources}

app = FastAPI(title="Bank Annual Report RAG")

# -----------------------
# 3) API schema
# -----------------------
class AskRequest(BaseModel):
    question: str
    bank: str = "TD"
    year: int = 2024
    k: int = 5


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(req: AskRequest):
    return answer_question(req.question, bank=req.bank, year=req.year, k=req.k)


print("API STARTED")

print("Chroma path:", vec_path.resolve())
print("Path exists:", vec_path.exists())
print("Files:", list(vec_path.glob("*")))

print("Collection count:", vectordb_v._collection.count())
