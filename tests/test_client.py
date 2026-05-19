from unittest.mock import patch, MagicMock

import pytest
from client import StorageClient


def test_get_volumes_returns_list(client, mock_response, sample_volumes):
    with patch.object(client, "_session") as mock_session:
        mock_session.get.return_value = mock_response(sample_volumes)
        result = client.get_volumes()
        assert isinstance(result, list)
      


def test_get_volume_by_id(client, mock_response, sample_volumes):
    with patch.object(client, "_session") as mock_session:
        mock_session.get.return_value = mock_response(sample_volumes[0])
        result = client.get_volume("vol-001")
        assert result["id"] == "vol-001"

def test_create_volume(client, mock_response):
    new_volume = {"name": "New Volume", "size": 10}
    created_volume = {"id": "vol-002", "name": "New Volume", "size": 10}
    with patch.object(client, "_session") as mock_session:
        mock_session.post.return_value = mock_response(created_volume)
        result = client.create_volume("New Volume", 10)
        assert result["id"] == "vol-002"
        assert result["name"] == "New Volume"
        assert result["size"] == 10

def test_delete_volume(client, mock_response):
    with patch.object(client, "_session") as mock_session:
        mock_session.delete.return_value = mock_response({"message": "Volume deleted"})
        result = client.delete_volume("vol-001")
        assert result is True

def test_get_volume_empty_id_raises_error(client):
    with pytest.raises(ValueError) as exc:
        client.get_volume("")
    assert str(exc.value) == "volume_id cannot be empty"
        



        