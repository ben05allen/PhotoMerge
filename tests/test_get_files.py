# pyright: basic


from pathlib import Path
from photomerge.get_files import find_files_with_extensions


def test_find_files_with_extensions_recursive(mocker):
    # Mock rglob to simulate recursive search in the directory
    mock_rglob = mocker.patch("photomerge.get_files.Path.rglob")
    mock_rglob.return_value = [
        Path("folder/file1.txt"),
        Path("folder/subfolder/file2.txt"),
        Path("folder/subfolder/file3.md"),
    ]

    # Test with recursive search
    result = list(
        find_files_with_extensions(Path("folder"), [".txt"], is_recursive=True)
    )
    expected = [
        Path("folder/file1.txt").resolve(),
        Path("folder/subfolder/file2.txt").resolve(),
    ]
    assert result == expected
    mock_rglob.assert_called_once_with("*")


def test_find_files_with_extensions_non_recursive(mocker):
    # Mock iterdir to simulate non-recursive search in the directory
    mock_iterdir = mocker.patch("photomerge.get_files.Path.iterdir")
    mock_iterdir.return_value = [
        Path("folder/file1.txt"),
        Path("folder/file2.md"),
        Path("folder/file3.txt"),
        Path("folder/subfolder"),  # This is a directory, not a file
    ]

    # Test with non-recursive search
    result = list(
        find_files_with_extensions(Path("folder"), [".txt"], is_recursive=False)
    )
    expected = [Path("folder/file1.txt").resolve(), Path("folder/file3.txt").resolve()]
    assert result == expected
    mock_iterdir.assert_called_once_with()


def test_find_files_with_extensions_non_recursive_no_match(mocker):
    # Mock iterdir to simulate non-recursive search with no matching files
    mock_iterdir = mocker.patch("photomerge.get_files.Path.iterdir")
    mock_iterdir.return_value = [
        Path("folder/file1.md"),
        Path("folder/file2.pdf"),
        Path("folder/subfolder"),  # This is a directory, not a file
    ]

    # Test with non-recursive search where no files match the extensions
    result = list(
        find_files_with_extensions(Path("folder"), [".txt"], is_recursive=False)
    )
    assert result == []
    mock_iterdir.assert_called_once_with()


def test_find_files_with_extensions_recursive_no_match(mocker):
    # Mock rglob to simulate recursive search with no matching files
    mock_rglob = mocker.patch("photomerge.get_files.Path.rglob")
    mock_rglob.return_value = [
        Path("folder/file1.md"),
        Path("folder/subfolder/file2.pdf"),
    ]

    # Test with recursive search where no files match the extensions
    result = list(
        find_files_with_extensions(Path("folder"), [".txt"], is_recursive=True)
    )
    assert result == []
    mock_rglob.assert_called_once_with("*")
