# pyright: basic


import pytest
from unittest.mock import patch

from photomerge import app_arg_parser


def test_parse_args_required_arguments():
    # Simulate command-line arguments
    test_args = "prog --source source_path --target target_path".split()

    with patch("sys.argv", test_args):
        args = app_arg_parser().parse_args()
        assert args.source == "source_path"
        assert args.target == "target_path"
        assert args.verbose is False  # Default when not specified
        assert args.non_recursive is True  # Default when not specified


def test_parse_args_short_flag_names():
    test_args = "prog -s source_path -t target_path -v -n -c config_path".split()

    with patch("sys.argv", test_args):
        args = app_arg_parser().parse_args()
        assert args.source == "source_path"
        assert args.target == "target_path"
        assert args.verbose is True  # Set by -v flag
        assert args.non_recursive is False  # Set by -n flag
        assert args.config == "config_path"


def test_parse_args_all_arguments():
    test_args = (
        "prog --source source_path --target target_path --verbose "
        "--non_recursive --config config_path"
    ).split()

    with patch("sys.argv", test_args):
        args = app_arg_parser().parse_args()
        assert args.source == "source_path"
        assert args.target == "target_path"
        assert args.verbose is True  # Set by --verbose flag
        assert args.non_recursive is False  # Set by --non_recursive flag
        assert args.config == "config_path"


def test_parse_args_missing_required_arguments():
    test_args = "prog --source source_path".split()

    with patch("sys.argv", test_args), pytest.raises(SystemExit):
        app_arg_parser().parse_args()  # Should exit due to missing --target
