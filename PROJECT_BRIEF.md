# Project Brief — Cloud & DevOps RAG Assistant
(Read this in full before making any changes. This is the source of
truth for what the project is and why it's built this way.)

## Who this is for
Richard, a final-year CS student specializing in Cloud/DevOps, is
building this project the same day as a technical exam and interview
for an "AI & ML Engineer (Level 1)" fresher role at a Google Cloud
Premier Partner company. The role wants: Python, REST APIs, basic
ML/LLM/RAG knowledge, Docker, and cloud-native deployment on Google
Cloud — with the JD explicitly saying they are NOT looking for deep
AI framework expertise, but strong fundamentals and the ability to
learn.

## What this project is
A backend API (no frontend needed) that:
1. Answers questions about cloud computing and DevOps topics.
2. Answers ONLY using its own knowledge base (Retrieval-Augmented
   Generation), not the LLM's general knowledge — this is the whole
   point of RAG and should be preserved.
3. Calls one of several LLM provider APIs (Gemini first, OpenAI as
   fallback) to generate the final answer, demonstrating "connecting
   APIs of different LLMs" from the job description.
4. Logs every interaction to a database, separate from the knowledge
   base itself.

## Why it's built this way (do not simplify away these decisions)
- **Provider abstraction (`app/llm/base.py` + `router.py`)**: this is
  intentional and should be preserved even if you add more providers.
  It's a direct, explainable example of the abstraction/polymorphism
  OOP pillars, and it's meant to come up in the interview.
- **Two separate storage layers**:
  - `data/raw/` + `vectorstore/` = the knowledge base (what the bot
    knows). Adding a new `.md` file here and re-running
    `scripts/ingest.py` is how you expand its knowledge.
  - `chat_logs.db` = operational logs (what was asked, by whom, which
    provider answered, how long it took). This is NOT the knowledge
    base and should never be fed back into it automatically.
- **Local embeddings (Chroma's default ONNX model)**: chosen instead
  of an embedding API so the project has one less external dependency
  and works even if an LLM API key is temporarily invalid.
- **FastAPI, not Flask**: chosen for automatic request validation
  (Pydantic), automatic docs at `/docs`, and async support — all
  relevant to the JD's "REST API fundamentals" and "FastAPI or Flask"
  requirement.

## What "done" looks like tonight
1. `python scripts/ingest.py` runs cleanly and populates `vectorstore/`.
2. `uvicorn app.main:app --reload` starts without errors.
3. `POST /chat` with a cloud/DevOps question returns a relevant answer,
   the correct source filenames, which provider answered, and latency.
4. `chat_logs.db` contains a row after each `/chat` call.
5. The app runs in Docker via `docker build` + `docker run` (or
   `docker-compose up`) and behaves the same as running locally.
6. (Stretch, if time allows) Deployed to Google Cloud Run and reachable
   over a public URL.

## What NOT to change without asking
- Don't remove the provider fallback logic to "simplify" it — the
  fallback IS the feature.
- Don't merge `data/` and `chat_logs.db` into one store.
- Don't swap FastAPI for Flask.
- Don't hardcode API keys anywhere — they must only come from `.env`
  (local) or environment variables / Secret Manager (deployed).

## Known constraints
- Time-boxed to one evening. Prioritize: ingestion working → chat
  endpoint working → logging working → Docker working → deploy
  (in that priority order). If time runs out, a working local demo
  (steps 1-4 above) is enough for the interview; Cloud Run deployment
  is a bonus, not a blocker.
- Keep dependencies minimal — every new package added is one more
  thing that can fail to install tonight.
