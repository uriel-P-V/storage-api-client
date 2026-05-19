import pytest
from unittest.mock import patch, MagicMock, call
from requests.exceptions import Timeout, ConnectionError, HTTPError
from client import StorageClient, StorageAPIError


def test_get_health_timeout_raises_storage_error(client):
    """Verifica que Timeout se convierte en StorageAPIError."""
    with patch.object(client, "_session") as mock_session:
        mock_session.get.side_effect = Timeout()
        with pytest.raises(StorageAPIError) as exc:
            client.get_health()
        assert "timed out" in str(exc.value).lower()


def test_get_health_connection_error(client):
    """Verifica que ConnectionError se convierte en StorageAPIError."""
    with patch.object(client, "_session") as mock_session:
        mock_session.get.side_effect = ConnectionError()
        with pytest.raises(StorageAPIError) as exc:
            client.get_health()
        assert "connect" in str(exc.value).lower()


def test_create_volume_called_with_correct_params(client, mock_response):
    """Verifica que create_volume llama la API con los datos correctos."""
    created = {"id": "vol-010", "name": "test-vol", "size_gb": 50}
    with patch.object(client, "_session") as mock_session:
        mock_session.post.return_value = mock_response(created)
        client.create_volume("test-vol", 50)

        # Verifica que se llamó con los parámetros correctos
        mock_session.post.assert_called_once_with(
            "https://fake-storage-api.com/volumes",
            json={"name": "test-vol", "size_gb": 50},
            timeout=10
        )


def test_get_volumes_calls_correct_url(client, mock_response):
    """Verifica que get_volumes llama la URL correcta."""
    with patch.object(client, "_session") as mock_session:
        mock_session.get.return_value = mock_response([])
        client.get_volumes()

        mock_session.get.assert_called_once_with(
            "https://fake-storage-api.com/volumes",
            timeout=10
        )


def test_delete_calls_correct_url(client, mock_response):
    """Verifica que delete llama la URL con el ID correcto."""
    with patch.object(client, "_session") as mock_session:
        mock_session.delete.return_value = mock_response({})
        client.delete_volume("vol-001")

        mock_session.delete.assert_called_once_with(
            "https://fake-storage-api.com/volumes/vol-001",
            timeout=10
        )


def test_api_key_sent_in_headers(client):
    """Verifica que el API key está en los headers de la sesión."""
    assert "X-API-Key" in client._session.headers
    assert client._session.headers["X-API-Key"] == "test-api-key-123"