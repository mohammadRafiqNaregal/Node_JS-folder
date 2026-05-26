# Node.js to Python Command Cheatsheet

Keep this alongside your roadmap as a quick reference.

## 1. PROJECT INITIALIZATION

### Node (Express)

```bash
npm init -y
npm install express
npm install -D nodemon prettier eslint
npm run dev
```

### Python (FastAPI)

#### Option A: Using uv (RECOMMENDED - most Node-like)

```bash
uv init my-project
cd my-project
uv add fastapi "uvicorn[standard]"
uv add -d black ruff  # dev dependencies
uv run uvicorn main:app --reload
```

#### Option B: Using pip (traditional)

```bash
mkdir my-project && cd my-project
python3.12 -m venv .venv
source .venv/bin/activate
pip install fastapi "uvicorn[standard]"
pip freeze > requirements.txt
uvicorn main:app --reload
```

---

## 2. SIDE-BY-SIDE COMMAND COMPARISON

| Task                  | Node                   | Python (pip)                    | Python (uv)             |
| --------------------- | ---------------------- | ------------------------------- | ----------------------- |
| Create project        | npm init               | Manual venv                     | **uv init**             |
| Install package       | npm install express    | pip install fastapi             | uv add fastapi          |
| Install dev only      | npm install -D nodemon | pip install --upgrade-dev black | uv add -d black         |
| View deps             | npm list               | pip list                        | uv tree                 |
| Lock exact versions   | auto package-lock.json | manual pip freeze               | auto uv.lock            |
| Run command           | npm run dev            | python main.py                  | uv run uvicorn main:app |
| Use without install   | npx nodemon            | pipx nodemon                    | uvx nodemon             |
| Switch Python version | nvm use 18             | pyenv local 3.12                | uv python pin 3.12      |
| Delete project env    | rm node_modules        | rm -rf .venv                    | uv sync --clean         |

---

## 3. FILE STRUCTURE COMPARISON

### Node + Express

```
my-app/
├── node_modules/       (auto-downloaded packages)
├── package.json        (project config + deps)
├── package-lock.json   (exact versions locked)
├── .gitignore
└── index.js           (main app file)
```

### Python + FastAPI (with uv)

```
my-app/
├── .venv/             (auto-created isolated environment)
├── pyproject.toml     (project config + deps)
├── uv.lock            (exact versions locked)
├── .gitignore
└── main.py            (main app file)
```

### Python + FastAPI (traditional pip)

```
my-app/
├── .venv/             (manual isolated venv)
├── requirements.txt   (manual deps list)
└── main.py            (main app file)
```

---

## 4. RUNTIME COMPARISON

| Aspect            | Node              | Python                              |
| ----------------- | ----------------- | ----------------------------------- |
| Version manager   | nvm               | pyenv or uv                         |
| Check version     | node -v           | python --version                    |
| Package manager   | npm               | pip or **uv**                       |
| Lock file manager | npm (automatic)   | pip (manual) or **uv (auto)**       |
| Dev dependencies  | npm install -D    | pip (manual group) or **uv add -d** |
| Virtual isolation | node_modules only | .venv (full isolation)              |

---

## 5. QUICK START (RECOMMENDED PATH FOR YOU)

### FastAPI with uv (most like Express workflow)

```bash
# 1. Install uv (one-time)
brew install uv

# 2. Create project
uv init fastapi-app
cd fastapi-app

# 3. Add dependencies
uv add fastapi "uvicorn[standard]"
uv add -d black ruff  # optional: dev tools

# 4. Create main.py
cat > main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}
EOF

# 5. Run
uv run uvicorn main:app --reload

# 6. Visit http://127.0.0.1:8000
```

---

## 6. DAILY WORKFLOW (after setup)

### Node

```bash
cd my-app
npm run dev
```

### Python with uv

```bash
cd my-app
uv run uvicorn main:app --reload
```

### Python with pip (traditional)

```bash
cd my-app
source .venv/bin/activate
uvicorn main:app --reload
```

---

## 7. WHY NO PYTHON EQUIVALENT TO npm init BY DEFAULT?

**Historical reason:**

- Python predates npm (Python 1991, npm 2010)
- Python had virtualenv, pip much earlier
- No unified "project init" tool was in stdlib
- It was community-fragmented for decades

**Modern tools bridge this gap:**

- uv (2024+) - modern and fast
- Poetry (2018+) - popular in teams
- PDM (2021+) - PEP-standard focused
- Hatch (evolving) - packaging-focused

**pip's role:**

- pip = only package manager (installs pre-made packages)
- NOT a project initializer like npm
- Does not create lock files automatically
- Does not manage virtual environments

---

## 8. INDUSTRY STANDARD (as of 2024-2026)

### Large teams / Production

- **Poetry** or **uv** (both with auto lock files)
- Most common in Django/FastAPI production repos

### Beginners / Simple projects

- **uv** (becoming new standard, extremely fast)
- pip + requirements.txt (simple but manual)

### Data Science / AI

- **pip + venv** (most common still)
- Poetry growing

### What's trending?

- **uv** is taking over (Astral, made Ruff)
- Poetry still dominant for published packages
- pip alone fading (too manual)

---

## 9. RECOMMENDATION FOR YOU NOW

**Start with:** uv

- Most Node-like experience
- Auto lock files (like package-lock.json)
- Handles virtual env automatically
- Fastest package downloads
- Growing industry adoption

**Later (if needed):** Poetry or pip + requirements.txt

- Poetry if you publish packages
- pip if you need absolute simplicity
