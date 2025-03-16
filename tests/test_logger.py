# pyright: basic


import pytest
import logging

from photomerge.logger import setup_logging, add_console_handler


@pytest.fixture
def temp_log_file(tmp_path):
    # Ensure the directory exists and create a temporary log file path
    temp_file_path = tmp_path / "test.log"
    temp_file_path.touch()  # Create the file to avoid FileNotFoundError
    return temp_file_path


@pytest.fixture
def isolated_logger():
    # Create and yield a fresh logger, clearing its handlers after each test
    logger = logging.getLogger(__name__)
    logger.handlers = []  # Clear existing handlers
    yield logger
    logger.handlers = []  # Reset for next test


def test_setup_logging_adds_file_handler(temp_log_file, isolated_logger):
    # Setup logging with the temporary file path
    logger = setup_logging(temp_log_file)

    # Verify there is one handler and it's a FileHandler
    assert len(logger.handlers) == 1
    assert logger.handlers[0].__class__.__name__ == "FileHandler"
    assert logger.handlers[0].level == logging.DEBUG

    # # Log a message and confirm it's written to the temp file
    # test_message = "Testing file handler"
    # logger.debug(test_message)
    # with open(temp_log_file, "r") as f:
    #     log_content = f.read()
    #     assert test_message in log_content


def test_setup_logging_does_not_add_duplicate_file_handler(temp_log_file):
    # Initialize the logger twice with the same file handler to test for duplicates
    logger = setup_logging(temp_log_file)
    logger = setup_logging(temp_log_file)

    # Ensure only one FileHandler is present
    file_handlers = [
        h for h in logger.handlers if h.__class__.__name__ == "FileHandler"
    ]
    assert len(file_handlers) == 1


def test_add_console_handler_adds_stream_handler(temp_log_file):
    # Initialize logger with a file handler
    logger = setup_logging(temp_log_file)

    # Add console handler and verify it's added
    add_console_handler(logger)

    # Ensure there are two handlers: FileHandler and StreamHandler
    assert len(logger.handlers) == 2
    assert any(h.__class__.__name__ == "FileHandler" for h in logger.handlers)
    assert any(h.__class__.__name__ == "StreamHandler" for h in logger.handlers)


def test_add_console_handler_does_not_add_duplicate_stream_handler(temp_log_file):
    # Initialize logger and add console handler twice to test for duplicates
    logger = setup_logging(temp_log_file)
    add_console_handler(logger)
    add_console_handler(logger)

    # Ensure only one StreamHandler is present
    stream_handlers = [
        h for h in logger.handlers if h.__class__.__name__ == "StreamHandler"
    ]
    assert len(stream_handlers) == 1


# def test_add_console_handler_logs_to_stdout(temp_log_file, capsys):
#     # Initialize logger with file handler
#     logger = setup_logging(temp_log_file)

#     # Add console handler
#     logger = add_console_handler(logger)

#     # Log a message
#     test_message = "Testing console handler"
#     logger.debug(test_message)

#     # Capture stdout and verify the log message is output to the console
#     captured = capsys.readouterr()
#     assert test_message in captured.out
