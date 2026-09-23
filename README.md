# Cloud & DevOps RAG Assistant

A RAG-powered chatbot that answers questions from a cloud/DevOps
knowledge base, with automatic fallback across multiple LLM providers
(Gemini → OpenAI).

## Architecture

```
User query
   |
   v
FastAPI /chat endpoint
   |
   |--> 1. Embed query & retrieve top-k chunks from Chroma vector store
   |--> 2. Build prompt = retrieved context + query
   |--> 3. LLM Router: try Gemini -> on failure -> try OpenAI
   |--> 4. Log query + response + provider + latency to SQLite
   v
Return JSON response
```

- **Knowledge base**: `data/raw/` — Markdown files on Docker, GCP/AWS
  mapping, Kubernetes, CI/CD, REST APIs, and networking/IAM. Drop new
  files here and re-run the ingestion script to expand what the bot
  knows.
- **Vector store**: `vectorstore/` (generated) — persisted Chroma DB
  built from `data/raw/`.
- **Operational database**: `chat_logs.db` (generated) — every chat
  interaction (query, retrieved sources, provider used, response,
  latency) is logged here, separate from the knowledge base.

## Local setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env and add your GEMINI_API_KEY and/or OPENAI_API_KEY

python scripts/ingest.py          # builds the vector store from data/raw/

uvicorn app.main:app --reload --port 8080
```

Visit `http://localhost:8080/docs` for interactive API docs.

## Try it

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the difference between a Docker image and a container?"}'
```

## Run with Docker

```bash
docker build -t cloud-rag-assistant .
docker run -p 8080:8080 --env-file .env cloud-rag-assistant
```

Or with docker-compose:
```bash
docker-compose up --build
```

## Deploy to Google Cloud Run

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/cloud-rag-assistant

gcloud run deploy cloud-rag-assistant \
  --image gcr.io/YOUR_PROJECT_ID/cloud-rag-assistant \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key,OPENAI_API_KEY=your_key
```

For production, prefer Secret Manager over plain `--set-env-vars` for
API keys.

## Adding a third LLM provider

1. Create `app/llm/<provider>_provider.py` implementing `LLMProvider`
   (see `app/llm/base.py`).
2. Register it in `app/llm/router.py`.
3. Add its API key to `.env` and `app/config.py`.

## Project structure

```
cloud-rag-assistant/
├── data/raw/            # knowledge base documents (feeds RAG)
├── app/
│   ├── main.py          # FastAPI app
│   ├── config.py        # settings from .env
│   ├── ingestion/       # loading, chunking, embedding, vector store
│   ├── rag/             # retrieval + prompt building
│   ├── llm/             # provider abstraction, Gemini, OpenAI, router
│   ├── db/               # SQLAlchemy models + session (chat logs)
│   └── schemas.py        # Pydantic request/response models
├── scripts/ingest.py     # builds/rebuilds the vector store
├── tests/                # basic tests
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
