# tests/conftest.py
import pytest

@pytest.fixture(autouse=True)
def mock_llm_environment(monkeypatch):
    """Set fake LLM env vars for every test and restore them afterwards."""
    monkeypatch.setenv("MODEL_NAME", "gemini-3.5-flash-lite")
    monkeypatch.setenv("GEMINI_API_KEY", "mock-api-key")
    # Αν το GOOGLE_API_KEY είναι ορισμένο στο CI, το SDK μπορεί να μπερδευτεί.
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)