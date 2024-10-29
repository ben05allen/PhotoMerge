import argparse
from pathlib import Path
import tomllib

from .copy_files import copy_file
from .get_files import find_files_with_extensions
from .hash_files import calculate_hash
from .logger import setup_logging


LOG_FILE = Path(__file__).parent / "logs" / "app.log"
DEFAULT_CONFIG = Path(__file__).parent / "config" / "config.toml"


def parse_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Process source, target, verbosity, recursive search and config arguments."
    )

    parser.add_argument(
        "--source", "-s", required=True, help="Source file or directory path"
    )
    parser.add_argument(
        "--target", "-t", required=True, help="Target directory path"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--non_recursive", "-n", action="store_false", help="Disable recursive search")
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


def main(args: argparse.ArgumentParser):
    config = get_config(args.config)
    allowed_extensions = config["extensions"]["allowed"]
    LOGGER.info(f"Allowed extensions: {allowed_extensions}")
    ignored_files = set(config["files"]["ignored"])
    LOGGER.info(f"Ignored files: {ignored_files}")

    data_dir = Path(args.source)
    LOGGER.info(f"Using source directory: {data_dir}")
    out_dir = Path(args.target)
    LOGGER.info(f"Using target directory: {out_dir}")
    
    # hash files, store hashes and file names in sets
    hashes = set()
    filenames = set()

    # check out_dir for any files
    for file in find_files_with_extensions(out_dir, allowed_extensions, is_recursive=False):
        hashes.add(calculate_hash(file))
        filenames.add(file.name)

    # process source files
    for file in find_files_with_extensions(data_dir, allowed_extensions, is_recursive=args.non_recursive):
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


if __name__ == "__main__":
    args = parse_args()
    LOGGER = setup_logging(LOG_FILE, verbose=args.verbose)

    main(args)