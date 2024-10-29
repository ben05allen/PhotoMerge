import pytest
from app.main import get_config
from unittest.mock import patch, mock_open
from pathlib import Path

# Assuming DEFAULT_CONFIG and LOGGER are defined in app.main
DEFAULT_CONFIG = Path("/path/to/default/config.toml")


@pytest.fixture
def mock_logger(mocker):
    mocker = mocker.patch("app.logger.setup_logging")
    return mocker.patch("app.main.LOGGER")


def test_get_config_with_custom_path(mock_logger, mocker):
    mock_config_data = b'{"key": "value"}'
    mock_open_file = mock_open(read_data=mock_config_data)

    with patch("app.main.open", mock_open_file):
        mock_tomllib = mocker.patch(
            "app.main.tomllib.load", return_value={"key": "value"}
        )

        # Call the function with a custom config path
        config = get_config("custom/config.toml")

        # Assertions
        assert config == {"key": "value"}
        mock_logger.info.assert_called_once_with(
            "Using custom config file: custom/config.toml"
        )
        mock_tomllib.assert_called_once()


def test_get_config_with_default_path(mock_logger, mocker):
    # Mock the file reading process with a sample config
    mock_config_data = b'{"key": "default_value"}'
    mock_open_file = mock_open(read_data=mock_config_data)
    with patch("app.main.open", mock_open_file):
        # Mock tomllib to simulate loading the configuration dictionary
        mock_tomllib = mocker.patch(
            "app.main.tomllib.load", return_value={"key": "default_value"}
        )

        config = get_config(None)

        # Check that the default config path is used and log message is correct
        assert config == {"key": "default_value"}
        mock_logger.info.assert_called_once_with("Using default config file")
        mock_tomllib.assert_called_once()


def test_get_config_file_not_found(mock_logger, mocker):
    # Patch open to raise FileNotFoundError
    with patch("app.main.open", side_effect=FileNotFoundError):
        config = get_config("nonexistent/config.toml")

        # Check that the function returns None and logs an error
        assert config is None
        mock_logger.error.assert_called_once_with(
            "Config file not found: nonexistent/config.toml"
        )
