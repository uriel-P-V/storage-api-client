"""
storage_client.py
-----------------
HTTP client for interacting with a storage management API.
This is the System Under Test (SUT) for mock-based tests.
"""

import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError


class StorageAPIError(Exception):
    """Raised when the storage API returns an error."""
    pass


class StorageClient:
    """
    Client for the IBM Storage Management API.
    Handles authentication, retries, and error mapping.
    """

    def __init__(self, base_url: str, api_key: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "X-API-Key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def get_volumes(self) -> list:
        """Fetch all storage volumes."""
        response = self._session.get(
            f"{self.base_url}/volumes",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def get_volume(self, volume_id: str) -> dict:
        """Fetch a specific volume by ID."""
        if not volume_id:
            raise ValueError("volume_id cannot be empty")
        response = self._session.get(
            f"{self.base_url}/volumes/{volume_id}",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def create_volume(self, name: str, size_gb: int) -> dict:
        """Create a new storage volume."""
        if not name or size_gb <= 0:
            raise ValueError("name required and size_gb must be positive")
        response = self._session.post(
            f"{self.base_url}/volumes",
            json={"name": name, "size_gb": size_gb},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def delete_volume(self, volume_id: str) -> bool:
        """Delete a storage volume."""
        response = self._session.delete(
            f"{self.base_url}/volumes/{volume_id}",
            timeout=self.timeout
        )
        response.raise_for_status()
        return True

    def get_health(self) -> dict:
        """Check API health status."""
        try:
            response = self._session.get(
                f"{self.base_url}/health",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Timeout:
            raise StorageAPIError("Health check timed out")
        except ConnectionError:
            raise StorageAPIError("Cannot connect to storage API")
        except HTTPError as e:
            raise StorageAPIError(f"API error: {e}")