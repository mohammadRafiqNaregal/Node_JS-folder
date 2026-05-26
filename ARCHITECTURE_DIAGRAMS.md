# Architecture Diagrams - Enterprise AI Knowledge Assistant

## 1. System Architecture Diagram

```mermaid
graph TB
    subgraph Frontend["Frontend Layer"]
        UI["Browser UI<br/>(React + shadcn/ui + Tailwind)"]
    end

    subgraph API["FastAPI Backend"]
        GW["API Gateway<br/>(CORS, Rate Limits)"]
        AUTH["Auth Middleware<br/>(JWT Validation)"]
        ROUTES["Route Controllers"]
    end

    subgraph Services["Business Logic Services"]
        USERSVR["User Service<br/>(Register, Login, RBAC)"]
        DOCSVR["Document Service<br/>(Upload, Metadata)"]
        PROCSVR["Processing Service<br/>(Async Jobs)"]
        SVRSEARCH["Search Service<br/>(Vector Retrieval)"]
        CHATSVR["Chat Service<br/>(LLM Orchestration)"]
    end

    subgraph Processing["Document Processing Pipeline"]
        EXTRACT["Text Extraction<br/>(PyPDF2, python-docx)"]
        CHUNK["Chunking<br/>(Semantic Overlap)"]
        EMBED["Embedding Generation<br/>(HuggingFace/OpenAI)"]
    end

    subgraph Storage["Storage & DB"]
        SQLITE["SQLite<br/>(User, Doc, Chat data)"]
        FAISS["FAISS Index<br/>(Vector Search)"]
        FILES["File Storage<br/>(uploads/)"]
    end

    subgraph External["External Services"]
        LLM["LLM API<br/>(OpenAI/HuggingFace)"]
    end

    UI -->|HTTP/REST + JWT| GW
    GW --> AUTH
    AUTH --> ROUTES
    ROUTES --> USERSVR
    ROUTES --> DOCSVR
    ROUTES --> CHATSVR
    ROUTES --> SVRSEARCH

    DOCSVR --> PROCSVR
    PROCSVR --> EXTRACT
    EXTRACT --> CHUNK
    CHUNK --> EMBED
    EMBED --> FAISS
    PROCSVR --> FILES

    USERSVR --> SQLITE
    DOCSVR --> SQLITE
    CHATSVR --> SQLITE
    PROCSVR --> SQLITE
    SVRSEARCH --> FAISS

    CHATSVR --> LLM
    EMBED --> LLM

    style Frontend fill:#e1f5ff
    style API fill:#fff3e0
    style Services fill:#f3e5f5
    style Processing fill:#e8f5e9
    style Storage fill:#fce4ec
    style External fill:#f1f8e9
```

## 2. Authentication Flow

```mermaid
sequenceDiagram
    participant User as User/Browser
    participant API as FastAPI Server
    participant DB as SQLite Database
    participant JWT as JWT Handler

    User->>API: POST /login {username, password}
    API->>DB: Query user by username
    DB-->>API: Return user + hash
    API->>API: Verify password hash

    alt Password matches
        API->>JWT: Create JWT token
        JWT-->>API: Token {user_id, role, exp}
        API-->>User: Return token + user info
        User->>User: Store token in localStorage

        User->>API: GET /documents (Header: Authorization: Bearer {token})
        API->>JWT: Validate token
        JWT-->>API: Valid payload
        API->>DB: Fetch documents user can access
        DB-->>API: Return filtered documents
        API-->>User: Return data
    else
        API-->>User: 401 Unauthorized
    end
```

## 3. Document Upload & Processing Flow

```mermaid
sequenceDiagram
    participant Admin as Admin User
    participant API as FastAPI API
    participant DB as SQLite
    participant QUEUE as Queue/Background
    participant FILE as File Storage
    participant PROCESS as Processing Service
    participant FAISS as FAISS Index

    Admin->>API: POST /documents/upload + file + metadata
    API->>API: Validate auth (must be Admin)
    API->>API: Validate file (type, size)
    API->>FILE: Save file to disk
    API->>DB: Create document record (status: pending)
    DB-->>API: Return document_id
    API->>QUEUE: Queue background job
    API-->>Admin: Return {document_id, status: "processing"}

    QUEUE->>PROCESS: Start process_document job
    PROCESS->>FILE: Read file
    FILE-->>PROCESS: File content
    PROCESS->>PROCESS: Extract text (PyPDF2/python-docx)
    PROCESS->>PROCESS: Split into chunks (overlap strategy)

    loop For each chunk
        PROCESS->>PROCESS: Generate embedding
        PROCESS->>FAISS: Add embedding vector
        PROCESS->>DB: Store chunk metadata
    end

    PROCESS->>DB: Mark document as "processed"
    DB-->>PROCESS: Confirmed

    Admin->>API: GET /documents/{doc_id}/status
    API->>DB: Fetch document status
    DB-->>API: {status: "processed", chunk_count: 50}
    API-->>Admin: Return status
```

## 4. Query & Response Flow

```mermaid
sequenceDiagram
    participant User as User/Chat UI
    participant API as FastAPI API
    participant AUTH as Auth Service
    participant EMBED as Embedding Model
    participant FAISS as FAISS Search
    participant DB as SQLite Database
    participant LLM as LLM API
    participant CHAT as Chat Repository

    User->>API: POST /chat/ask {question, session_id}
    API->>AUTH: Validate JWT token + user role
    AUTH-->>API: Valid user + permissions

    API->>EMBED: Generate embedding for question
    EMBED-->>API: Embedding vector [384 dims]

    API->>FAISS: Search K-nearest (top 10)
    FAISS-->>API: Return indices + distances

    loop For each result
        API->>DB: Fetch chunk + document metadata
        DB-->>API: Chunk content + document info
        API->>API: Check if user can access document
        alt User has permission
            API->>API: Keep result
        else
            API->>API: Filter out
        end
    end

    API->>API: Build prompt with top 5 chunks
    API->>LLM: POST (system_prompt + context + question)
    LLM-->>API: Generated response

    API->>CHAT: Store in chat history
    CHAT->>DB: INSERT chat record
    DB-->>CHAT: Confirmed

    API-->>User: Return {response, documents_used, metadata}
```

## 5. Role-Based Access Control Flow

```mermaid
graph TD
    A["User Login Request"] --> B{"Extract Role"}
    B -->|Admin| C["Can access all documents"]
    B -->|HR User| D["Can access HR documents"]
    B -->|Finance User| E["Can access Finance documents"]
    B -->|IT User| F["Can access IT documents"]
    B -->|Employee| G["Can access public documents"]

    C --> H["Query all departments"]
    D --> H
    E --> H
    F --> H
    G --> H

    H --> I["Filter documents by allowed_roles"]
    I --> J["Return accessible documents"]

    K["User asks question"] --> L["Generate embedding"]
    L --> M["Search FAISS index"]
    M --> N["Get results"]
    N --> O{"Check user permission<br/>for each document"}
    O -->|Allowed| P["Include in context"]
    O -->|Denied| Q["Exclude from context"]
    P --> R["Generate LLM response"]
    Q --> R
```

## 6. Database Schema Diagram

```mermaid
erDiagram
    USERS ||--o{ DOCUMENTS : uploads
    USERS ||--o{ CHAT_HISTORY : asks
    USERS ||--o{ ACCESS_LOG : accesses
    DOCUMENTS ||--o{ DOCUMENT_CHUNKS : contains
    DOCUMENTS ||--o{ CHAT_HISTORY : "referenced in"

    USERS {
        string id PK
        string username UK
        string email UK
        string password_hash
        string role "Admin|HR_User|Finance_User|IT_User|Employee"
        string department "HR|Finance|IT|null"
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    DOCUMENTS {
        string id PK
        string title
        string department "HR|Finance|IT"
        string section
        string tags "JSON array"
        string file_path
        string file_name
        int file_size
        string uploaded_by FK
        string allowed_roles "JSON array"
        string status "pending|processing|processed|failed"
        string processing_error
        timestamp created_at
        timestamp updated_at
    }

    DOCUMENT_CHUNKS {
        string id PK
        string document_id FK
        int chunk_index
        string content
        blob embedding_vector
        int embedding_id "FAISS index"
        timestamp created_at
    }

    CHAT_HISTORY {
        string id PK
        string user_id FK
        string session_id
        string question
        string response
        string retrieved_documents "JSON array"
        string feedback "helpful|not_helpful"
        int tokens_used
        int response_time_ms
        timestamp created_at
    }

    ACCESS_LOG {
        string id PK
        string user_id FK
        string document_id FK
        string action "view|download|search"
        timestamp created_at
    }
```

## 7. API Endpoint Hierarchy

```mermaid
graph TD
    API["REST API v1<br/>Base: /api/v1"]

    API --> AUTH["Authentication<br/>/auth"]
    API --> DOC["Documents<br/>/documents"]
    API --> CHAT["Chat<br/>/chat"]
    API --> SEARCH["Search<br/>/search"]
    API --> ADMIN["Admin<br/>/admin"]

    AUTH --> L1["POST /register"]
    AUTH --> L2["POST /login"]
    AUTH --> L3["POST /refresh"]
    AUTH --> L4["GET /me"]
    AUTH --> L5["POST /logout"]

    DOC --> D1["POST /upload"]
    DOC --> D2["GET / (list)"]
    DOC --> D3["GET /{id}"]
    DOC --> D4["DELETE /{id}"]
    DOC --> D5["GET /{id}/status"]

    CHAT --> C1["POST /ask"]
    CHAT --> C2["GET /history"]
    CHAT --> C3["POST /feedback"]
    CHAT --> C4["GET /sessions"]

    SEARCH --> S1["POST / (query)"]

    ADMIN --> A1["GET /users"]
    ADMIN --> A2["GET /stats"]
    ADMIN --> A3["GET /documents/processing"]
```

## 8. Component Dependency Graph

```mermaid
graph LR
    UI["Frontend<br/>React"]

    subgraph Core["Core Components"]
        AUTH_MID["Auth Middleware"]
        RBAC["RBAC Service"]
        REQ_VAL["Request Validator"]
    end

    subgraph Services["Service Layer"]
        USR["User Service"]
        DOC["Document Service"]
        CHAT["Chat Service"]
        SEARCH["Search Service"]
    end

    subgraph Infrastructure["Infrastructure"]
        DB["SQLite ORM"]
        CACHE["Cache Layer"]
        LOG["Logger"]
    end

    subgraph External["External Dependencies"]
        EMBED_API["Embedding API"]
        LLM_API["LLM API"]
        FAISS["FAISS Backend"]
        PARSERS["File Parsers"]
    end

    UI --> AUTH_MID
    AUTH_MID --> RBAC
    AUTH_MID --> REQ_VAL

    RBAC --> USR
    RBAC --> DOC
    RBAC --> CHAT
    RBAC --> SEARCH

    USR --> DB
    DOC --> DB
    CHAT --> DB
    SEARCH --> FAISS

    all["All Services"] -.-> LOG
    all -.-> CACHE

    DOC --> PARSERS
    CHAT --> LLM_API
    SEARCH --> EMBED_API
    SEARCH --> FAISS
```

## 9. Data Flow: Complete Request Lifecycle

```mermaid
graph TD
    A["1. User Request<br/>POST /chat/ask<br/>{question}"] --> B["2. Frontend<br/>Add Bearer token<br/>to headers"]

    B --> C["3. Express to FastAPI<br/>HTTP with Authorization"]

    C --> D["4. API Gateway<br/>Parse request"]

    D --> E["5. Auth Middleware<br/>Extract & validate JWT"]

    E --> F{"6. Token<br/>Valid?"}

    F -->|No| Z["Reject 401"]
    F -->|Yes| G["7. Extract User Info<br/>{user_id, role}"]

    G --> H["8. Request Handler<br/>Start chat/ask"]

    H --> I["9. Generate Embedding<br/>OpenAI/HuggingFace API"]

    I --> J["10. Search FAISS<br/>K-nearest neighbors"]

    J --> K["11. Fetch Chunk Metadata<br/>SQLite query"]

    K --> L["12. Check User Permissions<br/>Against allowed_roles"]

    L --> M["13. Build Context<br/>Combine top chunks"]

    M --> N["14. Call LLM API<br/>Send system + context + question"]

    N --> O["15. LLM Response<br/>Generated text"]

    O --> P["16. Validate Response<br/>Ensure uses context only"]

    P --> Q["17. Store Chat History<br/>INSERT into SQLite"]

    Q --> R["18. Format Response<br/>JSON with metadata"]

    R --> S["19. Send to Client<br/>HTTP 200 + JSON"]

    S --> T["20. Update UI<br/>Display response + sources"]

    Z --> U["Return Error<br/>Client handles"]
```

## 10. Deployment Architecture

```mermaid
graph TB
    subgraph Development["Development Environment"]
        DEV_CODE["Source Code<br/>(Git)"]
        DEV_DB["SQLite<br/>(local.db)"]
        DEV_ENV[".env file<br/>(local secrets)"]
    end

    subgraph Production["Production Server"]
        PROD_API["FastAPI Server<br/>(Uvicorn)"]
        PROD_DB["SQLite<br/>(persistent.db)"]
        PROD_ENV["Environment Variables<br/>(from system)"]
        PROD_FILES["Upload Storage<br/>(uploads/)"]
        PROD_LOGS["Log Files<br/>(logs/)"]
    end

    subgraph External_PROD["External Services"]
        API_LLM["OpenAI API<br/>(live keys)"]
        API_EMBED["Embedding API<br/>(live keys)"]
    end

    DEV_CODE -->|Git Push| PROD_API
    DEV_DB -->|Initialize| PROD_DB
    DEV_ENV -->|Configure| PROD_ENV

    PROD_API --> PROD_DB
    PROD_API --> PROD_ENV
    PROD_API --> PROD_FILES
    PROD_API --> PROD_LOGS

    PROD_API --> API_LLM
    PROD_API --> API_EMBED

    subgraph Monitoring["Monitoring"]
        MON_LOG["Log Aggregation<br/>(Syslog/ELK)"]
        MON_METRIC["Metrics<br/>(Response times, Errors)"]
    end

    PROD_LOG --> MON_LOG
    PROD_API --> MON_METRIC
```

## Key Design Principles

### 1. **Separation of Concerns**

- Each service has a single responsibility
- Clear interfaces between components
- Easy to test and modify independently

### 2. **Security by Design**

- RBAC enforced at every level
- No data leakage between user scopes
- Sensitive APIs require authentication

### 3. **Performance Optimization**

- FAISS index for sub-100ms searches
- Async document processing
- Embedding caching
- Connection pooling for DB

### 4. **Scalability Path**

- Stateless API servers (can be replicated)
- Database abstraction (can migrate to PostgreSQL)
- Background queue design (can use Celery)
- Pluggable LLM/embedding providers

### 5. **Resilience**

- Graceful error handling
- Fallback mechanisms
- Comprehensive logging
- Health check endpoints
