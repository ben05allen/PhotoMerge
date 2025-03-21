import hashlib
from pathlib import Path


def calculate_hash(file_path: Path):
    try:
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    except Exception as e:
        raise e
