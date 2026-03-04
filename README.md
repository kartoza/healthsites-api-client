# Healthsites API Client

[![PyPI version](https://badge.fury.io/py/healthsites-api-client.svg)](https://badge.fury.io/py/healthsites-api-client)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A Python client library for the [Healthsites.io](https://healthsites.io) API v3.

Healthsites.io is an open data repository of health facility locations, making health facility information more accessible to support better health outcomes.

## Features

- Full async support with `httpx`
- Synchronous wrapper for convenience
- Type hints throughout
- Comprehensive error handling
- Easy pagination handling

## Installation

```bash
pip install healthsites-api-client
```

Or with Nix:

```bash
nix develop
```

## Quick Start

### Async Usage (Recommended)

```python
import asyncio
from healthsites import HealthsitesClient

async def main():
    async with HealthsitesClient(api_key="your-api-key") as client:
        # List all endpoints
        endpoints = client.list_endpoints()
        for ep in endpoints:
            print(f"{ep['method']} {ep['path']} - {ep['description']}")

        # List facilities in South Africa
        facilities = await client.list_facilities(country="ZA", page=1)
        print(f"Found {len(facilities.get('features', []))} facilities")

        # Get statistics
        stats = await client.get_statistics(country="ZA")
        print(f"Statistics: {stats}")

        # Get a specific facility
        facility = await client.get_facility(osm_type="node", osm_id=123456)
        print(f"Facility: {facility}")

asyncio.run(main())
```

### Synchronous Usage

```python
from healthsites.client import HealthsitesClientSync

client = HealthsitesClientSync(api_key="your-api-key")

# List endpoints
for ep in client.list_endpoints():
    print(f"{ep['method']} {ep['path']}")

# Get facilities
facilities = client.list_facilities(country="ZA", page=1)
print(facilities)

client.close()
```

## API Endpoints

| Method | Endpoint | Description | Function |
|--------|----------|-------------|----------|
| GET | `/api/v3/facilities/` | List facilities | `list_facilities()` |
| POST | `/api/v3/facilities/` | Create facility | `create_facility()` |
| GET | `/api/v3/facilities/statistic/` | Get statistics | `get_statistics()` |
| GET | `/api/v3/facilities/{osm_type}/{osm_id}` | Get facility | `get_facility()` |
| POST | `/api/v3/facilities/{osm_type}/{osm_id}` | Update facility | `update_facility()` |
| GET | `/api/v3/shapefile/{country}` | Download shapefile | `download_shapefile()` |
| GET | `/api/v3/user/` | Get user details | `get_user()` |

## Documentation

Full documentation is available at [https://kartoza.github.io/healthsites-api-client](https://kartoza.github.io/healthsites-api-client)

## Development

```bash
# Enter development environment
nix develop

# Run tests
nix run .#test

# Format code
nix run .#format

# Run linters
nix run .#lint

# Build docs
nix run .#docs
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with love by [Kartoza](https://kartoza.com) | [Donate!](https://github.com/sponsors/kartoza) | [GitHub](https://github.com/kartoza/healthsites-api-client)
