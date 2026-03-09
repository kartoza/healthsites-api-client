# Quick Start

## Get an API Key

1. Visit [healthsites.io](https://healthsites.io)
2. Create an account or log in
3. Navigate to your profile to get your API key

## Configuration

Set your credentials via environment variables (recommended):

```bash
export HEALTHSITES_API_KEY=your-api-key
export HEALTHSITES_URL=https://healthsites.io  # optional
```

Or use a `.env` file and load it before running:

```bash
HEALTHSITES_API_KEY=your-api-key
HEALTHSITES_URL=https://healthsites.io
```

## Async Usage (Recommended)

```python
import asyncio
import os
from healthsites import HealthsitesClient

async def main():
    api_key = os.environ.get("HEALTHSITES_API_KEY")
    async with HealthsitesClient(api_key=api_key) as client:
        facilities = await client.list_facilities(country="South Africa", page=1)
        print(facilities)

asyncio.run(main())
```

## Synchronous Usage

```python
import os
from healthsites.client import HealthsitesClientSync

api_key = os.environ.get("HEALTHSITES_API_KEY")
client = HealthsitesClientSync(api_key=api_key)
facilities = client.list_facilities(country="South Africa", page=1)
print(facilities)
client.close()
```

## Create a Facility

```python
import asyncio
import os
from healthsites import HealthsitesClient, Tag

async def main():
    api_key = os.environ.get("HEALTHSITES_API_KEY")
    async with HealthsitesClient(api_key=api_key) as client:
        tag = Tag(
            amenity="clinic",
            healthcare=["doctor"],
            name="My Clinic",
            operator_type="public",
            operational_status="operational",
        )
        response = await client.create_facility(
            lat=47.287,
            lon=8.765,
            tag=tag,
            comment="Adding new clinic",
            source="survey",
        )
        print(response)

asyncio.run(main())
```

## List Available Endpoints

```python
import os
from healthsites import HealthsitesClient

api_key = os.environ.get("HEALTHSITES_API_KEY")
client = HealthsitesClient(api_key=api_key)
for endpoint in client.list_endpoints():
    print(f"{endpoint['method']} {endpoint['path']}")
    print(f"  {endpoint['description']}")
    print(f"  Function: {endpoint['function']}")
```

---

Made with love by [Kartoza](https://kartoza.com) | [Donate!](https://github.com/sponsors/kartoza) | [GitHub](https://github.com/kartoza/healthsites-api-client)