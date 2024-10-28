from pathlib import Path
from app.get_files import (
    find_files_with_extensions,
)


def test_find_files_with_matching_extensions(mocker):
    # Mock Path.rglob to return a list of Paths with various extensions
    mock_rglob = mocker.patch("app.get_files.Path.rglob")
    mock_rglob.return_value = [
        Path("file1.txt"),
        Path("file2.md"),
        Path("file3.TXT"),
        Path("file4.pdf"),
    ]

    # Test with .txt extension
    result = list(find_files_with_extensions("dummy_folder", [".txt"]))
    expected = [Path("file1.txt").resolve(), Path("file3.TXT").resolve()]
    assert result == expected


def test_find_files_with_no_matching_extensions(mocker):
    mock_rglob = mocker.patch("app.get_files.Path.rglob")
    mock_rglob.return_value = [Path("file1.txt"), Path("file2.md"), Path("file3.pdf")]

    # Test with .jpg extension, which doesn't match any file
    result = list(find_files_with_extensions("dummy_folder", [".jpg"]))
    assert result == []


def test_find_files_with_multiple_extensions(mocker):
    mock_rglob = mocker.patch("app.get_files.Path.rglob")
    mock_rglob.return_value = [
        Path("file1.txt"),
        Path("file2.md"),
        Path("file3.pdf"),
        Path("file4.JPG"),
        Path("file5.jpeg"),
    ]

    # Test with multiple extensions
    result = list(find_files_with_extensions("dummy_folder", [".jpg", ".jpeg"]))
    expected = [Path("file4.JPG").resolve(), Path("file5.jpeg").resolve()]
    assert result == expected


def test_find_files_case_insensitivity(mocker):
    mock_rglob = mocker.patch("app.get_files.Path.rglob")
    mock_rglob.return_value = [Path("file1.TxT"), Path("file2.md"), Path("file3.PDF")]

    # Test with mixed-case extensions
    result = list(find_files_with_extensions("dummy_folder", [".txt", ".pdf"]))
    expected = [Path("file1.TxT").resolve(), Path("file3.PDF").resolve()]
    assert result == expected
