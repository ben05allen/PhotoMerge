from pathlib import Path


def find_files_with_extensions(folder_path, extensions):
    extensions = set(ext.lower() for ext in extensions)

    # Recursively search for files with the specified extensions
    for file in Path(folder_path).rglob("*"):
        if file.suffix.lower() in extensions:
            yield file.resolve()
