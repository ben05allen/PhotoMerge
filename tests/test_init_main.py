# pyright: basic


import argparse
import pytest
from unittest.mock import patch

from photomerge import main


@pytest.fixture
def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", "-s", required=True)
    parser.add_argument("--target", "-t", required=True)
    parser.add_argument("--config", "-c")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--non_recursive", "-n", action="store_false")
    return parser.parse_args(
        [
            "--source",
            "source_dir",
            "--target",
            "target_dir",
            "--config",
            "config_file.toml",
            "--verbose",
        ]
    )


# def test_main_success(args, mocker):
#     # Mock dependencies
#     mock_logger = mocker.patch("photomerge.LOGGER")
#     mock_add_console_handler = mocker.patch("photomerge.add_console_handler")
#     mock_get_config = mocker.patch(
#         "photomerge.get_config",
#         return_value={
#             "extensions": {"allowed": [".jpg", ".png"]},
#             "files": {"ignored": ["ignored_file.jpg"]},
#         },
#     )
#     mock_initialize_paths = mocker.patch(
#         "photomerge.initialize_paths", return_value=(MagicMock(), MagicMock())
#     )
#     mock_initialize_hashes = mocker.patch(
#         "photomerge.initialize_hashes", return_value=(set(), set())
#     )
#     mock_process_files = mocker.patch("photomerge.process_files")
#
#     # Run main
#     main()
#
#     # Verify that add_console_handler was called since verbose=True
#     mock_add_console_handler.assert_called_once_with(mock_logger)
#
#     # Verify configuration is loaded correctly
#     mock_get_config.assert_called_once_with("config_file.toml")
#
#     # Verify that initialize_paths is called with correct arguments
#     mock_initialize_paths.assert_called_once_with("source_dir", "target_dir")
#
#     # Verify that initialize_hashes is called with the output directory path
#     out_dir = mock_initialize_paths.return_value[1]
#     extensions = {".jpg", ".png"}
#     mock_initialize_hashes.assert_called_once_with(extensions, out_dir)
#
#     # Verify process_files is called with the correct arguments
#     mock_process_files.assert_called_once_with(
#         data_dir=mock_initialize_paths.return_value[0],
#         out_dir=out_dir,
#         hashes=set(),
#         filenames=set(),
#         allowed_extensions={".jpg", ".png"},
#         ignored_files={"ignored_file.jpg"},
#         is_recursive=True,
#     )
#
#     # Check if logger info messages were called with expected values
#     # mock_logger.info.assert_any_call("Allowed extensions: {'.jpg', '.png'}")
#     mock_logger.info.assert_any_call("Ignored files: {'ignored_file.jpg'}")
