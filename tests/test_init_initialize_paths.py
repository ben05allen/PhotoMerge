# pyright: basic

from pathlib import Path
import pytest

from photomerge import initialize_paths


def test_initialize_paths_success(tmp_path):
    source_dir = tmp_path / "A"
    target_dir = tmp_path / "B"
    Path.mkdir(source_dir)
    Path.mkdir(target_dir)

    source, target = initialize_paths(str(source_dir), str(target_dir))

    # Assertions to ensure correct paths are returned
    assert source == Path(str(source_dir))
    assert target == Path(str(target_dir))


def test_initialize_paths_source_missing(tmp_path):
    source_dir = tmp_path / "Missing"
    target_dir = tmp_path / "B"
    Path.mkdir(target_dir)

    # Test for FileNotFoundError when source is missing
    with pytest.raises(
        FileNotFoundError,
        match=f"Source directory does not exist: {source_dir}",
    ):
        initialize_paths(str(source_dir), str(target_dir))


def test_initialize_paths_target_missing(tmp_path):
    source_dir = tmp_path / "A"
    Path.mkdir(source_dir)
    target_dir = tmp_path / "Missing"

    # Test for FileNotFoundError when target is missing
    with pytest.raises(
        FileNotFoundError,
        match=f"Target directory does not exist: {target_dir}",
    ):
        initialize_paths(str(source_dir), str(target_dir))
