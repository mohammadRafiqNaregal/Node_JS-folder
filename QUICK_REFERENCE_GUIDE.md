# Quick Reference Guide - Enterprise AI Knowledge Assistant

## Executive Summary Architecture

### What is Being Built?

An MVP knowledge assistant where:

- **Admins** upload documents (PDF/DOCX/TXT) with metadata
- **Employees** ask natural language questions
- **System** retrieves relevant docs + generates LLM responses
- **Access** is controlled by user role (HR/Finance/IT/etc)

### Key Innovation Points

```
┌─ User Query (Natural Language)
│       ↓
├─ Convert to Vector Embedding
│       ↓
└─ Fast Semantic Search (FAISS)
        ↓
    ┌─ Retrieve Relevant Document Chunks
    │       ↓
    └─ Run Through LLM with Context
            ↓
        Smart Answer Generated
```

---

## Architecture Decision Matrix

### 1. Why This Tech Stack?

| Layer          | Choice                              | Why                                           | Trade-off                    |
| -------------- | ----------------------------------- | --------------------------------------------- | ---------------------------- |
| **Backend**    | FastAPI                             | Async, fast, auto-docs                        | Learning curve               |
| **Database**   | SQLite MVP                          | Zero config, local dev                        | Scales to PostgreSQL         |
| **Vector DB**  | FAISS                               | Free, local, blazing fast                     | Must self-host later         |
| **Embeddings** | HuggingFace                         | Free, local, 384 dims                         | Can switch to OpenAI later   |
| **LLM**        | OpenAI/Llama                        | Best quality/flexibility                      | Context length limits        |
| **Frontend**   | React + Vite + shadcn/ui + Tailwind | Strong fit for chat, admin screens, and forms | More setup than static pages |

### 2. Scalability Path (When Needed)

```
Phase 1 (MVP):           Phase 2 (10k users):      Phase 3 (100k users):
├─ Single FastAPI       ├─ Load Balanced FastAPI  ├─ Microservices
├─ SQLite              ├─ PostgreSQL             ├─ Managed Postgres
├─ FAISS (local)       ├─ Redis Cache            ├─ Pinecone/Weaviate
└─ Single Server       ├─ Message Queue          ├─ Kubernetes
                       └─ Docker                 └─ Cloud Infrastructure
```

---

## Critical Design Principles

### 1. Security by Default

```python
✓ Every API call validates JWT token
✓ Every document access checks user role
✓ No data leakage between roles
✓ Passwords hashed with bcrypt
✓ File uploads validated strictly
```

### 2. Separation of Concerns

```
Frontend     → Handles UI/UX
    ↓
API Layer    → Routes + validation
    ↓
Services     → Business logic
    ↓
Database     → Persistence
    ↓
External     → LLM + Embeddings
```

### 3. Async Everything

```python
# Fast upload response
User uploads file
    ↓ (immediate)
Return job_id to UI
    ↓ (background)
Process document asynchronously
    ↓
Update status for polling
```

---

## Role-Based Access Control (Simplified)

```
Admin
├─ Upload documents
├─ View all documents
├─ Manage users
└─ Ask questions

HR User          Finance User        IT User          Employee
├─ View HR docs  ├─ View Finance     ├─ View IT      ├─ View public
└─ Ask questions └─ Ask questions    └─ Ask questions └─ Ask questions
```

---

## Data Flow at a Glance

### Upload Flow (Admin)

```
User selects file
    ↓
System validates (type, size)
    ↓
Save to disk + DB record (status: pending)
    ↓ [ASYNC]
Extract text from file
    ↓
Split into chunks (1000 tokens, 200 overlap)
    ↓
Generate embeddings (384-dimensional vectors)
    ↓
Store in FAISS index
    ↓
Mark document as "processed"
    ↓
Admin sees status = "processed"
```

### Query Flow (Any Auth User)

```
User: "What is the PTO policy?"
    ↓
Generate embedding for question
    ↓
Search FAISS: "Find 10 most similar chunks"
    ↓
Filter by user's role (HR User can only see HR docs)
    ↓
Take top 5 chunks as context
    ↓
Build prompt: "Using this context, answer: ..."
    ↓
Call LLM (OpenAI/HuggingFace)
    ↓
Return response + source documents
```

---

## Database Schema (Simplified)

```
┌─ USERS
│  ├─ id (PK)
│  ├─ username, email, password_hash
│  ├─ role (Admin, HR_User, Finance_User, IT_User, Employee)
│  └─ department (HR, Finance, IT)
│
├─ DOCUMENTS
│  ├─ id (PK)
│  ├─ title, department, section, tags
│  ├─ file_path, status (pending/processing/processed)
│  ├─ allowed_roles (JSON: ["HR_User", "Employee"])
│  └─ uploaded_by (FK to users)
│
├─ DOCUMENT_CHUNKS
│  ├─ id (PK)
│  ├─ document_id (FK)
│  ├─ content (text chunk)
│  ├─ embedding_id (reference to FAISS index)
│  └─ chunk_index (order)
│
└─ CHAT_HISTORY
   ├─ id (PK)
   ├─ user_id (FK)
   ├─ question, response
   ├─ retrieved_documents (JSON list)
   ├─ feedback (helpful/not_helpful)
   └─ timestamp
```

---

## API Endpoints (Quick Reference)

### Authentication

```
POST   /auth/login              → Get JWT token
POST   /auth/register           → Admin creates user
GET    /auth/me                 → Current user info
```

### Documents

```
POST   /documents/upload        → Admin uploads file
GET    /documents              → List user's documents
GET    /documents/{id}         → View document
DELETE /documents/{id}          → Admin deletes
GET    /documents/{id}/status   → Processing status
```

### Chat

```
POST   /chat/ask                → Ask a question
GET    /chat/history            → Get past questions
POST   /chat/feedback           → Rate response
```

### Search

```
POST   /search                  → Direct vector search
```

### Admin

```
GET    /admin/stats             → Overview metrics
GET    /admin/users             → All users
```

---

## Key Files & Their Purpose

```
backend/
├─ main.py                  → FastAPI app initialization
├─ config.py                → Settings from .env
├─ database.py              → SQLAlchemy setup
│
├─ models/                  → Database models (SQLAlchemy)
│   ├─ user.py
│   ├─ document.py
│   └─ chat_history.py
│
├─ schemas/                 → Request/response validation (Pydantic)
│   └─ user.py
│
├─ services/                → Business logic
│   ├─ auth_service.py      → Login, token generation
│   ├─ document_service.py  → Upload, list, delete
│   ├─ search_service.py    → Vector search
│   ├─ chat_service.py      → LLM orchestration
│   └─ processing_service.py → Async document processing
│
├─ api/                     → REST endpoints
│   ├─ auth.py              → /auth routes
│   ├─ documents.py         → /documents routes
│   ├─ chat.py              → /chat routes
│   └─ search.py            → /search routes
│
└─ utils/
    ├─ security.py          → JWT, password hashing
    ├─ embeddings.py        → Generate vectors
    └─ file_parser.py       → Extract text from PDF/DOCX
```

---

## Implementation Timeline

```
Week 1-2: Foundation
├─ FastAPI setup + database
├─ User authentication (login/JWT)
└─ Basic CRUD for users

Week 3-4: Document Management
├─ File upload API
├─ Document storage
└─ Metadata handling

Week 5-6: Vector Search
├─ Text extraction (PDF/DOCX)
├─ Chunking strategy
├─ Embedding generation
└─ FAISS integration

Week 7-8: LLM Integration
├─ LangChain setup
├─ LLM API calls
└─ Chat endpoint

Week 9-10: Frontend
├─ React + Vite app setup
├─ shadcn/ui + Tailwind setup
├─ Admin upload UI
├─ Chat interface with AI SDK
└─ Document list

Week 11-12: Testing & Polish
├─ Unit tests
├─ Integration tests
├─ Security audit
└─ Performance tuning
```

---

## Common Questions & Answers

### Q: Why FAISS and not just database search?

**A**: FAISS is 1000x faster for similarity. Database `LIKE` query finds "holiday" but misses "time off". FAISS finds "PTO policy" even when asked "what's my vacation allowance?"

### Q: Why not just use ChatGPT directly without embeddings?

**A**: Cost + hallucination risk. Without context, LLM makes up answers. With embedded docs, it only answers from company documents (no hallucinations).

### Q: How big can documents be?

**A**: 50MB limit (MVP). A 500-page PDF = ~2 million tokens = takes ~30 seconds to process.

### Q: What if two employees ask same question?

**A**: Good! FAISS caches embeddings. Same embedding = instant search. No redundant work.

### Q: When do I need PostgreSQL?

**A**: When > 1000 concurrent users OR running multiple API servers. For MVP (50 users), SQLite is fine.

### Q: Can I switch LLMs easily?

**A**: Yes! LangChain abstraction. Change 1 line:

```python
# Current
llm = OpenAI(api_key=key)

# To open-source
llm = HuggingFaceHub(repo_id="meta-llama/Llama-2-7b")
```

### Q: What should I use on the frontend for RAG chat UI?

**A**: Use React with Vite, Tailwind, and shadcn/ui for the application UI, and use Vercel AI SDK for chat state and streaming. Keep LangChain in the backend because retrieval and authorization logic must stay server-side.

### Q: What if document processing fails?

**A**: Status marked as "failed". Admin notified. Can re-upload. Graceful error handling throughout.

---

## Testing Checklist

Before launch, verify:

```
✓ Login works with JWT
✓ Admin can upload PDF/DOCX/TXT
✓ Document processing completes
✓ User can only see allowed documents
✓ Search returns relevant chunks
✓ LLM generates sensible answers
✓ Chat history saves correctly
✓ Can filter by department
✓ Rate limiting prevents abuse
✓ Errors logged properly
✓ Load test: 50+ concurrent users
✓ Response times < 3 seconds
✓ No data leakage between roles
```

---

## Performance Targets

| Metric           | Target  | How to Measure           |
| ---------------- | ------- | ------------------------ |
| Upload Response  | < 2s    | Time to get confirmation |
| Processing       | < 2 min | 100-page PDF             |
| Search Latency   | < 100ms | FAISS query time         |
| Chat Response    | < 3s    | LLM API time             |
| Concurrent Users | 50+     | Load test                |
| API Uptime       | 99%+    | Monitoring dashboard     |

---

## Deployment Readiness Checklist

```
Pre-Deployment:
├─ [ ] All tests passing
├─ [ ] .env configured correctly
├─ [ ] Database initialized
├─ [ ] CORS configured
├─ [ ] HTTPS ready
├─ [ ] Logging enabled
├─ [ ] Backups scheduled
└─ [ ] Admin account created

Post-Deployment:
├─ [ ] Health check endpoint working
├─ [ ] API docs available
├─ [ ] Frontend accessible
├─ [ ] Start test uploads
├─ [ ] Monitor error rates
├─ [ ] Check performance metrics
└─ [ ] Demo prepared
```

---

## Architecture Example Queries

### How does role-based access work?

1. User logs in → Gets JWT with `role: "HR_User"`
2. When asking question → Token middleware extracts role
3. User can only search documents with `allowed_roles = ["HR_User"]`
4. If user queries "Show me Finance docs" → Returns 403 (Forbidden)

### How does embedding search work?

```python
# Document processing
"Our PTO policy gives 20 days"
  → Generate 384-dimensional vector
  → Store in FAISS with chunk_id

# User query
"How many vacation days?"
  → Generate embedding (same model)
  → Search FAISS for similar vectors
  → Returns chunk about PTO
  → Pass to LLM for final answer
```

### Why async document processing?

Without: User waits 2 minutes for upload to complete (bad UX)
With: User gets confirmation instantly, processing in background (good UX)

### What if LLM API is down?

Current: Chat fails (tell user to try later)
Future: Queue requests, retry automatically

---

## Troubleshooting Scenarios

| Problem                         | Solution                                             |
| ------------------------------- | ---------------------------------------------------- |
| Search returns old docs         | Rebuild FAISS index: `python scripts/build_index.py` |
| User can see wrong docs         | Check `allowed_roles` in documents table             |
| LLM responses are hallucinating | Ensure context is being passed (check logs)          |
| Upload takes forever            | Check file size (limit 50MB), check server logs      |
| Search is slow                  | FAISS index might be corrupted, rebuild it           |
| JWT token expired               | Frontend should request new `access_token`           |

---

## Environment Setup (Copy-Paste)

```bash
# 1. Create venv
python -m venv venv
source venv/bin/activate

# 2. Install packages
pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib bcrypt \
  PyPDF2 python-docx sentence-transformers faiss-cpu langchain openai

# 3. Create .env
cat > .env << EOF
JWT_SECRET=your-super-secret-key-here
DATABASE_URL=sqlite:///./knowledge_assistant.db
OPENAI_API_KEY=sk-your-key-here
DEBUG=True
EOF

# 4. Run
python -m uvicorn backend.main:app --reload

# 5. Visit
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

---

## Next Steps After MVP

1. **User Feedback**: Deploy, let 10 employees use it for 1 week
2. **Metrics**: Track which documents are searched most, what questions fail
3. **Improvements**: Add features based on real usage patterns
4. **Scale**: If successful, move to PostgreSQL + multi-server setup
5. **Polish**: Add analytics, better UI, more features

---

## Key Contacts for Decisions

- **LLM Choice**: Verify OpenAI budget vs. open-source self-hosted
- **Embedding Model**: Test `all-MiniLM-L6-v2` vs `all-mpnet-base-v2` for quality
- **File Storage**: Local disk ok for MVP, but plan for NAS/cloud later
- **Rate Limiting**: Decide on limits per user (100 queries/day?)
- **Chat History**: How long to retain? (recommend 1 year for MVP)

---

## Success Metrics for Phase 1

```
✓ System demo-ready in 1 month
✓ Can handle 50 concurrent users
✓ Document processing < 2 minutes
✓ Chat responses < 3 seconds
✓ Search accuracy > 80% (manual testing)
✓ Zero data leakage between roles
✓ Admin can upload and manage documents
✓ Employees can ask and get answers
✓ All endpoints documented
✓ Error handling graceful throughout
```

This completes your comprehensive system design! All three documents are now available in your Desktop/AI folder.
