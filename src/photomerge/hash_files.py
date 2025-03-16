import hashlib
from pathlib import Path


def calculate_hash(file_path: Path):
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()
