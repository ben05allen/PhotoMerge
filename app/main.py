import argparse
from pathlib import Path
import tomllib

from copy_files import copy_file
from get_files import find_files_with_extensions
from hash_files import calculate_hash
from logger import setup_logging, add_console_handler


DEFAULT_CONFIG = Path(__file__).parent / "config" / "config.toml"
LOG_FILE = Path(__file__).parent / "logs" / "app.log"
LOGGER = setup_logging(LOG_FILE)


def parse_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Process source, target, verbosity, recursive search and config arguments."
    )

    parser.add_argument(
        "--source", "-s", required=True, help="Source file or directory path"
    )
    parser.add_argument("--target", "-t", required=True, help="Target directory path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--non_recursive", "-n", action="store_false", help="Disable recursive search"
    )
    parser.add_argument("--config", "-c", help="Configuration file path")

    return parser.parse_args()


def get_config(cli_path: str | None) -> dict | None:
    if cli_path:
        config_path = Path(cli_path)
        LOGGER.info(f"Using custom config file: {config_path}")
    else:
        config_path = DEFAULT_CONFIG
        LOGGER.info("Using default config file")

    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
        return config
    except FileNotFoundError:
        LOGGER.error(f"Config file not found: {config_path}")
        return None


def initialize_paths(source: str, target: str) -> tuple[Path, Path]:
    source_dir = Path(source)
    if not source_dir.exists():
        LOGGER.error(f"Source directory does not exist: {source_dir}")
        raise FileNotFoundError(f"Source directory does not exist: {source_dir}")

    target_dir = Path(target)
    if not target_dir.exists():
        LOGGER.error(f"Target directory does not exist: {target_dir}")
        raise FileNotFoundError(f"Target directory does not exist: {target_dir}")

    return source_dir, target_dir


def initialize_hashes(out_dir: Path) -> tuple[set, set]:
    hashes = set()
    filenames = set()

    for file in find_files_with_extensions(out_dir, is_recursive=False):
        hashes.add(calculate_hash(file))
        filenames.add(file.name)

    return hashes, filenames


def process_files(
    data_dir: Path,
    out_dir: Path,
    hashes: set[str],
    filenames: set[str],
    allowed_extensions: set[str],
    ignored_files: set,
    is_recursive: bool,
):
    # process source files
    for file in find_files_with_extensions(
        data_dir, allowed_extensions, is_recursive=is_recursive
    ):
        if file.name in ignored_files:
            LOGGER.info(f"Ignoring file: {file.name}")
            continue

        file_hash = calculate_hash(file)
        if file_hash not in hashes:
            LOGGER.info(f"New photo found: {file.name}")
            hashes.add(file_hash)

            if file.name not in filenames:
                filenames.add(file.name)
                suceeded = copy_file(file, out_dir)
                if not suceeded:
                    LOGGER.error(f"Failed to copy file: {file.name}")
                else:
                    LOGGER.info(f"Saved: {file.name} in {out_dir}")
                continue

            idx = 1
            while (out_dir / (new_name := f"{file.stem}_{idx}{file.suffix}")).exists():
                idx += 1
            filenames.add(new_name)
            suceeded = copy_file(file, out_dir / new_name)
            if not suceeded:
                LOGGER.error(f"Failed to copy file: {file.name}")
            else:
                LOGGER.info(f"Saved: {file.name} in {out_dir} as {new_name}")


def main(args: argparse.ArgumentParser):
    global LOGGER
    if args.verbose:
        add_console_handler(LOGGER)

    config = get_config(args.config)
    is_recursive = args.non_recursive
    allowed_extensions = set(config["extensions"]["allowed"])
    LOGGER.info(f"Allowed extensions: {allowed_extensions}")
    ignored_files = set(config["files"]["ignored"])
    LOGGER.info(f"Ignored files: {ignored_files}")

    data_dir, out_dir = initialize_paths(args.source, args.target)

    hashes, filenames = initialize_hashes(out_dir)

    process_files(
        data_dir=data_dir,
        out_dir=out_dir,
        hashes=hashes,
        filenames=filenames,
        allowed_extensions=allowed_extensions,
        ignored_files=ignored_files,
        is_recursive=is_recursive,
    )


if __name__ == "__main__":
    args = parse_args()

    main(args)
