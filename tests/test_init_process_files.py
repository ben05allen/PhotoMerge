# pyright: basic


from pathlib import Path
import pytest
import tempfile

from photomerge import process_files


@pytest.fixture()
def source_dir():
    temp_src_dir = tempfile.TemporaryDirectory(delete=False)

    (Path(temp_src_dir.name) / "folder1").mkdir(exist_ok=True)
    (Path(temp_src_dir.name) / "folder2").mkdir(exist_ok=True)

    for file_name in [
        "file1.jpg",
        "folder1/file1.jpg",
        "folder1/file2.png",
        "folder1/file3.jpg",
        "folder1/file4.txt",
        "folder2/file1.jpg",
    ]:
        file = Path(temp_src_dir.name) / file_name
        file.write_bytes(file_name.encode())

    yield Path(temp_src_dir.name)

    temp_src_dir.cleanup()


@pytest.fixture
def bad_source_dir():
    temp_src_dir = tempfile.TemporaryDirectory(delete=False)

    (Path(temp_src_dir.name) / "folder1").mkdir(exist_ok=True)

    for file_name in ["bad_file1.jpg", "bad_file2.jpg", "folder1/bad_file1.jpg"]:
        file = Path(temp_src_dir.name) / file_name
        file.write_bytes(file_name.encode())

    yield Path(temp_src_dir.name)

    temp_src_dir.cleanup()


@pytest.fixture()
def target_dir():
    temp_tgt_dir = tempfile.TemporaryDirectory()

    yield Path(temp_tgt_dir.name)

    temp_tgt_dir.cleanup()


def test_process_files_ignores_file_in_ignored_files(source_dir, target_dir, caplog):
    caplog.set_level(10)  # Set log level to INFO
    ignored_files = {"file1.jpg"}
    process_files(
        data_dir=source_dir,
        out_dir=target_dir,
        hashes=set(),
        filenames=set(),
        allowed_extensions={".jpg", ".png"},
        ignored_files=ignored_files,
        is_recursive=True,
    )

    # Check that the file was ignored
    should_not_exist = target_dir / "file1.jpg"
    assert not should_not_exist.exists()
    assert "Ignoring file: file1.jpg" in caplog.text
    assert "New photo found: file1.jpg" not in caplog.text


def test_process_files_new_file_copied_successfully(source_dir, target_dir, caplog):
    caplog.set_level(10)  # Set log level to INFO
    allowed_extensions = {".jpg", ".png"}

    process_files(
        data_dir=source_dir,
        out_dir=target_dir,
        hashes=set(),
        filenames=set(),
        allowed_extensions=allowed_extensions,
        ignored_files=set(),
        is_recursive=True,
    )

    for p in [
        "file1.jpg",
        "file1_1.jpg",
        "file2.png",
        "file3.jpg",
        "file4.txt",
        "file1_2.jpg",
    ]:
        target_file = target_dir / p
        if f".{p.lower().split('.')[-1]}" in allowed_extensions:
            assert target_file.exists()
        else:
            assert not target_file.exists()

    # Check that the file was processed, copied, and logged
    assert "New photo found: file2.png" in caplog.text
    assert "New photo found: file1.jpg" in caplog.text
    assert f"Saved: file3.jpg in {target_dir}" in caplog.text
    assert f"Saved: file1.jpg in {target_dir} as file1_1.jpg" in caplog.text


def test_process_files_copy_failure(bad_source_dir, target_dir, mocker, caplog):
    caplog.set_level(10)  # Set log level to INFO

    mock_copy_file = mocker.patch("photomerge.copy_file", return_value=False)  # noqa: F841

    process_files(
        data_dir=bad_source_dir,
        out_dir=target_dir,
        hashes=set(),
        filenames=set(),
        allowed_extensions={".jpg", ".png"},
        ignored_files=set(),
        is_recursive=True,
    )

    # Check that the copy failure is logged
    assert "Failed to copy file: bad_file1.jpg" in caplog.text
    assert "Failed to copy file: bad_file2.jpg" in caplog.text
    assert "Failed to copy duplicate file: bad_file1.jpg" in caplog.text
    assert f"Saved: bad_file1.jpg in {target_dir}" not in caplog.text
    assert not (target_dir / "bad_file.jpg").exists()


def test_process_files_respects_is_not_recursive(source_dir, target_dir, caplog):
    caplog.set_level(10)  # Set log level to INFO
    allowed_extensions = {".jpg", ".png"}

    process_files(
        data_dir=source_dir,
        out_dir=target_dir,
        hashes=set(),
        filenames=set(),
        allowed_extensions=allowed_extensions,
        ignored_files=set(),
        is_recursive=False,
    )

    # Check that only allowed files were processed, copied, and logged
    for p in ["file2.png", "file3.jpg", "file4.txt", "file1_1.jpg"]:
        target_file = target_dir / p
        assert not target_file.exists()

    assert "New photo found: file1.jpg" in caplog.text
    assert "New photo found: file2.png" not in caplog.text
    assert f"Saved: file3.jpg in {target_dir}" not in caplog.text
    assert f"Saved: file1.jpg in {target_dir} as file1_1.jpg" not in caplog.text


def test_process_files_respects_allowed_extensions(source_dir, target_dir, caplog):
    caplog.set_level(10)  # Set log level to INFO
    allowed_extensions = {".jpg"}

    process_files(
        data_dir=source_dir,
        out_dir=target_dir,
        hashes=set(),
        filenames=set(),
        allowed_extensions=allowed_extensions,
        ignored_files=set(),
        is_recursive=True,
    )

    # Check that only allowed files were processed, copied, and logged
    for p in ["file2.png", "file4.txt"]:
        target_file = target_dir / p
        assert not target_file.exists()

    assert "New photo found: file1.jpg" in caplog.text
    assert "New photo found: file2.png" not in caplog.text
    assert f"Saved: file3.jpg in {target_dir}" in caplog.text
    assert f"Saved: file4.txt in {target_dir}" not in caplog.text
    assert f"Saved: file1.jpg in {target_dir} as file1_1.jpg" in caplog.text
