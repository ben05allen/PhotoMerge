import pytest
from hash_files import calculate_hash
from unittest.mock import mock_open, patch
import hashlib


def test_calculate_hash_success(mocker):
    # Mock data to simulate file content
    mock_data = b"sample data for hashing"
    expected_hash = hashlib.md5(mock_data).hexdigest()

    # Patch 'open' and simulate reading from a file
    mock_open_file = mock_open(read_data=mock_data)
    with patch("hash_files.open", mock_open_file):
        result = calculate_hash("dummy_file.txt")

    # Verify that the result is the expected hash
    assert result == expected_hash
    mock_open_file.assert_called_once_with("dummy_file.txt", "rb")


def test_calculate_hash_file_not_found(mocker):
    # Patch 'open' to raise a FileNotFoundError
    mock_open_file = mocker.patch("hash_files.open", side_effect=FileNotFoundError)

    with pytest.raises(FileNotFoundError):
        calculate_hash("nonexistent_file.txt")

    # Ensure open was called with the right arguments
    mock_open_file.assert_called_once_with("nonexistent_file.txt", "rb")


def test_calculate_hash_empty_file(mocker):
    # Simulate an empty file by returning an empty byte string
    mock_data = b""
    expected_hash = hashlib.md5(mock_data).hexdigest()

    mock_open_file = mock_open(read_data=mock_data)
    with patch("hash_files.open", mock_open_file):
        result = calculate_hash("empty_file.txt")

    # Verify that the result is the hash for an empty string
    assert result == expected_hash
    mock_open_file.assert_called_once_with("empty_file.txt", "rb")
