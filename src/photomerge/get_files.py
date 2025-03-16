from collections.abc import Generator, Iterable
from pathlib import Path


def find_files_with_extensions(
    folder_path: str | Path, extensions: Iterable[str], is_recursive: bool = True
) -> Generator[Path, None, None]:
    extensions = set(ext.lower() for ext in extensions)

    if isinstance(folder_path, str):
        folder_path = Path(folder_path)

    if is_recursive:
        folder_search = folder_path.rglob("*")
    else:
        folder_search = folder_path.iterdir()

    for file in folder_search:
        if file.suffix.lower() in extensions:
            yield file.resolve()
