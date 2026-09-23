from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# /chat requires a populated vector store and at least one valid API key,
# so it's best exercised manually or in an integration test with real keys:
#
# def test_chat():
#     response = client.post("/chat", json={"query": "What is Docker?"})
#     assert response.status_code == 200
#     assert "answer" in response.json()
