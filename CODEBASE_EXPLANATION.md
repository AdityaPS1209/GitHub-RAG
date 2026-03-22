# 🚀 RAG Knowledge Assistant - Codebase Explanation

This document provides a comprehensive overview of the application's architecture, what each file is responsible for, and the foundational concepts that make the system work.

---

## 1. 🌊 The Whole Flow of Code

The application operates primarily through two major data flows: **Repository Ingestion** and **User Querying**.

### A. Repository Ingestion Flow (Adding a GitHub Repo)
When a user submits a GitHub repository URL via the frontend dashboard:
1. **API Call**: The frontend sends a `POST` request to the backend `ingest_controller.py`.
2. **Background Task**: The controller immediately returns a success response and hands the heavy lifting off to a background worker via Celery (`tasks.py`).
3. **Cloning & Parsing**: The `ingestion_service.py` clones the repository securely into a temporary folder and reads the relevant code and text files.
4. **Chunking**: The raw text from the files is split into smaller, manageable chunks (e.g., 500 characters each) so the LLM doesn't get overwhelmed with unrelated code later.
5. **Embedding**: The `embedding_service.py` uses a machine learning model (`Sentence-Transformers`) to convert each text chunk into a multi-dimensional array of numbers (an embedding).
6. **Storage**: The vectors are saved into a local vector database (**FAISS**) via `vector_repo.py`, while the track record and status of the ingestion are saved to MongoDB.

### B. User Query Flow (Asking the Copilot)
When a user asks a question like *"How does the auth controller work?"*:
1. **API Call**: The chat interface sends a `POST` request to the backend `query_controller.py`.
2. **Question Embedding**: The user's question is passed to `embedding_service.py` to be converted into an embedding in the exact same vector space as the code chunks.
3. **Semantic Search**: The `query_service.py` searches the FAISS database for the "nearest neighbors" — the code chunks with embeddings most mathematically similar to the question's embedding. This pulls the most relevant code contexts.
4. **Context Assembly**: The retrieved code chunks are combined with the user's original question to form a prompt.
5. **LLM Generation**: The prompt is sent to the LLM via `llm_service.py` (Groq API using LLaMa 3). The LLM reads the context and generates an intelligent, natural language answer.
6. **Delivery**: The final answer is returned to the frontend and displayed in the chat interface.

---

## 2. 📂 What Each File Does

### 🔙 Backend (FastAPI + Python)
The backend is structured using a clean, layered controller-service-repository architecture.

* **`main.py`**: The entry point of the FastAPI application. It sets up routing, configures CORS, and initializes the application state.
* **`controllers/`** *(API Endpoints - Route handling)*
  * `auth_controller.py`: Defines the endpoints for user signup and login.
  * `ingest_controller.py`: Defines the endpoint to trigger GitHub repository ingestion.
  * `query_controller.py`: Defines the endpoint to handle chat queries from users.
* **`services/`** *(Business Logic - Where the core work happens)*
  * `auth_service.py`: Contains the logic for authenticating users and hashing passwords.
  * `ingestion_service.py`: Handles cloning git repositories, reading file text, and splitting text into chunks.
  * `embedding_service.py`: Uses `sentence-transformers` to generate mathematical vector representations of text.
  * `query_service.py`: Orchestrates the search process (queries FAISS, gathers context, then calls the LLM).
  * `llm_service.py`: Connects to external AI APIs (like Groq) to leverage the LLaMa-3 model for response generation.
  * `eval_service.py`: Utility service responsible for testing and evaluating LLM answer quality.
* **`repositories/`** *(Database Access - CRUD operations)*
  * `user_repo.py`: Handles interacting with MongoDB to read/write user profiles and settings.
  * `vector_repo.py`: Manages the FAISS index files (saving, loading, and querying vector embeddings).
* **`models/`** *(Data Schemas - Pydantic definitions)*
  * `user.py`: API payload schemas for user registration and authentication.
  * `document.py`: Schemas defining the structure of chunks, files, and embeddings.
  * `query.py`: Schemas for incoming chat questions and outgoing answers.
* **`core/`** *(Configuration & Setup)*
  * `config.py`: Loads and provides environment variables (e.g., API keys, DB URIs) to the app.
  * `database.py`: Establishes and manages connections to MongoDB and Redis.
  * `security.py`: Logic for creating and verifying JWT access tokens.
* **`workers/`** *(Asynchronous Tasks)*
  * `celery_app.py`: Configures the Celery instance and message broker (Redis).
  * `tasks.py`: Defines the async task function (`process_repository`) that runs independently of the main API thread.

### 🖼️ Frontend (React + TypeScript + Vite)
The UI is an interactive, single-page application built with modern web technologies.

* **`src/main.tsx`** & **`src/App.tsx`**: The root components. They set up the React component tree, the theme provider, and the router.
* **`src/index.css`** & **`src/App.css`**: Contains global stylesheets, including variables for the modern dark glassmorphism theme and custom animations.
* **`src/types.ts`**: TypeScript definitions and interfaces mapping to the backend payload structures (ensuring type safety).
* **`src/pages/`**: Contains the full-page views (Dashboard, Chat, Login, Register). Each corresponds to a core route.
* **`src/components/`**: Reusable UI blocks like Buttons, Input fields, Navbars, Sidebars, and Chat message bubbles.
* **`src/context/`**: Contains React Contexts, mostly used to manage global state like whether a user is logged in.
* **`src/lib/`**: Contains utility functions, and centralized API clients (like Axios/Fetch setups with interceptors to automatically attach JWT tokens).

---

## 3. 🧠 Key Concepts Used

### 1. RAG (Retrieval-Augmented Generation)
An architectural pattern that gives an LLM access to external data. Large Language Models don't know about private codebases. RAG solves this by first *Retrieving* relevant code from a database, *Augmenting* the user's prompt with that code, and then asking the LLM to *Generate* an answer.

### 2. Vector Embeddings
A fundamental Machine Learning concept where text is converted into an array (vector) of floating-point numbers. Semantically similar texts (e.g., "login mechanism" and "authentication flow") will have numbers that end up mathematically close to each other in a multi-dimensional space, even if they don't share exact keywords.

### 3. Semantic Search & FAISS
Standard database searches look for exact string matches. Semantic search uses Vector Embeddings to find concepts that *mean* the same thing. FAISS (Facebook AI Similarity Search) is an ultra-fast local database optimized for storing these massive arrays and instantly finding the "nearest neighbors" (most similar chunks) to a query.

### 4. Background Message Queues (Celery + Redis)
To prevent the web API from crashing or freezing when downloading and processing thousands of lines of code, the system uses a queue. The API sends a message to Redis ("Process repo X"). Celery, a background worker, picks up that message and does the heavy lifting seamlessly behind the scenes.

### 5. JWT (JSON Web Tokens)
A secure way to manage user sessions without storing server-side state. Upon logging in, the server gives the client a signed token. The client sends this token with every subsequent request. The server verifies the signature to ensure the user is who they claim to be.

### 6. Dependency Injection & Service Layer Pattern
The backend structure isolates concerns. Controllers handle HTTP (JSON in/out). Services hold pure business logic (chunking, searching). Repositories handle database specifics. FastAPI's Dependency Injection system easily passes these layers into each other, making the code clean, modular, and easy to test.
