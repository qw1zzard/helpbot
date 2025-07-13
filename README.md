# helpbot 🤖

**helpbot** is a Q&A assistant powered by FastAPI, Streamlit, LangChain, and
Ollama. It answers user questions by retrieving the most relevant answer from a
structured knowledge base (CSV file). The chatbot uses a Retrieval-Augmented
Generation (RAG) architecture with persistent session tracking and a modern
GPU-enabled containerized stack.

---

## 🚀 Features

- Chat-based user interface (Streamlit)
- RAG pipeline with LangChain, Ollama, and Chroma
- GPU-accelerated model support via Docker
- Session tracking with SQLite
- Fully configurable via `.env`
- GitHub release automation via `release-please`

---

## 🐳 Quickstart (Docker)

1. **Create `.env`**

Duplicate `.env.example` and fill in the values:

```bash
cp .env.example .env
````

2. **Launch containers**

```bash
docker compose up --build
```

- FastAPI backend: [http://localhost:80](http://localhost:80)
- Streamlit UI: [http://localhost:8501](http://localhost:8501)
- Ollama (model host): [http://localhost:11434](http://localhost:11434)

---

## 🔧 Dependency Management

This project uses [`uv`](https://github.com/astral-sh/uv) for dependency resolution:

```bash
# To upgrade dependencies
uv pip compile --upgrade --extra dev

# To install dependencies locally (optional)
uv pip install --system --no-cache .
```

---

## 🧪 Development Tips

- Dev dependencies: `ruff`, `mypy`
- All RAG logic is defined in `src/model.py`
- Chroma vectorstore uses persistent directory (`./vectorestore`)
- Data source: `data.csv` (Q\&A pairs)

---

## 🛠 Release Automation

GitHub Actions uses [`release-please`](https://github.com/googleapis/release-please) to automatically:

- Bump version
- Update `CHANGELOG.md`
- Create GitHub releases

Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) when committing to enable this.

---

## 📄 License

MIT License
