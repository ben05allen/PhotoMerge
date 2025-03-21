# pyright: basic


from pathlib import Path
import pytest
import tempfile

from photomerge.copy_files import copy_file


@pytest.fixture()
def source_file():
    with tempfile.NamedTemporaryFile() as temp_src_file:
        temp_src_file.write(b"source file contents")

        yield Path(temp_src_file.name)


@pytest.fixture()
def target_folder():
    temp_tgt_folder = tempfile.TemporaryDirectory()
    yield Path(temp_tgt_folder.name)


def test_copy_file_success(source_file, target_folder):
    result = copy_file(source_file, target_folder)

    assert (target_folder / (source_file.name)).exists()
    assert result is True


def test_copy_file_failure_io_error(mocker):
    # Mock copy2 to raise an IOError
    mock_copy = mocker.patch("photomerge.copy_files.copy2", side_effect=IOError)

    # Test if function returns False on IOError
    result = copy_file(Path("source.txt"), Path("destination.txt"))
    assert result is False
    mock_copy.assert_called_once_with(
        str(Path("source.txt").resolve()), str(Path("destination.txt").resolve())
    )


def test_copy_file_failure_os_error(caplog, mocker):
    # Mock copy2 to raise an OSError
    mock_copy = mocker.patch("photomerge.copy_files.copy2", side_effect=OSError)

    # Test if function returns False on OSError
    result = copy_file(Path("source.txt"), Path("destination.txt"))
    assert result is False
    mock_copy.assert_called_once_with(
        str(Path("source.txt").resolve()), str(Path("destination.txt").resolve())
    )
    assert "Error attempting to copy file" in caplog.text


def test_copy_file_failure_file_not_found(mocker):
    # Mock copy2 to raise a FileNotFoundError
    mock_copy = mocker.patch(
        "photomerge.copy_files.copy2", side_effect=FileNotFoundError
    )

    # Test if function returns False on FileNotFoundError
    result = copy_file(Path("source.txt"), Path("destination.txt"))
    assert result is False
    mock_copy.assert_called_once_with(
        str(Path("source.txt").resolve()), str(Path("destination.txt").resolve())
    )
