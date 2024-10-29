from pathlib import Path


def find_files_with_extensions(folder_path, extensions, is_recursive: bool = True):
    extensions = set(ext.lower() for ext in extensions)

    # Recursively search for files with the specified extensions
    if is_recursive:
        for file in Path(folder_path).rglob("*"):
            if file.suffix.lower() in extensions:
                yield file.resolve()
    else:
        for file in Path(folder_path).iterdir():
            if file.suffix.lower() in extensions:
                yield file.resolve()
    