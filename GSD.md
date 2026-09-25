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
- Removed all OpenAI fallback code, config, and UI elements to exclusively use Gemini.
- Bound FastAPI server to `0.0.0.0` and moved it to **port 8081** to bypass port collision with the old Docker container on port 8080.
- Decoupled the frontend from the backend FastAPI app by removing `StaticFiles` and adding CORS middleware.
- Built a multi-container architecture for Docker Compose: created a separate Nginx frontend image (`frontend/Dockerfile`) that serves the static UI and proxies `/chat` and `/health` to the FastAPI backend image, sharing a bridged network and preserving volume bind mounts.

## In Progress
- Verify frontend functionality manually via `http://localhost:8081/index.html` from the host browser.

## To Do
- Commit frontend wiring changes
- Optional: demo questions, architecture explanation, github repo push
- Clarify file structure change for "data cl444..."
