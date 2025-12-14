"""
Pytest configuration and fixtures
"""
import pytest
import os
from unittest.mock import patch


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Set up test environment variables"""
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test_alpha_key")


@pytest.fixture
def mock_requests():
    """Mock requests library"""
    with patch('requests.get') as mock_get:
        yield mock_get






