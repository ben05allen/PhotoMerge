from pathlib import Path
from shutil import copy2


def copy_file(source_path: Path, destination_path: Path) -> bool:
    try:
        copy2(str(source_path.resolve()), str(destination_path.resolve()))
        return True
    except Exception:
        return False
