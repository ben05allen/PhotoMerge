from copy_files import copy_file


def test_copy_file_success(mocker):
    # Mock copy2 to simulate a successful file copy
    mock_copy = mocker.patch("copy_files.copy2", return_value=None)

    result = copy_file("source.txt", "destination.txt")
    mock_copy.assert_called_once_with("source.txt", "destination.txt")
    assert result is True


def test_copy_file_failure_io_error(mocker):
    # Mock copy2 to raise an IOError
    mock_copy = mocker.patch("copy_files.copy2", side_effect=IOError)

    # Test if function returns False on IOError
    result = copy_file("source_path", "destination_path")
    assert result is False
    mock_copy.assert_called_once_with("source_path", "destination_path")


def test_copy_file_failure_os_error(mocker):
    # Mock copy2 to raise an OSError
    mock_copy = mocker.patch("copy_files.copy2", side_effect=OSError)

    # Test if function returns False on OSError
    result = copy_file("source_path", "destination_path")
    assert result is False
    mock_copy.assert_called_once_with("source_path", "destination_path")


def test_copy_file_failure_file_not_found(mocker):
    # Mock copy2 to raise a FileNotFoundError
    mock_copy = mocker.patch("copy_files.copy2", side_effect=FileNotFoundError)

    # Test if function returns False on FileNotFoundError
    result = copy_file("source_path", "destination_path")
    assert result is False
    mock_copy.assert_called_once_with("source_path", "destination_path")
