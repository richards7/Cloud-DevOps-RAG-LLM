# REST API Fundamentals

REST (Representational State Transfer) is an architectural style for
designing networked APIs, built around resources identified by URLs
and manipulated with standard HTTP methods.

## Core principles
- **Statelessness**: each request contains all the information needed
  to process it; the server doesn't store client session state between
  requests.
- **Client-server separation**: the client and server evolve
  independently, communicating only through the defined interface.
- **Uniform interface**: resources are accessed and manipulated using a
  consistent set of operations (HTTP methods) and representations
  (typically JSON).

## HTTP methods
- `GET` — retrieve a resource (safe, doesn't change data)
- `POST` — create a new resource
- `PUT` — replace a resource entirely
- `PATCH` — partially update a resource
- `DELETE` — remove a resource

## Idempotency
An operation is idempotent if performing it multiple times has the same
effect as performing it once. `GET`, `PUT`, and `DELETE` are idempotent;
`POST` generally is not (calling it twice typically creates two
resources).

## Common status codes
- `200 OK` — success
- `201 Created` — resource created successfully
- `400 Bad Request` — invalid input from the client
- `401 Unauthorized` — missing/invalid authentication
- `403 Forbidden` — authenticated but not permitted
- `404 Not Found` — resource doesn't exist
- `500 Internal Server Error` — unexpected server-side failure

## Authentication
- **API keys**: a static token sent with each request, simple but less
  secure if leaked.
- **Bearer tokens / OAuth 2.0**: a token (often short-lived) proving the
  caller's identity, typically sent in the `Authorization` header.

## FastAPI vs Flask
FastAPI is built on Starlette and Pydantic, giving automatic request
validation, automatic interactive API docs (Swagger UI at `/docs`), and
native async support — all useful for AI APIs that call external LLM
services. Flask is simpler and more minimal, with a larger legacy
ecosystem but fewer built-in features for this kind of work.

## A minimal FastAPI endpoint
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    text: str

@app.post("/predict")
def predict(q: Query):
    return {"result": f"processed: {q.text}"}
```
