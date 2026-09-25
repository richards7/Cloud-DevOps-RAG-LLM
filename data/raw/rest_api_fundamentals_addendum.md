# REST API Fundamentals — Additional Common Errors & Fixes
(Supplements rest_api_fundamentals.md already in the knowledge base.)

- **CORS errors in the browser console**: the backend doesn't include the right
  `Access-Control-Allow-Origin` header for the requesting origin — this is a browser
  security feature, not visible when calling the same API from `curl` or a server.
- **422 Unprocessable Entity (common in FastAPI)**: the request body doesn't match the
  Pydantic model's expected schema — check field names/types match exactly.
- **API works with Postman but not from the frontend**: often a CORS issue (see
  above), or the frontend is sending a different `Content-Type` header than the
  backend expects.
