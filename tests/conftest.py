import os
import pytest

@pytest.fixture(autouse=True)
def mock_llm_environment():
    """Automatically mock LLM environment variables for all tests."""
    # Replace 'MODEL_NAME' with the exact env variable your code looks for 
    # (e.g., 'OPENAI_MODEL', 'ANTHROPIC_MODEL', etc.)
    os.environ["MODEL_NAME"] = "gemini-3.5-flash-lite"
    
    # It's also a good idea to mock API keys so tests don't make real web requests
    os.environ["GEMINI_API_KEY"] = "mock-api-key"
    
    yield
    
    # Clean up after tests finish
    if "MODEL_NAME" in os.environ:
        del os.environ["MODEL_NAME"]
