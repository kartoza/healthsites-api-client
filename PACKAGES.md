# Healthsites API Client - Package Architecture

## Project Structure

```
healthsites-api-client/
├── healthsites/              # Main Python package
│   ├── __init__.py          # Package exports and version
│   ├── client.py            # Main API client implementation
│   └── exceptions.py        # Custom exception classes
├── tests/                    # Test suite
│   ├── __init__.py
│   └── test_client.py       # Client tests
├── docs/                     # MkDocs documentation
│   └── ...
├── pyproject.toml           # Project configuration
├── flake.nix                # Nix development environment
└── README.md                # Project readme
```

## Package Dependencies

### Runtime Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `httpx` | >=0.25.0 | Async HTTP client for API requests |

### Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | >=7.0 | Testing framework |
| `pytest-asyncio` | >=0.21 | Async test support |
| `pytest-cov` | >=4.0 | Coverage reporting |
| `respx` | >=0.20 | HTTP mocking for tests |
| `black` | >=23.0 | Code formatting |
| `ruff` | >=0.1 | Linting |
| `mypy` | >=1.0 | Type checking |
| `pre-commit` | >=3.0 | Pre-commit hooks |

### Documentation Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `mkdocs` | >=1.5 | Documentation generator |
| `mkdocs-material` | >=9.0 | Material theme |
| `mkdocstrings[python]` | >=0.24 | API documentation |

## Module Descriptions

### `healthsites/__init__.py`
Package entry point. Exports main classes and version information.

### `healthsites/client.py`
Contains:
- `HealthsitesClient`: Main async API client
- `HealthsitesClientSync`: Synchronous wrapper

Key methods:
- `list_facilities()`: Query facilities with filters
- `get_facility()`: Get specific facility
- `create_facility()`: Create new facility
- `update_facility()`: Update existing facility
- `get_statistics()`: Get facility statistics
- `download_shapefile()`: Download country shapefile
- `get_user()`: Get authenticated user details
- `list_endpoints()`: List all API endpoints

### `healthsites/exceptions.py`
Custom exceptions:
- `HealthsitesError`: Base exception
- `AuthenticationError`: 401 errors
- `NotFoundError`: 404 errors
- `RateLimitError`: 429 errors
- `ValidationError`: 400 errors

---

Made with love by [Kartoza](https://kartoza.com)
