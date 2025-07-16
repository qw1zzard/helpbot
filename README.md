# helpbot 🤖

**helpbot** is a Q&A assistant powered by FastAPI, Streamlit, LangChain, and
Ollama. It retrieves the most relevant answer from a structured knowledge base
using Retrieval-Augmented Generation (RAG). It supports GPU acceleration,
persistent vector storage, and session tracking via PostgreSQL.

## 🚀 Features

- Chat-based UI with Streamlit
- RAG pipeline using LangChain, Ollama, HuggingFace, and Qdrant
- GPU support via Docker (Ollama & Transformers)
- Persistent vector store with Qdrant
- Session tracking with PostgreSQL
- Fully configurable via `.env`
- GitHub release automation via `release-please`

## 🐳 Quickstart (Docker)

1. **Create `.env`**

```bash
cp .env.example .env
````

2. **Start services**

```bash
docker compose up --build
```

Access:

- Streamlit UI: [http://localhost:8501](http://localhost:8501)
- FastAPI backend: [http://localhost:80](http://localhost:80)
- Ollama (model host): [http://localhost:11434](http://localhost:11434)
- Qdrant (vector store): [http://localhost:6333](http://localhost:6333)

## 📚 Load Knowledge Base

To load and convert RuBQ example to CSV format:

```bash
python data/load_rubq.py
```

## 🚀 Release Automation

GitHub Actions uses [`release-please`](https://github.com/googleapis/release-please) to:

- Bump versions
- Update `CHANGELOG.md`
- Create GitHub releases

Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) when committing to enable this.

## 📄 License

MIT License
