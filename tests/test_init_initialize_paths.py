# pyright: basic


from pathlib import Path
import pytest
from photomerge import initialize_paths


def test_initialize_paths_success(mocker):
    # Mock Path.exists to simulate that both paths exist
    mock_exists = mocker.patch("pathlib.Path.exists", return_value=True)

    # Call the function with mock paths
    source, target = initialize_paths("source_dir", "target_dir")

    # Assertions to ensure correct paths are returned
    assert source == Path("source_dir")
    assert target == Path("target_dir")
    assert mock_exists.call_count == 2  # Check that both paths were checked


def test_initialize_paths_source_missing(mocker):
    # Mock Path.exists to simulate source does not exist, but target does
    mock_exists = mocker.patch("pathlib.Path.exists", side_effect=[False, True])  # noqa: F841
    mock_logger = mocker.patch("photomerge.LOGGER")  # Mock the logger

    # Test for FileNotFoundError when source is missing
    with pytest.raises(
        FileNotFoundError, match="Source directory does not exist: source_dir"
    ):
        initialize_paths("source_dir", "target_dir")

    # Assert that the logger was called with the correct message
    mock_logger.error.assert_called_once_with(
        "Source directory does not exist: source_dir"
    )


def test_initialize_paths_target_missing(mocker):
    # Mock Path.exists to simulate source exists but target does not
    mock_exists = mocker.patch("pathlib.Path.exists", side_effect=[True, False])  # noqa: F841
    mock_logger = mocker.patch("photomerge.LOGGER")  # Mock the logger

    # Test for FileNotFoundError when target is missing
    with pytest.raises(
        FileNotFoundError, match="Target directory does not exist: target_dir"
    ):
        initialize_paths("source_dir", "target_dir")

    # Assert that the logger was called with the correct message
    mock_logger.error.assert_called_once_with(
        "Target directory does not exist: target_dir"
    )
