from shutil import copy2


def copy_file(source_path: str, destination_path: str) -> bool:
    try:
        copy2(source_path, destination_path)
        return True
    except (IOError, OSError, FileNotFoundError):
        return False
