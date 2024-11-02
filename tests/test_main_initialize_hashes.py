from pathlib import Path
from app.main import initialize_hashes


def test_initialize_hashes_success(mocker):
    # Mock find_files_with_extensions to simulate files in the directory
    mock_find_files = mocker.patch(
        "app.main.find_files_with_extensions",
        return_value=[
            Path("file1.jpg"),
            Path("file2.jpg"),
            Path("file3.png"),
        ],
    )

    # Mock calculate_hash to return a unique hash for each file
    mock_calculate_hash = mocker.patch(
        "app.main.calculate_hash", side_effect=["hash1", "hash2", "hash3"]
    )

    # Call the function
    hashes, filenames = initialize_hashes(Path("out_dir"))

    # Assertions
    assert hashes == {"hash1", "hash2", "hash3"}
    assert filenames == {"file1.jpg", "file2.jpg", "file3.png"}
    mock_find_files.assert_called_once_with(Path("out_dir"), is_recursive=False)
    assert mock_calculate_hash.call_count == 3


def test_initialize_hashes_empty_directory(mocker):
    # Mock find_files_with_extensions to return an empty list, simulating an empty directory
    mock_find_files = mocker.patch(
        "app.main.find_files_with_extensions", return_value=[]
    )

    # Call the function
    hashes, filenames = initialize_hashes(Path("out_dir"))

    # Assertions
    assert hashes == set()
    assert filenames == set()
    mock_find_files.assert_called_once_with(Path("out_dir"), is_recursive=False)
