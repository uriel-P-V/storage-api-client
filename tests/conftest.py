import pytest
from unittest.mock import MagicMock, patch
from client import StorageClient


@pytest.fixture
def client():
    """StorageClient with mocked session."""
    c = StorageClient(
        base_url="https://fake-storage-api.com",
        api_key="test-api-key-123"
    )
    return c


@pytest.fixture
def mock_response():
    """Factory fixture that creates a fake HTTP response."""
    def _make_response(json_data, status_code=200):
        response = MagicMock()
        response.status_code = status_code
        response.json.return_value = json_data
        response.raise_for_status.return_value = None
        return response
    return _make_response


@pytest.fixture
def sample_volumes():
    """Sample volume data for tests."""
    return [
        {"id": "vol-001", "name": "production", "size_gb": 100, "status": "available"},
        {"id": "vol-002", "name": "backup",     "size_gb": 50,  "status": "available"},
        {"id": "vol-003", "name": "archive",    "size_gb": 200, "status": "available"},
    ]