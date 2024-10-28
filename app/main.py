import argparse
from pathlib import Path
import tomllib

from copy_files import copy_file
from get_files import find_files_with_extensions
from hash_files import calculate_hash
from logger import setup_logging

parser = argparse.ArgumentParser(
    description="Process source, target, and config arguments."
)
parser.add_argument(
    "--source", "-s", required=True, help="Source file or directory path"
)
parser.add_argument(
    "--target", "-t", required=True, help="Target file or directory path"
)
# parser.add_argument("--verbose", "-v", help="Verbose output")
parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
parser.add_argument("--config", "-c", help="Configuration file path")
args = parser.parse_args()

log_file = Path(__file__).parent / "logs" / "app.log"
logger = setup_logging(log_file, verbose=args.verbose)

if args.config:
    config_source = args.config
    logger.info(f"Using config file: {config_source}")
else:
    config_source = Path(__file__).parent / "config" / "config.toml"
    logger.info("Using default config file")


with open(config_source, "rb") as f:
    config = tomllib.load(f)

allowed_extensions = config["extensions"]["allowed"]
ignored_files = set(config["files"]["ignored"])

data_dir = Path(args.source)
logger.info(f"Using source directory: {data_dir}")
out_dir = Path(args.target)
logger.info(f"Using target directory: {out_dir}")
hashes = set()
filenames = set()

# hash files, store hashes and file names in sets
for file in find_files_with_extensions(out_dir, allowed_extensions):
    hashes.add(calculate_hash(file))
    filenames.add(file.name)

# process source files
for file in find_files_with_extensions(data_dir, allowed_extensions):
    if file.name in ignored_files:
        logger.info(f"Ignoring file: {file.name}")
        continue
    file_hash = calculate_hash(file)
    if file_hash not in hashes:
        logger.info(f"New photo found: {file.name}")
        hashes.add(file_hash)

        if file.name not in filenames:
            filenames.add(file.name)
            copy_file(file, out_dir)
            logger.info(f"Saved: {file.name} in {out_dir}")
            continue

        idx = 1
        while (out_dir / (new_name := f"{file.stem}_{idx}{file.suffix}")).exists():
            idx += 1
        filenames.add(new_name)
        copy_file(file, out_dir / new_name)
        logger.info(f"Saved: {file.name} in {out_dir} as {new_name}")
