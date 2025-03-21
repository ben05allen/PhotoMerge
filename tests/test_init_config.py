# pyright: basic

import logging
from pathlib import Path
import pytest
from tempfile import NamedTemporaryFile
from unittest.mock import patch

from photomerge import get_config


@pytest.fixture
def config_file_path():
    config_data = 'foo = "bar"'
    with NamedTemporaryFile(delete=False, suffix=".toml") as temp_file:
        temp_file.write(config_data.encode())
        temp_file_path = Path(temp_file.name)
    yield temp_file_path
    temp_file_path.unlink()


def test_get_config_with_custom_path(config_file_path, caplog):
    # Mock the file reading process with a sample config
    caplog.set_level(logging.INFO)
    config = get_config(config_file_path)

    # Check that the correct path is used and log message is correct
    assert config == {"foo": "bar"}
    assert caplog.records[-1].message == (
        f"Using custom config file: {str(config_file_path)}"
    )


def test_get_config_with_default_path(config_file_path, caplog):
    # Mock the file reading process with a sample config
    with patch("photomerge.DEFAULT_CONFIG", config_file_path):
        caplog.set_level(logging.INFO)
        config = get_config(None)

    # Check that the default config path is used and log message is correct
    assert config == {"foo": "bar"}
    assert caplog.records[-1].message == "Using default config file"


def test_get_config_file_not_found(caplog):
    # Patch open to raise FileNotFoundError

    path_to_nonexistent_file = Path("nonexistent/config.toml")
    with pytest.raises(FileNotFoundError):
        _ = get_config(path_to_nonexistent_file)

    assert caplog.records[-1].message == (
        f"Config file not found: {str(path_to_nonexistent_file)}"
    )
