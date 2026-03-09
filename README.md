
# RAG Knowledge Assistant

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-blue)
![FAISS](https://img.shields.io/badge/VectorDB-FAISS-orange)
![LLM](https://img.shields.io/badge/LLM-LLaMA3-purple)

A **full-stack Retrieval-Augmented Generation (RAG) system** that enables users to ingest GitHub repositories and ask natural language questions about the codebase.

The system retrieves relevant code snippets using **semantic vector search** and generates context-aware answers using a **Large Language Model (LLaMA-3)**.

This project demonstrates how to build a **production-style LLM application** combining modern AI infrastructure with scalable backend architecture.

---

# Problem

Large codebases are difficult to understand, especially when:

* onboarding to a new project
* exploring open-source repositories
* trying to locate specific logic

Traditional keyword search is limited because it cannot understand **semantic meaning**.

This project solves that problem by combining **vector search + LLM reasoning**.

---

# Solution

The system implements **Retrieval-Augmented Generation (RAG)**:

1. Repository code is converted into embeddings.
2. Embeddings are stored in a **vector database (FAISS)**.
3. User questions are converted into embeddings.
4. The system retrieves the **most relevant code chunks**.
5. An LLM generates answers using the retrieved context.

This ensures responses are **grounded in the actual codebase**.

---

# System Architecture

```
                +------------------+
                |     Frontend     |
                | React + Vite UI  |
                +--------+---------+
                         |
                         | REST API
                         |
                +--------v---------+
                |      FastAPI     |
                | Backend Services |
                +--------+---------+
                         |
            +------------+-------------+
            |                          |
      +-----v-----+             +------v------+
      |  MongoDB  |             |    Redis    |
      | User Data |             |   Caching   |
      +-----------+             +-------------+

                         |
                         |
                 +-------v-------+
                 |  Embeddings   |
                 | SentenceTrans |
                 +-------+-------+
                         |
                  Vector Storage
                         |
                 +-------v-------+
                 |     FAISS     |
                 | Vector Search |
                 +-------+-------+
                         |
                 Context Retrieval
                         |
                 +-------v-------+
                 |   LLaMA-3     |
                 |  Groq API     |
                 +---------------+
```

---

# Features

* Retrieval-Augmented Generation (RAG)
* GitHub repository ingestion
* Semantic code search
* Context-aware LLM responses
* JWT-based authentication
* Vector database with FAISS
* Redis caching for faster queries
* Chat history persistence
* Full-stack architecture (React + FastAPI)

---

# Tech Stack

## Frontend

* React
* TypeScript
* Vite

## Backend

* FastAPI
* Python
* JWT Authentication
* REST APIs

## AI / Machine Learning

* Sentence Transformers
* FAISS Vector Database
* Retrieval-Augmented Generation

## Infrastructure

* MongoDB
* Redis
* Groq API (LLaMA-3)

---

# Data Flow

## Repository Ingestion

1. User submits GitHub repository URL
2. Backend clones repository
3. Files are split into chunks
4. Sentence Transformers generate embeddings
5. Embeddings stored in FAISS vector index
6. Metadata stored in MongoDB

---

## Query Processing

1. User asks question in chat interface
2. Question converted into embedding
3. FAISS retrieves top-K similar code chunks
4. Context assembled with user query
5. Sent to LLaMA-3 (Groq API)
6. Generated answer returned to user

---

# Example Use Cases

* Understanding unfamiliar repositories
* AI-assisted code exploration
* Developer onboarding
* Semantic code search
* Intelligent documentation assistant

---

# Future Improvements

* Multi-repository knowledge base
* Code summarization
* Streaming LLM responses
* Role-based access control
* Docker deployment
* Support for documents (PDFs, docs)

---

# Author

**Aditya Pratap Singh**

Machine Learning Engineer | AI Systems | Backend Development

* YouTube: DataDissection
* Focus Areas: AI Systems, Computer Vision, LLM Applications


# Screenshots

![Dashboard](images/dashboard.png)
![Chat Interface](images/chat.png)
```

---

If you want, I can also give you **3 very small additions that make GitHub projects look “senior engineer level” instead of student projects** (most people don’t know these).
