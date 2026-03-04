# Examples

## List Facilities with Filters

```python
import asyncio
from healthsites import HealthsitesClient

async def main():
    async with HealthsitesClient(api_key="your-api-key") as client:
        # Filter by country
        facilities = await client.list_facilities(
            country="ZA",
            page=1,
            output="geojson"
        )

        # Filter by bounding box
        facilities = await client.list_facilities(
            extent="18.0,-34.5,19.0,-33.5",
            page=1
        )

        # Filter by date range
        facilities = await client.list_facilities(
            from_date="2024-01-01",
            to_date="2024-12-31",
            page=1
        )

asyncio.run(main())
```

## Get Facility Statistics

```python
import asyncio
from healthsites import HealthsitesClient

async def main():
    async with HealthsitesClient(api_key="your-api-key") as client:
        stats = await client.get_statistics(country="ZA")
        print(f"Total facilities: {stats}")

asyncio.run(main())
```

## Download Shapefile

```python
import asyncio
from healthsites import HealthsitesClient

async def main():
    async with HealthsitesClient(api_key="your-api-key") as client:
        # Save to file
        path = await client.download_shapefile(
            country="ZA",
            output_path="south_africa_health.zip"
        )
        print(f"Saved to: {path}")

asyncio.run(main())
```

## Error Handling

```python
import asyncio
from healthsites import (
    HealthsitesClient,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
)

async def main():
    async with HealthsitesClient(api_key="your-api-key") as client:
        try:
            facility = await client.get_facility("node", 123456)
        except AuthenticationError:
            print("Invalid API key")
        except NotFoundError:
            print("Facility not found")
        except RateLimitError:
            print("Rate limit exceeded, try again later")

asyncio.run(main())
```

---

Made with love by [Kartoza](https://kartoza.com) | [Donate!](https://github.com/sponsors/kartoza) | [GitHub](https://github.com/kartoza/healthsites-api-client)
