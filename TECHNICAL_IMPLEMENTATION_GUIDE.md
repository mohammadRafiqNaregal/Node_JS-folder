# Technical Implementation Guide - Enterprise AI Knowledge Assistant

## Table of Contents

1. [Tech Stack Justification](#tech-stack-justification)
2. [Project Structure](#project-structure)
3. [Core Implementation Details](#core-implementation-details)
4. [Configuration & Environment Setup](#configuration--environment-setup)
5. [Development Guide](#development-guide)
6. [Testing Strategy](#testing-strategy)
7. [Performance Benchmarks](#performance-benchmarks)

---

## Tech Stack Justification

### Backend Framework: FastAPI

**Why FastAPI over Django/Flask?**

| Criteria                   | FastAPI                | Django                | Flask          |
| -------------------------- | ---------------------- | --------------------- | -------------- |
| **Speed**                  | ⚡⚡⚡ Modern async    | ⚡⚡ Synchronous      | ⚡ Synchronous |
| **Built-in Documentation** | ✓ Swagger + ReDoc      | Manual setup          | Manual setup   |
| **Async Support**          | ✓ Native               | Partial (Django 3.1+) | Limited        |
| **Type Hints**             | ✓ Full support         | Minimal               | None           |
| **Validation**             | ✓ Pydantic auto        | Manual                | Manual         |
| **Performance**            | 5000 req/s             | 2000 req/s            | 1500 req/s     |
| **Learning Curve**         | Medium                 | Steep                 | Easy           |
| **Scalability**            | Horizontal (stateless) | Vertical              | Vertical       |

**For this project**:

- High-throughput chat API needed
- Async document processing fits perfectly
- Auto API documentation crucial for team
- Pydantic models save validation code

### Database: SQLite

**Why SQLite for MVP?**

**Pros**:

- ✓ Zero configuration
- ✓ File-based (easy backup)
- ✓ All data in single file
- ✓ Sufficient for ~10k chats/day
- ✓ Excellent for development
- ✓ ACID compliant

**Cons**:

- ✗ Single-writer problem
- ✗ Not suitable for 100k+ concurrent queries
- ✗ No built-in replication

**Migration Path** (Phase 2):

```python
# To PostgreSQL - just change connection string
# SQLAlchemy makes this seamless
DB_URL = "postgresql://user:password@localhost/knowledge_assistant"
# vs current
DB_URL = "sqlite:///./knowledge_assistant.db"
```

### Vector Database: FAISS

**Why FAISS?**

| Feature               | FAISS      | Pinecone     | Weaviate | Milvus     |
| --------------------- | ---------- | ------------ | -------- | ---------- |
| **Cost**              | Free       | $$$          | $$       | $          |
| **Setup Time**        | 5 min      | 2 min        | 30 min   | 60 min     |
| **Local Development** | ✓ Easy     | ✗ Cloud only | ✓ Docker | ✓ Docker   |
| **Performance**       | ⚡⚡ 100ms | ⚡⚡⚡ 50ms  | ⚡ 200ms | ⚡⚡ 100ms |
| **For MVP**           | Perfect    | Overkill     | Good     | Good       |

**FAISS Advantages**:

- Runs locally without additional infrastructure
- Extremely fast (millions of vectors in memory)
- Backed by Meta (production-proven)
- Easy Python integration
- Perfect for single-machine MVP

**When to Migrate**:

- If multi-region support needed
- If document store > 10GB
- If query SLA < 50ms required

### LLM Integration: LangChain

**Benefits**:

- Unified interface for multiple LLMs (OpenAI, HuggingFace, Llama)
- Built-in prompt templates
- Document loaders and splitters
- Memory management
- Easy switching between providers

**Example**:

```python
# Same code works for any LLM
from langchain.llms import OpenAI, HuggingFaceHub

# Switch by config
llm = OpenAI(api_key=OPENAI_KEY)  # Production
# or
llm = HuggingFaceHub(repo_id="model-name")  # Open source
```

### Embeddings: HuggingFace (Recommended)

**Comparison**:

| Provider        | Model                  | Speed        | Cost | Quality    | Setup |
| --------------- | ---------------------- | ------------ | ---- | ---------- | ----- |
| **HuggingFace** | all-MiniLM-L6-v2       | ⚡⚡⚡ Local | Free | ⭐⭐⭐⭐   | 2 min |
| **OpenAI**      | text-embedding-3-small | ⚡⚡ API     | $    | ⭐⭐⭐⭐⭐ | 1 min |
| **Cohere**      | embed-english-v3.0     | ⚡⚡ API     | $    | ⭐⭐⭐⭐   | 1 min |

**For MVP Phase 1**: Use HuggingFace (local, no API calls, fast)

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # 22MB
embeddings = model.encode(["text1", "text2"])  # Returns 384-dim vectors

# Migration to OpenAI later
from langchain.embeddings.openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(api_key=OPENAI_KEY)
```

### File Parsing: PyPDF2 + python-docx

**Why these**:

- PyPDF2: Most reliable PDF library
- python-docx: Native DOCX support
- Simple integration with LangChain

**Alternative libraries**:

- Pypdf: Newer, faster version of PyPDF2
- PDFMiner: More accurate but slower
- Apache Tika: Requires Java, overkill

### Frontend: React + Vite + shadcn/ui + Tailwind

**Recommended for Phase 1**: React (Vite) with shadcn/ui and Tailwind CSS

- Better fit for a multi-screen internal product with auth, uploads, admin views, and chat
- shadcn/ui gives accessible UI primitives without locking you into a heavy design framework
- Tailwind keeps the UI system fast to iterate on and easy to standardize
- Vite gives fast local development and a simple build pipeline

**Recommended UI stack**:

- `react` + `react-router-dom` for routing and application structure
- `tailwindcss` for styling and layout
- `shadcn/ui` for forms, dialogs, tables, tabs, badges, dropdowns, and toast primitives
- `react-hook-form` + `zod` for auth and upload forms
- `@tanstack/react-query` for client-side server state where useful
- `@tanstack/react-table` for document/admin tables
- `sonner` for notifications
- `lucide-react` for icons

### AI UI Libraries for RAG Applications

**Best option**: Vercel AI SDK

- `ai` for server-side model and streaming primitives
- `@ai-sdk/react` for `useChat` and React chat state
- `@ai-sdk/openai` or another provider adapter depending on provider choice

**Why it fits**:

- Simplifies chat message state and streaming updates
- Makes chat UI delivery much faster than building the interaction model from scratch
- Works well in plain React applications

**Important distinction**:

- LangChain is the backend orchestration layer, not a frontend UI library
- Keep retrieval, permission filtering, and prompt construction in FastAPI
- Use AI SDK in the frontend, with FastAPI streaming endpoints for token streaming UX

**Recommended architecture split**:

- FastAPI: authentication, document upload, parsing, chunking, embeddings, FAISS retrieval, role checks, chat history
- React frontend: login, admin upload flow, document list, chat experience
- Optional lightweight Node/BFF proxy only if required by your deployment constraints

---

## Project Structure

```
enterprise-knowledge-assistant/
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
│
├── backend/
│   ├── main.py                    # FastAPI entry point
│   ├── config.py                  # Configuration settings
│   ├── database.py                # SQLAlchemy setup
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py               # User model (SQLAlchemy)
│   │   ├── document.py           # Document model
│   │   ├── chat_history.py       # Chat history model
│   │   └── access_log.py         # Audit logging model
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py               # Pydantic schemas for validation
│   │   ├── document.py
│   │   ├── chat.py
│   │   └── common.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py       # User CRUD + auth logic
│   │   ├── document_service.py   # Document CRUD
│   │   ├── chat_service.py       # Chat logic
│   │   ├── search_service.py     # Vector search
│   │   └── processing_service.py # Async document processing
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py             # Main router combiner
│   │   ├── auth.py               # /api/v1/auth endpoints
│   │   ├── documents.py          # /api/v1/documents endpoints
│   │   ├── chat.py               # /api/v1/chat endpoints
│   │   ├── search.py             # /api/v1/search endpoints
│   │   └── admin.py              # /api/v1/admin endpoints
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py               # JWT validation
│   │   ├── rbac.py               # Role-based access control
│   │   └── error_handler.py      # Global error handling
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── security.py           # Password hashing, JWT
│   │   ├── logger.py             # Structured logging
│   │   ├── embeddings.py         # Embedding generation
│   │   └── file_parser.py        # PDF/DOCX parsing
│   │
│   ├── cache/
│   │   ├── __init__.py
│   │   └── faiss_cache.py        # FAISS index management
│   │
│   └── uploads/                  # User-uploaded files
│       └── .gitkeep
|
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── postcss.config.js
│   ├── tailwind.config.ts
│   ├── components.json          # shadcn/ui config
│   ├── index.html
│   │
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── styles/
│   │   │   └── globals.css
│   │   ├── pages/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── AdminUploadPage.tsx
│   │   │   ├── DocumentsPage.tsx
│   │   │   └── ChatPage.tsx
│   │   ├── routes/
│   │   │   ├── router.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   ├── components/
│   │   │   ├── ui/              # shadcn/ui generated components
│   │   │   ├── admin/
│   │   │   ├── chat/
│   │   │   └── documents/
│   │   ├── hooks/
│   │   │   ├── use-auth.ts
│   │   │   └── use-chat-stream.ts
│   │   └── lib/
│   │       ├── api-client.ts
│   │       ├── auth.ts
│   │       ├── validators.ts
│   │       └── utils.ts
│   │
│   └── public/
│       └── logo.svg
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_auth.py
│   ├── test_documents.py
│   ├── test_chat.py
│   ├── test_search.py
│   └── test_integration.py
│
├── scripts/
│   ├── init_db.py               # Initialize database
│   ├── seed_data.py             # Add sample data
│   └── build_index.py           # Rebuild FAISS index
│
├── logs/                        # Application logs
│   └── .gitkeep
│
└── docker/                      # (Future: Docker support)
    ├── Dockerfile
    └── docker-compose.yml
```

---

## Core Implementation Details

### 1. Authentication Service

```python
# backend/utils/security.py
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    @staticmethod
    def create_access_token(user_id: str, role: str, expires_in_hours: int = 24) -> str:
        payload = {
            "user_id": user_id,
            "role": role,
            "exp": datetime.utcnow() + timedelta(hours=expires_in_hours),
            "iat": datetime.utcnow()
        }
        return jwt.encode(
            payload,
            os.getenv("JWT_SECRET"),
            algorithm="HS256"
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        return jwt.decode(
            token,
            os.getenv("JWT_SECRET"),
            algorithms=["HS256"]
        )
```

### 2. Middleware: RBAC Enforcement

```python
# backend/middleware/rbac.py
from fastapi import HTTPException, status
from typing import Dict, List

ROLE_PERMISSIONS = {
    "Admin": {
        "upload_document": True,
        "view_all_documents": True,
        "delete_document": True,
        "manage_users": True,
        "view_chat_history": True,
        "ask_questions": True,
    },
    "HR_User": {
        "upload_document": False,
        "view_all_documents": False,
        "delete_document": False,
        "manage_users": False,
        "view_chat_history": False,
        "ask_questions": True,
        "view_hr_documents": True,
    },
    "Finance_User": {
        "upload_document": False,
        "ask_questions": True,
        "view_finance_documents": True,
    },
    "IT_User": {
        "upload_document": False,
        "ask_questions": True,
        "view_it_documents": True,
    },
    "Employee": {
        "upload_document": False,
        "ask_questions": True,
        "view_public_documents": True,
    }
}

def check_permission(user_role: str, permission: str) -> bool:
    """Check if user role has permission"""
    return ROLE_PERMISSIONS.get(user_role, {}).get(permission, False)

def verify_document_access(user_role: str, allowed_roles: List[str]) -> bool:
    """Check if user can access document"""
    if user_role == "Admin":
        return True
    return user_role in allowed_roles
```

### 3. Document Processing Pipeline

```python
# backend/services/processing_service.py
import asyncio
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class DocumentProcessor:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.faiss_index = None
        self.chunk_size = 1000
        self.chunk_overlap = 200

    async def process_document(self, doc_id: str, file_path: str):
        """Main processing pipeline"""
        try:
            # 1. Extract text
            text = await self._extract_text(file_path)

            # 2. Chunk text
            chunks = self._chunk_text(text)

            # 3. Generate embeddings
            embeddings = self.embedding_model.encode(chunks)

            # 4. Add to FAISS index
            dimension = embeddings.shape[1]
            self.faiss_index = faiss.IndexFlatL2(dimension)
            self.faiss_index.add(embeddings.astype('float32'))

            # 5. Store chunks in DB
            await self._store_chunks(doc_id, chunks, embeddings)

            return {"status": "completed", "chunks": len(chunks)}

        except Exception as e:
            print(f"Error processing document {doc_id}: {e}")
            return {"status": "failed", "error": str(e)}

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = " ".join(words[i:i + self.chunk_size])
            chunks.append(chunk)

        return chunks

    async def _extract_text(self, file_path: str) -> str:
        """Extract text based on file type"""
        path = Path(file_path)

        if path.suffix == ".pdf":
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            text = "".join([page.extract_text() for page in reader.pages])

        elif path.suffix == ".docx":
            from docx import Document
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])

        elif path.suffix == ".txt":
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")

        return text
```

### 4. Search & Retrieval Service

```python
# backend/services/search_service.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class SearchService:
    def __init__(self, faiss_index_path: str = None):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.faiss_index = None
        self.document_id_map = {}  # embedding_id -> doc_id

        if faiss_index_path:
            self.load_index(faiss_index_path)

    def search(self, query: str, k: int = 10, threshold: float = 0.7) -> List[Dict]:
        """Search for relevant documents"""
        # Generate embedding for query
        query_embedding = self.embedding_model.encode([query])[0]
        query_embedding = np.array([query_embedding]).astype('float32')

        # Search FAISS index
        distances, indices = self.faiss_index.search(query_embedding, k)

        results = []
        for idx, distance in zip(indices[0], distances[0]):
            # Convert L2 distance to similarity score (0-1)
            similarity = 1 / (1 + distance)

            if similarity >= threshold:
                doc_id = self.document_id_map.get(int(idx))
                results.append({
                    "document_id": doc_id,
                    "score": float(similarity),
                    "distance": float(distance)
                })

        return sorted(results, key=lambda x: x['score'], reverse=True)
```

### 5. Chat Service with LLM Integration

```python
# backend/services/chat_service.py
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from database import ChatHistory

class ChatService:
    def __init__(self, search_service, llm_api_key: str):
        self.search_service = search_service
        self.llm = OpenAI(api_key=llm_api_key, temperature=0.7)
        self.system_prompt = """You are a helpful knowledge assistant.
Answer questions only using the provided document context.
If you cannot answer from the context, say "I don't have information on this topic in our documents."
Be concise and professional."""

    async def answer_question(
        self,
        user_id: str,
        question: str,
        user_role: str,
        allowed_documents: List[str]
    ) -> Dict:
        """Generate answer based on retrieved context"""

        # 1. Search for relevant documents
        search_results = self.search_service.search(question, k=10)

        # 2. Filter by user permissions
        accessible_results = [
            r for r in search_results
            if r['document_id'] in allowed_documents
        ]

        # 3. Retrieve full chunks
        chunks = await self._retrieve_chunks(accessible_results)

        # 4. Build context
        context = "\n\n".join([
            f"From {c['document_title']}:\n{c['content']}"
            for c in chunks[:5]
        ])

        # 5. Call LLM
        user_message = f"""Context from documents:
{context}

Question: {question}

Answer:"""

        response = self.llm(self.system_prompt + "\n\n" + user_message)

        # 6. Store in chat history
        chat_record = ChatHistory(
            user_id=user_id,
            question=question,
            response=response,
            retrieved_documents=[r['document_id'] for r in accessible_results]
        )
        await self._store_chat(chat_record)

        return {
            "response": response,
            "documents_used": chunks,
            "confidence": min([r['score'] for r in accessible_results])
        }
```

---

## Configuration & Environment Setup

### Environment Variables

```bash
# .env file (never commit this!)
# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=False

# Database
DATABASE_URL=sqlite:///./knowledge_assistant.db

# JWT
JWT_SECRET=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24

# LLM & Embeddings
OPENAI_API_KEY=sk-...  # Leave empty to use HuggingFace
HUGGINGFACE_MODEL=all-MiniLM-L6-v2

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# File Upload
MAX_FILE_SIZE_MB=50
UPLOAD_DIR=./uploads

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Admin credentials (for initial setup only)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-in-production
```

### FastAPI Configuration

```python
# backend/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Config
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./knowledge_assistant.db"

    # JWT
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_hours: int = 24

    # LLM
    openai_api_key: str = ""
    huggingface_model: str = "all-MiniLM-L6-v2"

    # File Upload
    max_file_size_mb: int = 50
    upload_dir: str = "./uploads"
    allowed_extensions: List[str] = ["pdf", "docx", "txt"]

    # CORS
    allowed_origins: List[str] = ["http://localhost:5173"]

    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

### FastAPI App Setup

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.router import router
from config import settings
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Enterprise Knowledge Assistant API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug
    )
```

---

## Development Guide

### Initial Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd enterprise-knowledge-assistant

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env with your settings

# 5. Initialize database
python scripts/init_db.py

# 6. Seed sample data (optional)
python scripts/seed_data.py

# 7. Start development server
python -m uvicorn backend.main:app --reload

# API should be available at http://localhost:8000
# Swagger UI: http://localhost:8000/docs
```

### Running the Frontend

```bash
# Start React frontend (Vite)
cd frontend
npm install
npm run dev

# Access at http://localhost:5173
```

### Building Requirements

```
# requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.1.1
PyPDF2==3.0.1
python-docx==0.8.11
sentence-transformers==2.2.2
faiss-cpu==1.7.4
langchain==0.1.1
openai==1.3.8
python-multipart==0.0.6
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_auth.py
import pytest
from backend.utils.security import SecurityUtils

class TestAuthentication:
    def test_password_hashing(self):
        password = "test_password"
        hashed = SecurityUtils.hash_password(password)

        assert hashed != password
        assert SecurityUtils.verify_password(password, hashed)

    def test_jwt_token_creation(self):
        token = SecurityUtils.create_access_token(
            user_id="123",
            role="Admin"
        )

        payload = SecurityUtils.decode_token(token)
        assert payload["user_id"] == "123"
        assert payload["role"] == "Admin"

    def test_jwt_token_expiration(self):
        from datetime import datetime, timedelta
        token = SecurityUtils.create_access_token(
            user_id="123",
            role="Admin",
            expires_in_hours=-1  # Expired
        )

        with pytest.raises(Exception):  # jwt.ExpiredSignatureError
            SecurityUtils.decode_token(token)
```

### Integration Tests

```python
# tests/test_integration.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

class TestCompleteWorkflow:
    def test_user_login_upload_query_workflow(self):
        # 1. Register user
        response = client.post("/api/v1/auth/register", json={
            "username": "testuser",
            "password": "password123",
            "email": "test@example.com",
            "role": "Admin"
        })
        assert response.status_code == 201
        user_data = response.json()
        token = user_data["token"]

        # 2. Upload document
        with open("test_doc.pdf", "rb") as f:
            response = client.post(
                "/api/v1/documents/upload",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": f},
                data={
                    "title": "Test Document",
                    "department": "HR",
                    "section": "Policies"
                }
            )
        assert response.status_code == 200
        doc_data = response.json()

        # 3. Query document
        response = client.post(
            "/api/v1/chat/ask",
            headers={"Authorization": f"Bearer {token}"},
            json={"question": "What is the PTO policy?"}
        )
        assert response.status_code == 200
```

### Performance Tests

```python
# tests/test_performance.py
import pytest
import time
from backend.services.search_service import SearchService

class TestPerformance:
    def test_search_latency(self):
        search_service = SearchService()
        query = "What are the benefits?"

        start = time.time()
        results = search_service.search(query)
        elapsed = time.time() - start

        assert elapsed < 0.5  # Should complete in < 500ms
        assert len(results) > 0

    def test_embedding_generation_speed(self):
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')

        texts = ["Hello world"] * 100

        start = time.time()
        embeddings = model.encode(texts)
        elapsed = time.time() - start

        assert elapsed < 5  # Should embed 100 texts in < 5 seconds
        assert embeddings.shape == (100, 384)
```

---

## Performance Benchmarks

### Expected Performance Metrics (Phase 1)

| Operation               | Target     | Notes                                   |
| ----------------------- | ---------- | --------------------------------------- |
| **Document Upload**     | < 2s       | Response time, excluding processing     |
| **Document Processing** | < 2 min    | 100-page PDF with chunking + embeddings |
| **Vector Search**       | < 100ms    | Top-10 results from 10k chunks          |
| **Chat Response**       | < 3s       | LLM-dependent, mainly API latency       |
| **JWT Validation**      | < 5ms      | Per-request overhead                    |
| **DB Query**            | < 50ms     | User/document lookups                   |
| **API Throughput**      | 1000 req/s | Concurrent connections                  |
| **Concurrent Users**    | 50+        | Typical office day load                 |

### Load Testing with Locust

```python
# tests/load_test.py
from locust import HttpUser, task, between

class KnowledgeAssistantUser(HttpUser):
    wait_time = between(1, 5)
    token = None

    def on_start(self):
        # Login
        response = self.client.post("/api/v1/auth/login", json={
            "username": "testuser",
            "password": "password123"
        })
        self.token = response.json()["access_token"]

    @task(3)
    def ask_question(self):
        self.client.post(
            "/api/v1/chat/ask",
            headers={"Authorization": f"Bearer {self.token}"},
            json={"question": "What is the PTO policy?"}
        )

    @task(1)
    def list_documents(self):
        self.client.get(
            "/api/v1/documents",
            headers={"Authorization": f"Bearer {self.token}"}
        )

# Run: locust -f tests/load_test.py --headless -u 100 -r 10
```

### Memory Usage Estimates

| Component         | Memory    | Notes                     |
| ----------------- | --------- | ------------------------- |
| FAISS Index       | ~400MB    | For 1M vectors (384-dim)  |
| Embedding Model   | ~100MB    | all-MiniLM-L6-v2          |
| FastAPI Server    | ~150MB    | Python + FastAPI overhead |
| SQLite DB         | ~50MB     | 100k chats, 1k documents  |
| **Total for MVP** | **700MB** | Single server, reasonable |

---

## Deployment Checklist

### Pre-Deployment

- [ ] All tests passing (100% coverage > 80%)
- [ ] Security audit complete
- [ ] Environment variables set correctly
- [ ] Database backed up
- [ ] API tested with Postman collection
- [ ] Frontend assets optimized
- [ ] HTTPS certificates ready
- [ ] Rate limiting configured
- [ ] Logging configured
- [ ] Error monitoring setup (Sentry, etc.)

### Production Setup

- [ ] FastAPI served via Gunicorn (4 workers)
- [ ] Nginx as reverse proxy
- [ ] SSL/TLS certificates (Let's Encrypt)
- [ ] Database backups scheduled (daily)
- [ ] Monitor CPU, memory, disk usage
- [ ] Set up alert for errors > 5%
- [ ] Document API with Postman/Swagger
- [ ] Create admin account
- [ ] Test complete workflow end-to-end

### Monitoring & Maintenance

```python
# Monitoring endpoints
GET /health                    # Basic health
GET /metrics                   # Prometheus metrics
GET /api/v1/admin/stats       # Business metrics
```

---

## Next Phase (Phase 2) Enhancements

### Scalability Improvements

- PostgreSQL for multi-user support
- Redis for caching and sessions
- Celery for distributed processing
- Separate vector database (Pinecone/Weaviate)
- Docker & Kubernetes deployment

### Feature Enhancements

- Advanced chat memory (conversation context)
- Citation tracking (which document + which page)
- Feedback loop (improve responses based on ratings)
- Analytics dashboard
- User preferences and settings
- Notification system

### Security Improvements

- OAuth2 integration
- Two-factor authentication
- API key management
- Audit logging
- Encryption at rest

This completes the comprehensive technical implementation guide for your Enterprise AI Knowledge Assistant MVP!
