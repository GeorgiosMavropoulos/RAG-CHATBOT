import os
from unittest.mock import patch

import pytest
import requests
from google.api_core import exceptions as google_exceptions

from llm.llm_client import LLM

# =====================================================================
# FIXTURES
# =====================================================================



@pytest.fixture
def mock_llm_instance():
    """Creates an instance of LLM with the genai.Client mocked out to avoid real API calls."""
    with patch("google.genai.Client") as mock_client_cls:
        # Instantiate the class normally (safely wrapped inside a patch context)
        instance = LLM()
        # Expose the mocked client to our tests so we can configure return values
        instance.mock_client = mock_client_cls.return_value
        yield instance


# =====================================================================
# TESTS FOR __init__ (Initialization Errors)
# =====================================================================

def test_init_missing_model_raises_value_error(monkeypatch):
    """Verify that missing model raises value errors"""
    monkeypatch.delenv("MODEL_NAME", raising=False)
    with pytest.raises(ValueError, match="Model name has not been declared"):
        LLM() 

def test_init_api_call_error_raises_runtime_error():
    """
    Verifies that if google's client throws an API connection error during setup,
    it wraps it cleanly into a RuntimeError.
    """
    with patch("google.genai.Client") as mock_client_cls:
        # Simulate a Google API Core Exception during Client() initialization
        mock_client_cls.side_effect = google_exceptions.GoogleAPICallError("Connection rejected")
        
        with pytest.raises(RuntimeError) as exc_info:
            LLM()
        assert "Failed to connect with the LLM" in str(exc_info.value)


def test_init_unexpected_exception_propagates():
    """
    Verifies that generic system crashes (e.g., MemoryError or OS bugs) 
    bubble up raw instead of getting swallowed.
    """
    with patch("google.genai.Client") as mock_client_cls:
        mock_client_cls.side_effect = Exception("System Crash")
        
        with pytest.raises(Exception) as exc_info:
            LLM()
        assert "System Crash" in str(exc_info.value)


# =====================================================================
# TESTS FOR get_llm (Execution Errors & Success)
# =====================================================================

def test_get_llm_success(mock_llm_instance):
    """
    Verifies the happy path where the API returns a response.
    Validates correct structural arguments passing (model, temperature, text extraction).
    """
    # Setup mock response text matching structure: response.text
    mock_llm_instance.mock_client.models.generate_content.return_value.text = "Hello there!"

    result = mock_llm_instance.get_llm("Hi")

    assert result == "Hello there!"
    
    # Assert parameters passed into generate_content match our configurations exactly
    mock_llm_instance.mock_client.models.generate_content.assert_called_once()
    kwargs = mock_llm_instance.mock_client.models.generate_content.call_args.kwargs
    assert kwargs["model"] == "test-gemini-model"
    assert kwargs["contents"] == "Hi"
    assert kwargs["config"].temperature == 0.2


def test_get_llm_empty_response_raises_runtime_error(mock_llm_instance):
    """
    Verifies that if the API returns None or an empty response payload, 
    a RuntimeError is raised.
    """
    # Simulate API returning None
    mock_llm_instance.mock_client.models.generate_content.return_value = None

    with pytest.raises(RuntimeError) as exc_info:
        mock_llm_instance.get_llm("Test question")
    assert "Error, cannot produce the response" in str(exc_info.value)


def test_get_llm_network_request_exception_raises_runtime_error(mock_llm_instance):
    """
    Verifies that HTTP/Network level drops (requests exceptions) 
    are caught and transformed into a clean "The LLM is unavailable" error.
    """
    # Simulate a network timeout or connection drop
    mock_llm_instance.mock_client.models.generate_content.side_effect = requests.exceptions.RequestException("Timeout")

    with pytest.raises(RuntimeError) as exc_info:
        mock_llm_instance.get_llm("Test question")
    assert "The LLM is unavailable" in str(exc_info.value)


def test_get_llm_generic_exception_raises_runtime_error(mock_llm_instance):
    """
    Verifies that any other unhandled exception inside get_llm 
    is safely packaged into a generic RuntimeError message.
    """
    # Simulate a generic unexpected bug inside the client package
    mock_llm_instance.mock_client.models.generate_content.side_effect = Exception("Unknown API Bug")

    with pytest.raises(RuntimeError) as exc_info:
        mock_llm_instance.get_llm("Test question")
    assert "An unexpected error occurred: Unknown API Bug" in str(exc_info.value)
