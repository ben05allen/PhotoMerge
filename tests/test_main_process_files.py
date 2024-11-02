from pathlib import Path
from app.main import process_files


# def test_process_files_ignores_file_in_ignored_files(mocker):
#     mock_logger = mocker.patch("app.main.LOGGER")
#     mock_find_files = mocker.patch(  # noqa: F841
#         "app.main.find_files_with_extensions", return_value=[Path("ignored_file.jpg")]
#     )
#     mock_calculate_hash = mocker.patch("app.main.calculate_hash")

#     process_files(
#         data_dir=Path("data_dir"),
#         out_dir=Path("out_dir"),
#         hashes=set(),
#         filenames=set(),
#         allowed_extensions={".jpg", ".png"},
#         ignored_files={"ignored_file.jpg"},
#         is_recursive=True,
#     )

#     # Assert that ignored file is logged as ignored and not processed
#     mock_logger.info.assert_any_call("Ignoring file: ignored_file.jpg")
#     mock_calculate_hash.assert_not_called()


def test_process_files_new_file_copied_successfully(mocker):
    mock_logger = mocker.patch("app.main.LOGGER")
    mock_find_files = mocker.patch(  # noqa: F841
        "app.main.find_files_with_extensions", return_value=[Path("new_file.jpg")]
    )
    mock_calculate_hash = mocker.patch("app.main.calculate_hash", return_value="hash1")  # noqa: F841
    mock_copy_file = mocker.patch("app.main.copy_file", return_value=True)

    hashes = set()
    filenames = set()
    process_files(
        data_dir=Path("data_dir"),
        out_dir=Path("out_dir"),
        hashes=hashes,
        filenames=filenames,
        allowed_extensions={".jpg", ".png"},
        ignored_files=set(),
        is_recursive=True,
    )

    # Check that the file was processed, copied, and logged
    assert "hash1" in hashes
    assert "new_file.jpg" in filenames
    mock_copy_file.assert_called_once_with(Path("new_file.jpg"), Path("out_dir"))
    mock_logger.info.assert_any_call("New photo found: new_file.jpg")
    mock_logger.info.assert_any_call("Saved: new_file.jpg in out_dir")


def test_process_files_copy_failure(mocker):
    mock_logger = mocker.patch("app.main.LOGGER")
    mock_find_files = mocker.patch(  # noqa: F841
        "app.main.find_files_with_extensions", return_value=[Path("file_fail.jpg")]
    )
    mock_calculate_hash = mocker.patch(  # noqa: F841
        "app.main.calculate_hash", return_value="hash_fail"
    )
    mock_copy_file = mocker.patch("app.main.copy_file", return_value=False)  # noqa: F841

    process_files(
        data_dir=Path("data_dir"),
        out_dir=Path("out_dir"),
        hashes=set(),
        filenames=set(),
        allowed_extensions={".jpg", ".png"},
        ignored_files=set(),
        is_recursive=True,
    )

    # Check that the copy failure is logged
    mock_logger.error.assert_any_call("Failed to copy file: file_fail.jpg")


# def test_process_files_duplicate_file_name(mocker):
#     mock_logger = mocker.patch("app.main.LOGGER")
#     mock_find_files = mocker.patch(  # noqa: F841
#         "app.main.find_files_with_extensions", return_value=[Path("duplicate_file.jpg")]
#     )
#     mock_calculate_hash = mocker.patch(  # noqa: F841
#         "app.main.calculate_hash", return_value="duplicate_hash"
#     )
#     mock_copy_file = mocker.patch(
#         "app.main.copy_file", side_effect=[False, True]
#     )  # First copy fails

#     # Mock existence check to simulate duplicate file names
#     mock_exists = mocker.patch("pathlib.Path.exists", side_effect=[True, False])  # noqa: F841

#     filenames = {"duplicate_file.jpg"}
#     process_files(
#         data_dir=Path("data_dir"),
#         out_dir=Path("out_dir"),
#         hashes=set(),
#         filenames=filenames,
#         allowed_extensions={".jpg", ".png"},
#         ignored_files=set(),
#         is_recursive=True,
#     )

#     # Check that the file was copied with a new name
#     new_name = "duplicate_file_1.jpg"
#     mock_copy_file.assert_called_with(
#         Path("duplicate_file.jpg"), Path("out_dir") / new_name
#     )
#     assert new_name in filenames
#     mock_logger.info.assert_any_call(
#         f"Saved: duplicate_file.jpg in out_dir as {new_name}"
#     )


def test_process_files_respects_is_recursive(mocker):
    mock_find_files = mocker.patch(
        "app.main.find_files_with_extensions", return_value=[]
    )
    process_files(
        data_dir=Path("data_dir"),
        out_dir=Path("out_dir"),
        hashes=set(),
        filenames=set(),
        allowed_extensions={".jpg", ".png"},
        ignored_files=set(),
        is_recursive=False,
    )

    # Verify that `is_recursive` was passed correctly to `find_files_with_extensions`
    mock_find_files.assert_called_once_with(
        Path("data_dir"), {".jpg", ".png"}, is_recursive=False
    )
