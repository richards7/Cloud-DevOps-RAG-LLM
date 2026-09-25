FROM python:3.13-slim

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Build the vector store at image build time from data/raw/.
# (If your API keys or data change often, you can instead run
# scripts/ingest.py at container startup — see README.)
RUN python scripts/ingest.py

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
