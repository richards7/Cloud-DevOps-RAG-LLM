# Get Shit Done (GSD)

## Completed
- Backend scaffold and setup (FastAPI, Chroma, LLM Router)
- Python environment created and dependencies fixed (Python 3.14 compatibility)
- API keys added to `.env` (Gemini)
- Data ingestion run successfully (`vectorstore` populated)
- Local backend tested and verified via `curl` (`/chat` and `/health`)
- Logs written to `chat_logs.db` successfully
- Docker container built and tested successfully
- Frontend static files mounted at root (`/`) via `StaticFiles` in `app/main.py`
- Fixed `StaticFiles` `directory` argument to use an absolute path (`os.path.abspath`) instead of a relative path to resolve `{"detail": "Not Found"}` errors when uvicorn is run from different directories.
- Committed frontend wiring (`git commit -m "Wire up frontend static files to FastAPI app"`)

## In Progress
- Test frontend interactivity (chat, suggestions, API status) in the browser
- Test responsive layout on narrow width

## To Do
- Commit frontend wiring changes
- Optional: demo questions, architecture explanation, github repo push
- Clarify file structure change for "data cl444..."
