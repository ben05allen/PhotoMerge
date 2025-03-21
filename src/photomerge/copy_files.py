from pathlib import Path
from shutil import copy2
from .logger import setup_logging

LOG_FILE = Path(__file__).parent / "logs" / "app.log"
LOGGER = setup_logging(LOG_FILE)


def copy_file(source_path: Path, destination_path: Path) -> bool:
    try:
        copy2(str(source_path.resolve()), str(destination_path.resolve()))
        return True
    except Exception as err:
        LOGGER.error(
            f"Error attempting to copy file {source_path} to {destination_path} - {err}"
        )
        return False
