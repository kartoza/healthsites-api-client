# Development Setup

## Prerequisites

- Python 3.10+
- Git
- Nix (optional but recommended)

## Setup with Nix

```bash
git clone https://github.com/kartoza/healthsites-api-client.git
cd healthsites-api-client
nix develop
```

## Setup with pip

```bash
git clone https://github.com/kartoza/healthsites-api-client.git
cd healthsites-api-client
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,docs]"
```

## Running Tests

```bash
# With Nix
nix run .#test

# With pytest
pytest tests/ -v
```

## Linting and Formatting

```bash
# Format code
nix run .#format
# or
black healthsites/ tests/
ruff check --fix healthsites/ tests/

# Run linters
nix run .#lint
# or
ruff check healthsites/ tests/
mypy healthsites/
```

## Building Documentation

```bash
# Build
nix run .#docs
# or
mkdocs build

# Serve locally
nix run .#docs-serve
# or
mkdocs serve
```

## Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

---

Made with love by [Kartoza](https://kartoza.com) | [Donate!](https://github.com/sponsors/kartoza) | [GitHub](https://github.com/kartoza/healthsites-api-client)
