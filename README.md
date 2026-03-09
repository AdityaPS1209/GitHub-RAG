# RAG Knowledge Assistant

A production-style Retrieval Augmented Generation (RAG) backend and frontend. 

## Features
- **User Authentication**: JWT-based login/registration.
- **Repository Ingestion**: Scrapes and chunks GitHub repositories asynchronously using Celery.
- **Vector Search**: Embeds tokens using `all-MiniLM-L6-v2` and searches via local FAISS.
- **Chat Copilot**: Generates answers with context from your codebase using OpenAI or Ollama.
- **Modern UI**: Dark-mode glassmorphism React interface.

## Setup Instructions

### 1. Environment Variables
Create a file named `.env` in the `backend/` directory with the following variables:
```env
MONGODB_URL=mongodb+srv://<username>:<password>@cluster.mongodb.net/
MONGODB_DB_NAME=rag_assistant
REDIS_URL=redis://default:<password>@<your-redis-url>:port
OPENAI_API_KEY=sk-...
SECRET_KEY=your-super-secret-key-change-in-production
```

### 2. Run the Backend (FastAPI)
From the project root:
```bash
cd backend
# assuming venv is activated
uvicorn backend.main:app --reload
```

### 3. Run the Celery Worker (Background Tasks)
In a separate terminal, from the project root:
```bash
cd backend
# For Windows, you must use --pool=solo
celery -A backend.workers.celery_app worker --pool=solo -l info
```

### 4. Run the Frontend (Vite + React)
In a separate terminal, from the project root:
```bash
cd frontend
npm run dev
```

Visit `http://localhost:5173` to access the application. Register an account, add a GitHub repository (like `https://github.com/tiangolo/fastapi`), wait for it to be processed by Celery, and then ask questions about it in the Chat copilot!
