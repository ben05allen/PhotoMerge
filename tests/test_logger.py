import logging
from app.logger import setup_logging


def test_setup_logging_file_handler(tmp_path):
    # Create a temporary file path for the log file
    log_file = tmp_path / "test.log"

    # Set up logging without verbose mode
    logger = setup_logging(str(log_file), verbose=False)

    # Check that there is only one handler (file handler) when verbose=False
    assert len(logger.handlers) == 1
    file_handler = logger.handlers[0]
    assert isinstance(file_handler, logging.FileHandler)

    # Log a message and verify it is written to the log file
    test_message = "Test debug message"
    logger.debug(test_message)

    # Check if the message was written to the log file
    with open(log_file, "r") as f:
        log_content = f.read()
        assert test_message in log_content


def test_setup_logging_verbose_mode(tmp_path, caplog):
    # Create a temporary file path for the log file
    log_file = tmp_path / "test.log"

    # Set up logging with verbose mode
    logger = setup_logging(str(log_file), verbose=True)

    # Check that there are two more handlers (file and console) when verbose=True
    assert len(logger.handlers) == 2

    # Log a message and verify it appears in both file and console
    test_message = "Test verbose mode message"
    with caplog.at_level(logging.DEBUG):
        logger.debug(test_message)

        # Check that the message appears in the console output
        assert any(test_message in record.message for record in caplog.records)


def test_setup_logging_no_duplicate_handlers(tmp_path):
    # Create a temporary file path for the log file
    log_file = tmp_path / "test.log"

    # Set up logging twice to check for duplicate handlers
    logger = setup_logging(str(log_file), verbose=True)
    logger = setup_logging(str(log_file), verbose=True)

    # Ensure no duplicate handlers are created
    assert len(logger.handlers) == 2


def test_setup_logging_file_handler_log_levels(tmp_path):
    # Create a temporary file path for the log file
    log_file = tmp_path / "test.log"

    # Set up logging without verbose mode
    logger = setup_logging(str(log_file), verbose=False)

    # Check that the file handler is set to DEBUG level
    file_handler = logger.handlers[0]
    assert file_handler.level == logging.DEBUG
