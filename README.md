# PhotoMerge

For Louis's 20TB of internet cat photos

## Installation

Clone from Github

Install `uv` (if not already)

```[bash]
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Load dependencies and python version

```[bash]
uv sync
```

## Usage

```[bash]
uv run photomerge [-h] --source SOURCE --target TARGET [--verbose] [--config CONFIG]

Process source, target, and config arguments.

options:
  -h, --help            show this help message and exit
  --source SOURCE, -s SOURCE
                        Source file or directory path
  --target TARGET, -t TARGET
                        Target file or directory path
  --verbose, -v         Verbose output
  --config CONFIG, -c CONFIG
                        Configuration file path
```

## Tests

```[bash]
uv run pytest
```
