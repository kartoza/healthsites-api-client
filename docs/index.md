# Healthsites API Client

A Python client library for the [Healthsites.io](https://healthsites.io) API v3.

Healthsites.io is an open data repository of health facility locations, making health facility information more accessible to support better health outcomes.

## Features

- Full async support with `httpx`
- Synchronous wrapper for convenience
- Type hints throughout
- Comprehensive error handling
- Easy pagination handling

## Quick Start

```python
import asyncio
from healthsites import HealthsitesClient

async def main():
    async with HealthsitesClient(api_key="your-api-key") as client:
        # List all endpoints
        endpoints = client.list_endpoints()
        for ep in endpoints:
            print(f"{ep['method']} {ep['path']}")

        # List facilities in South Africa
        facilities = await client.list_facilities(country="ZA", page=1)
        print(facilities)

asyncio.run(main())
```

## Installation

```bash
pip install healthsites-api-client
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/facilities/` | List facilities |
| POST | `/api/v3/facilities/` | Create facility |
| GET | `/api/v3/facilities/statistic/` | Get statistics |
| GET | `/api/v3/facilities/{osm_type}/{osm_id}` | Get facility |
| POST | `/api/v3/facilities/{osm_type}/{osm_id}` | Update facility |
| GET | `/api/v3/shapefile/{country}` | Download shapefile |
| GET | `/api/v3/user/` | Get user details |

---

Made with love by [Kartoza](https://kartoza.com) | [Donate!](https://github.com/sponsors/kartoza) | [GitHub](https://github.com/kartoza/healthsites-api-client)
