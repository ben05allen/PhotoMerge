import pytest
from main import parse_args
from unittest.mock import patch


def test_parse_args_required_arguments():
    # Simulate command-line arguments
    test_args = ["prog", "--source", "source_path", "--target", "target_path"]

    with patch("sys.argv", test_args):
        args = parse_args()
        assert args.source == "source_path"
        assert args.target == "target_path"
        assert args.verbose is False  # Default when not specified
        assert args.non_recursive is True  # Default when not specified


def test_parse_args_all_arguments():
    test_args = [
        "prog",
        "--source",
        "source_path",
        "--target",
        "target_path",
        "--verbose",
        "--non_recursive",
        "--config",
        "config_path",
    ]

    with patch("sys.argv", test_args):
        args = parse_args()
        assert args.source == "source_path"
        assert args.target == "target_path"
        assert args.verbose is True  # Set by --verbose flag
        assert args.non_recursive is False  # Set by --non_recursive flag
        assert args.config == "config_path"


def test_parse_args_missing_required_arguments():
    test_args = ["prog", "--source", "source_path"]

    with patch("sys.argv", test_args), pytest.raises(SystemExit):
        parse_args()  # Should exit due to missing --target


def test_parse_args_non_recursive_flag():
    # Test if `--non_recursive` correctly sets the flag to False
    test_args = [
        "prog",
        "--source",
        "source_path",
        "--target",
        "target_path",
        "--non_recursive",
    ]

    with patch("sys.argv", test_args):
        args = parse_args()
        assert args.non_recursive is False  # --non_recursive should set it to False


def test_parse_args_default_recursive_flag():
    # Test if `non_recursive` defaults to True when --non_recursive is not set
    test_args = ["prog", "--source", "source_path", "--target", "target_path"]

    with patch("sys.argv", test_args):
        args = parse_args()
        assert args.non_recursive is True  # Should default to True
