import pytest

@pytest.fixture(autouse=True)
def mock_llm_environment(monkeypatch):
    """Mock Model name, gemini api key and google api key"""
    monkeypatch.setenv("MODEL_NAME", "test-gemini-model")
    monkeypatch.setenv("GEMINI_API_KEY", "mock-api-key")
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)