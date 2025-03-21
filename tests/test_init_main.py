# pyright: basic

import logging
from pathlib import Path
import pytest
import tempfile
from unittest.mock import patch

from photomerge import main as photomerge_main


@pytest.fixture
def source_dir():
    temp_src_dir = tempfile.TemporaryDirectory(delete=False)

    (Path(temp_src_dir.name) / "folder1").mkdir(exist_ok=True)
    (Path(temp_src_dir.name) / "folder2").mkdir(exist_ok=True)

    for file_name in [
        "file1.jpg",
        "folder1/file1.jpg",
        "folder1/file2.png",
        "folder2/file1.jpg",
    ]:
        file = Path(temp_src_dir.name) / file_name
        file.write_bytes(file_name.encode())

    yield Path(temp_src_dir.name)

    temp_src_dir.cleanup()


@pytest.fixture
def target_dir():
    temp_tgt_dir = tempfile.TemporaryDirectory()

    yield Path(temp_tgt_dir.name)

    temp_tgt_dir.cleanup()


@pytest.fixture
def custom_config():
    temp_config_file = tempfile.NamedTemporaryFile(delete=False, suffix=".toml")

    config_contents = """
[extensions]
    allowed = ['.png', '.jpg', '.jpeg', '.tiff', 'tif', '.bmp', '.webp', '.heif', '.heic']
    
[files]
    ignored = ['ignore_me.png']
"""
    with open(temp_config_file.name, "w") as f:
        f.write(config_contents)

    yield Path(temp_config_file.name)

    temp_config_file.close()


def test_main_success(source_dir, target_dir):
    test_args = f"prog --source {source_dir} --target {target_dir}".split()

    with patch("sys.argv", test_args):
        photomerge_main()
        assert (Path(str(target_dir)) / "file1.jpg").exists()


def test_main_verbose_success(source_dir, target_dir):
    test_args = f"prog --source {source_dir} --target {target_dir} --verbose".split()

    with patch("sys.argv", test_args):
        photomerge_main()
        assert (Path(str(target_dir)) / "file1.jpg").exists()


def test_main_custom_config_success(source_dir, target_dir, custom_config):
    test_args = f"prog --source {source_dir} --target {target_dir} --config {custom_config}".split()

    with patch("sys.argv", test_args):
        photomerge_main()
        assert (Path(str(target_dir)) / "file1.jpg").exists()


def test_main_config_failure(source_dir, target_dir, caplog):
    test_args = f"prog --source {source_dir} --target {target_dir} --config path/that/doesnt/exist".split()

    with patch("sys.argv", test_args):
        with pytest.raises(FileNotFoundError):
            photomerge_main()

        assert "Config file not found: path/that/doesnt/exist" in caplog.text
        assert not (Path(str(target_dir)) / "file1.jpg").exists()
