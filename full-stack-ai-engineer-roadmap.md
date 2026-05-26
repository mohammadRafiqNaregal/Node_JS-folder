# Full Stack AI Engineer — Transition Roadmap (16 Weeks)

> **Starting point:** Frontend developer (React, Next.js, Node.js, TypeScript, AWS basics)
> **Target:** Full Stack AI Engineer building production-grade LLM-powered applications in Python

---

## Phase 0 — Python Foundations & Environment Setup (Weeks 1–2)

**Goal:** Get production-comfortable with Python, since the AI ecosystem is Python-first.

### Week 1: Core Python

- [ ] Python syntax, data structures (lists, dicts, sets, tuples, comprehensions)
- [ ] Functions, decorators, generators, context managers
- [ ] Type hints and `typing` module (you'll appreciate this coming from TypeScript)
- [ ] Virtual environments (`venv`, `pyenv`) and dependency management (`pip`, `poetry`, `uv`)
- [ ] File I/O, JSON handling, error handling
- [ ] **Project:** Build a CLI tool that reads a CSV/JSON, transforms data, and outputs results

### Week 2: Python Ecosystem for Backend

- [ ] FastAPI fundamentals — routes, Pydantic models, dependency injection, async/await
- [ ] Comparison with Express.js (you'll find FastAPI very similar conceptually)
- [ ] Environment variables, config management (`python-dotenv`, `pydantic-settings`)
- [ ] HTTP clients: `httpx`, `requests`
- [ ] Testing with `pytest`
- [ ] **Project:** Build a REST API with FastAPI that mirrors something you've built in Express

### Resources

- [Python for JavaScript Developers](https://www.valentinog.com/blog/python-for-js/) (mental model mapping)
- [FastAPI official tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Real Python](https://realpython.com/) for deep dives

---

## Phase 1 — AI/ML Foundations & LLM Basics (Weeks 3–5)

**Goal:** Understand how LLMs work, how to call them, and core prompting patterns.

### Week 3: AI/ML Concepts (Breadth, Not Depth)

- [ ] What are embeddings, tokens, transformers, attention (conceptual, not math-heavy)
- [ ] Supervised vs unsupervised vs reinforcement learning (high-level)
- [ ] What is fine-tuning vs prompting vs RAG
- [ ] How LLMs are trained, inference, and why context windows matter
- [ ] Cost/latency tradeoffs: model size, quantization, batching
- [ ] **Deliverable:** Write a 1-page summary explaining LLM architecture to a frontend dev

### Week 4: Working with LLM APIs

- [ ] OpenAI API — chat completions, system/user/assistant roles, streaming
- [ ] Anthropic API — messages API, system prompts, tool use
- [ ] Prompt engineering: zero-shot, few-shot, chain-of-thought, structured output
- [ ] Token counting, cost estimation, rate limiting
- [ ] Handling API errors, retries, fallbacks
- [ ] **Project:** Build a multi-model chat interface (CLI or simple web app) that can switch between OpenAI and Anthropic

### Week 5: Prompt Engineering & Structured Output

- [ ] Output parsing: JSON mode, function calling, tool use
- [ ] Prompt templating and management
- [ ] Evaluation basics — how to measure prompt quality
- [ ] Guardrails and content filtering
- [ ] **Project:** Build a structured data extractor — given unstructured text (e.g., job posting, recipe), extract structured JSON using LLM + validation with Pydantic

### Resources

- [Andrej Karpathy — Intro to LLMs (YouTube)](https://www.youtube.com/watch?v=zjkBMFhNj_g)
- [OpenAI Cookbook](https://cookbook.openai.com/)
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

---

## Phase 2 — RAG Pipelines & Vector Databases (Weeks 6–8)

**Goal:** Build retrieval-augmented generation systems — the #1 production pattern for AI apps.

### Week 6: Embeddings & Vector Databases

- [ ] What are vector embeddings and why they matter
- [ ] Embedding models: OpenAI `text-embedding-3-small/large`, open-source (sentence-transformers)
- [ ] Vector databases: Pinecone (managed), pgvector (PostgreSQL extension), Weaviate, Chroma (local dev)
- [ ] Similarity search: cosine similarity, approximate nearest neighbors
- [ ] Indexing strategies, metadata filtering, namespaces
- [ ] **Project:** Build a semantic search engine over a document corpus using Pinecone or pgvector

### Week 7: RAG Pipeline Architecture

- [ ] Document loading: PDFs, web pages, markdown, databases (LangChain/LlamaIndex loaders)
- [ ] Chunking strategies: fixed-size, recursive, semantic, sentence-based
- [ ] Retrieval strategies: naive, hybrid (keyword + semantic), re-ranking
- [ ] Context window management and stuffing
- [ ] Evaluation: retrieval quality (precision/recall), answer quality (faithfulness, relevance)
- [ ] **Project:** Build a "Chat with your docs" app — upload PDFs, chunk, embed, retrieve, answer

### Week 8: Advanced RAG

- [ ] Hybrid search (BM25 + vector), re-ranking with Cohere or cross-encoders
- [ ] Query transformation: HyDE, multi-query, step-back prompting
- [ ] Parent-child chunking, metadata enrichment
- [ ] Caching strategies for embeddings and responses
- [ ] **Project:** Enhance your Week 7 project with hybrid search, re-ranking, and a FastAPI backend with a React/Next.js frontend

### Resources

- [LlamaIndex docs (RAG-focused)](https://docs.llamaindex.ai/)
- [LangChain RAG tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [Pinecone Learning Center](https://www.pinecone.io/learn/)

---

## Phase 3 — Frameworks & Agentic Workflows (Weeks 9–11)

**Goal:** Build autonomous AI agents that use tools, reason, and complete multi-step tasks.

### Week 9: LangChain & LlamaIndex Deep Dive

- [ ] LangChain: chains, LCEL (LangChain Expression Language), callbacks, memory
- [ ] LlamaIndex: indices, query engines, response synthesizers
- [ ] When to use LangChain vs LlamaIndex vs going framework-free
- [ ] Observability: LangSmith, LangFuse for tracing and debugging
- [ ] **Project:** Rebuild your RAG app using both LangChain and LlamaIndex — compare

### Week 10: Agentic AI — Tool Use & Reasoning

- [ ] What are AI agents: ReAct pattern, planning, tool use
- [ ] OpenAI function calling / Anthropic tool use as agent primitives
- [ ] Building custom tools (API calls, database queries, web scraping, code execution)
- [ ] Agent memory: conversation history, short-term vs long-term
- [ ] Multi-agent systems: delegation, supervisor patterns
- [ ] **Project:** Build a research agent that can search the web, read pages, and write a summary report

### Week 11: Production Agentic Patterns

- [ ] Agent orchestration frameworks: LangGraph, CrewAI, AutoGen
- [ ] State machines for agent workflows (LangGraph is key here)
- [ ] Human-in-the-loop patterns
- [ ] Error handling, timeouts, cost caps for agents
- [ ] Streaming agent responses to frontend
- [ ] **Project:** Build a multi-step workflow agent using LangGraph (e.g., content pipeline: research → outline → draft → review → publish)

### Resources

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)
- [Anthropic's guide to tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Building Effective Agents — Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
- [DeepLearning.AI short courses](https://www.deeplearning.ai/short-courses/) (free, many on agents)

---

## Phase 4 — Data Pipelines & Infrastructure (Weeks 12–14)

**Goal:** Handle data ingestion, transformation, and orchestration at scale.

### Week 12: Data Processing

- [ ] Pandas basics for data manipulation
- [ ] Data ingestion patterns: APIs, web scraping (`BeautifulSoup`, `Scrapy`), file processing
- [ ] Data cleaning, transformation, normalization
- [ ] Feature engineering for AI applications
- [ ] Streaming data with async Python
- [ ] **Project:** Build an ingestion pipeline that scrapes data sources, cleans, and loads into a database

### Week 13: Workflow Orchestration

- [ ] Apache Airflow or Prefect — DAGs, tasks, scheduling, retries
- [ ] Orchestrating RAG refresh pipelines (re-embed on new data)
- [ ] Batch processing vs real-time processing
- [ ] Monitoring and alerting for data pipelines
- [ ] **Project:** Build an Airflow/Prefect DAG that: ingests data → transforms → embeds → upserts to vector DB on a schedule

### Week 14: Deployment & Infrastructure

- [ ] Docker for AI apps (multi-stage builds, GPU support)
- [ ] Kubernetes basics for scaling (Deployments, Services, HPA)
- [ ] AWS: Lambda for serverless inference, ECS/EKS for containers, SageMaker basics
- [ ] GCP: Cloud Run, Vertex AI basics
- [ ] CI/CD for AI apps (model versioning, prompt versioning)
- [ ] Cost optimization: caching, model routing, tiered inference
- [ ] **Project:** Dockerize and deploy your RAG application on AWS ECS or GCP Cloud Run with CI/CD

### Resources

- [Prefect docs](https://docs.prefect.io/)
- [Airflow tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html)
- [Docker for ML — Made With ML](https://madewithml.com/)

---

## Phase 5 — Production Hardening & Portfolio (Weeks 15–16)

**Goal:** Ship a polished, production-grade AI application and build your portfolio.

### Week 15: Production Concerns

- [ ] Inference optimization: caching (Redis/semantic cache), model routing, streaming
- [ ] Observability: structured logging, tracing (OpenTelemetry), metrics (Prometheus/Grafana)
- [ ] Security: API key management, input sanitization, prompt injection defense
- [ ] Rate limiting, usage tracking, cost dashboards
- [ ] A/B testing prompts and models
- [ ] Load testing AI endpoints (handling latency variance)

### Week 16: Capstone Project & Portfolio

- [ ] Build ONE impressive end-to-end project that demonstrates everything:
  - Full-stack app (Next.js frontend + FastAPI backend)
  - RAG pipeline with vector database
  - Agentic workflow with tool use
  - Data ingestion pipeline
  - Deployed on cloud with Docker
  - Observability and monitoring
  - Clean README, architecture diagram, demo video
- [ ] Polish 2–3 best projects from earlier phases for GitHub
- [ ] Update resume and LinkedIn with AI engineering skills
- [ ] Write 2–3 blog posts or technical deep-dives on what you built

---

## Capstone Project Ideas

| Project                            | What It Demonstrates                                                                       |
| ---------------------------------- | ------------------------------------------------------------------------------------------ |
| **AI-Powered Support Agent**       | RAG over product docs + agentic ticket routing + escalation workflow + analytics dashboard |
| **Research & Report Generator**    | Multi-agent research pipeline + web scraping + document generation + scheduled updates     |
| **AI Code Review Assistant**       | GitHub integration + code analysis agents + RAG over style guides + PR comment automation  |
| **Intelligent Document Processor** | PDF/image ingestion + OCR + structured extraction + search + data pipeline                 |

---

## Weekly Schedule Template

| Day                | Focus                                   | Hours       |
| ------------------ | --------------------------------------- | ----------- |
| Mon–Fri (weekdays) | Learn concepts + hands-on coding        | 2–3 hrs/day |
| Saturday           | Project work (build, integrate, deploy) | 4–6 hrs     |
| Sunday             | Review, write notes, plan next week     | 1–2 hrs     |

**Total: ~18–23 hrs/week → 288–368 hrs over 16 weeks**

---

## Tools & Accounts to Set Up (Week 0)

- [ ] Python 3.11+ via `pyenv`
- [ ] `uv` or `poetry` for package management
- [ ] VS Code with Python + Pylance + Ruff extensions
- [ ] OpenAI API key ($5–20/month budget)
- [ ] Anthropic API key
- [ ] Pinecone free tier account
- [ ] Docker Desktop
- [ ] AWS free tier or GCP free tier
- [ ] GitHub repo for each project
- [ ] LangSmith account (free tier for tracing)

---

## Key Principles for Your Transition

1. **Leverage your frontend skills** — You already know React/Next.js. Every AI app needs a frontend. Build full-stack demos, not just notebooks.

2. **Build > Study** — Spend 30% reading/watching, 70% building. Every week has a project for a reason.

3. **Don't go deep on ML math** — You're becoming an AI _engineer_, not a researcher. Understand concepts well enough to make architecture decisions, but focus on building systems.

4. **TypeScript → Python is easier than you think** — Both have type systems, async/await, package managers, and testing frameworks. FastAPI ≈ Express. Pydantic ≈ Zod.

5. **Production > Prototype** — Always add error handling, logging, deployment, and a clean API. This is what separates AI engineers from prompt hobbyists.

6. **Stay current** — The AI space moves fast. Follow Simon Willison's blog, Latent Space podcast, and the LangChain/LlamaIndex changelogs weekly.

---

## Communities & Learning

- **Latent Space podcast** — AI engineering deep dives
- **AI Engineer Foundation** — Community for AI engineers
- **r/LocalLLaMA**, **r/MachineLearning** — Reddit communities
- **Hugging Face Discord** — Open-source AI community
- **DeepLearning.AI short courses** — Free, high-quality, many by Andrew Ng
- **Full Stack Deep Learning** — Production ML course (free)

---

_Last updated: 29 April 2026_
