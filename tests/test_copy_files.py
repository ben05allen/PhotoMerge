# pyright: basic


from pathlib import Path

from photomerge.copy_files import copy_file


def test_copy_file_success(tmp_path):
    source_file = tmp_path / "src_file"
    source_file.write_bytes(b"source file contents")
    target_folder = tmp_path / "tgt_folder"
    Path.mkdir(target_folder)

    result = copy_file(source_file, target_folder)
    with open(target_folder / "src_file", "rb") as f:
        file_contents = f.read()

    assert result is True
    assert (target_folder / (source_file.name)).exists()
    assert b"source file contents" in file_contents


def test_copy_file_failure(caplog):
    # Test if function returns False on OSError
    result = copy_file(Path("source.txt"), Path("destination.txt"))
    assert result is False
    assert "Error attempting to copy file" in caplog.text
