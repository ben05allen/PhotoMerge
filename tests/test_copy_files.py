from app.copy_files import copy_file


def test_copy_file_success(mocker):
    # Mock copy2 to simulate a successful file copy
    mock_copy = mocker.patch("app.copy_files.copy2", return_value=None)

    result = copy_file("source.txt", "destination.txt")
    mock_copy.assert_called_once_with("source.txt", "destination.txt")
    assert result is True
