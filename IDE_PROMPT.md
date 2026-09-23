# Prompt to paste into Antigravity (Gemini Pro / Claude)

Paste this as your first message to the coding agent, after opening
the unzipped `cloud-rag-assistant/` folder as the workspace.

---

```
I'm building a project tonight and need it working end-to-end by the
end of the evening. Before doing anything else, read PROJECT_BRIEF.md
in the root of this workspace completely — it explains what this
project is, why it's structured this way, and what must not be changed.

The codebase is already scaffolded with working (but unverified) code:
FastAPI app, a Chroma-based RAG pipeline, a multip-provider LLM router
(Gemini + OpenAI with fallback), SQLite logging, a Dockerfile, and a
knowledge base of cloud/DevOps markdown docs in data/raw/.

Your job right now:

1. Read PROJECT_BRIEF.md and README.md fully.
2. Set up a Python virtual environment and install requirements.txt.
3. Help me create my .env file from .env.example — I'll provide my
   Gemini and OpenAI API keys when you ask for them (see
   API_SETUP_GUIDE.md if you need to explain how I get them).
4. Run scripts/ingest.py and fix any errors until it completes
   successfully and populates the vectorstore/ folder.
5. Start the FastAPI app (uvicorn app.main:app --reload --port 8080)
   and fix any startup errors.
6. Test the /chat endpoint with 2-3 real questions about Docker,
   GCP vs AWS, and REST APIs — show me the responses and confirm the
   "provider" field and "sources" look correct.
7. Confirm chat_logs.db is being written to after each call.
8. Build and run the Docker image, confirm it behaves the same as
   running locally.
9. Only if time allows: walk me through deploying this to Google
   Cloud Run using the gcloud commands in README.md.

Go step by step, run things for real (don't just describe what should
happen), and fix errors as they come up rather than asking me to fix
them. Tell me clearly at each step whether it succeeded before moving
to the next one. If you hit a genuine blocker that needs a decision
from me (not just a bug to fix), stop and ask — otherwise keep going.
```

---

## After the agent finishes

Ask it to also do these, if time is left:
- "Write 5 sample questions I can ask in the live demo that will get
  good answers from the current knowledge base."
- "Give me a 90-second explanation of this architecture I can say out
  loud in the interview."
- "Push this to a new GitHub repo called cloud-rag-assistant with a
  clean commit history and the README as the repo description."
