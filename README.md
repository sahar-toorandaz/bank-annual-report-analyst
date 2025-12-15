# Bank Annual Report Q&A (RAG)

This project allows users to ask questions about bank annual reports and receive clear answers based only on the report content.  
It is an end-to-end example of a Retrieval-Augmented Generation (RAG) system.

The same pipeline works with both **OpenAI** and **Google Vertex AI (Gemini)** by switching the LLM and embedding provider.

---

## What It Does

- Reads bank annual report PDFs  
- Breaks them into small text chunks  
- Stores the content in a vector database  
- Finds the most relevant sections for a question  
- Uses a language model to answer using only those sections  
- Shows where the answer came from (page and chunk)  

---

## How It Works

1. PDF reports are converted to clean text  
2. Text is split into overlapping chunks  
3. Each chunk is embedded and stored in Chroma  
4. A user question is embedded  
5. The most relevant chunks are retrieved  
6. The model generates an answer using only that context  

---

## LLM Options

- OpenAI: embeddings + chat model for local development  
- Vertex AI (Gemini): alternative provider for the same pipeline, designed for GCP deployment  

---

## Local App

- FastAPI backend for the `/ask` endpoint  
- Streamlit UI for interactive Q&A  

---

## Cloud Deployment (GCP)

This project is designed to run on Google Cloud:

- Docker is used to containerize the FastAPI service  
- The container image is pushed to Artifact Registry (GCP container repository)  
- The container is deployed to Cloud Run for a managed, scalable API endpoint  
- Vertex AI (Gemini) can be used in the deployed version for LLM calls  

---

## Tech Stack

- Python  
- LangChain  
- OpenAI and Vertex AI (Gemini)  
- Chroma vector database  
- FastAPI (backend)  
- Streamlit (UI)  
- Docker  
- GCP: Artifact Registry + Cloud Run + Vertex AI  

---

## Example

Question:
"What are the main risk factors mentioned for 2024?"


Output:
- A short, grounded answer  
- Supporting points  
- Page and chunk references  

---

## Why This Project

This project was built to demonstrate practical experience with:
- RAG systems and vector search  
- OpenAI and Vertex AI (Gemini) integration  
- Building a small AI product (API + UI)  
- Containerization and deployment on GCP (Docker, Artifact Registry, Cloud Run)  
