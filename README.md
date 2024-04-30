# BrokenLinks

BrokenLinks is a Python project used to find all occurrences of broken or external links on a website. It generates a report in CSV format.

# Usage

```bash
    pip install -r requirements.txt
    python brokenlinks.py --url=https://example.com
```

## Ignore URL Patterns

You can specify a regex to exclude certain URL Patterns. This can be done using the `--ignore` command line option. The format is a comma
separated list of regex patterns to exclude.

## Report Path

The default output path is `output.csv`. You can change the path of the output file using the  `--output` command line option.

# Development

The requirements for development are located in `requirements-dev.txt`. Install them using pip

```bash
    pip install -r requirements-dev.txt
```

## Pre-commit Installation

This project uses pre-commit to run various checking and formatting tools before committing a change. Install pre-commit using

```bash
    pre-commit install
```

after installing the dev dependencies.
