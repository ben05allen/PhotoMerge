import logging
from app.main import get_config  # Replace 'app.main' with the module name
from unittest.mock import patch, mock_open
from pathlib import Path

# Assuming DEFAULT_CONFIG and LOGGER are defined in app.main
DEFAULT_CONFIG = Path("/path/to/default/config.toml")


def test_get_config_with_custom_path(caplog, mocker):
    # Mock the file reading process with a sample config
    mock_config_data = b'{"key": "value"}'
    mock_open_file = mock_open(read_data=mock_config_data)
    with patch("app.main.open", mock_open_file), caplog.at_level(logging.INFO):
        # Mock tomllib to simulate loading the configuration dictionary
        mock_tomllib = mocker.patch(
            "app.main.tomllib.load", return_value={"key": "value"}
        )

        config = get_config("custom/config.toml")

        # Check that the correct path is used and log message is correct
        assert config == {"key": "value"}
        assert caplog.records[-1].message == (
            "Using custom config file: custom/config.toml"
        )
        mock_tomllib.assert_called_once()


def test_get_config_with_default_path(caplog, mocker):
    # Mock the file reading process with a sample config
    mock_config_data = b'{"key": "default_value"}'
    mock_open_file = mock_open(read_data=mock_config_data)
    with patch("app.main.open", mock_open_file), caplog.at_level(logging.INFO):
        # Mock tomllib to simulate loading the configuration dictionary
        mock_tomllib = mocker.patch(
            "app.main.tomllib.load", return_value={"key": "default_value"}
        )

        config = get_config(None)

        # Check that the default config path is used and log message is correct
        assert config == {"key": "default_value"}
        assert caplog.records[-1].message == "Using default config file"
        mock_tomllib.assert_called_once()


def test_get_config_file_not_found(caplog):
    # Patch open to raise FileNotFoundError
    with patch("app.main.open", side_effect=FileNotFoundError):
        config = get_config("nonexistent/config.toml")

        # Check that the function returns None and logs an error
        assert config is None
        caplog.records[-1].levelname == "ERROR"
