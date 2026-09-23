# Frontend — Cloud & DevOps RAG Assistant

Two pages, plain HTML/CSS/JS (no build step, no framework):

- **`landing.html`** — marketing/overview page explaining the pipeline.
- **`index.html`** — the actual chat interface, calling the FastAPI backend.
- **`style.css`** — shared design tokens and styles for both pages.
- **`script.js`** — chat logic: sends `POST /chat`, renders sources/provider/latency, checks `GET /health`.

## Running it against your backend

By default the frontend calls `http://localhost:8080`. Two ways to run it:

### Option A — open directly (fastest, for local testing)
Just open `frontend/index.html` in a browser while `uvicorn` is running.
You may need to enable CORS on the backend (see below) since the page
is served from `file://` while the API is on `localhost:8080`.

### Option B — serve via FastAPI (recommended, one origin, no CORS needed)
Add this to `app/main.py`:
```python
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
```
Then visit `http://localhost:8080/index.html` and
`http://localhost:8080/landing.html` — same origin as the API, so no
CORS configuration is needed.

### Enabling CORS (only needed for Option A, or a separately hosted frontend)
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten this before sharing publicly
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Pointing at a different backend URL

Set it before `script.js` loads, e.g. in `index.html`:
```html
<script>window.API_BASE = "https://your-cloud-run-url.a.run.app";</script>
<script src="script.js"></script>
```

## Design notes

Dark slate palette with an amber accent, IBM Plex Sans/Mono pairing.
The sidebar lists the actual files in `data/raw/` — update it if you
add or rename knowledge base documents, so the UI matches what the
bot can actually answer from.
