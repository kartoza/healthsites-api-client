# Examples

## List Facilities with Filters

```python
import asyncio
import os

from healthsites import HealthsitesClient


async def main():
    async with HealthsitesClient(
            api_key=os.environ.get("HEALTHSITES_API_KEY")) as client:
        # Filter by country
        facilities = await client.list_facilities(
            country="South Africa",
            page=1,
            output="geojson",
        )

        # Filter by bounding box
        facilities = await client.list_facilities(
            extent="18.0,-34.5,19.0,-33.5",
            page=1,
        )

        # Filter by Unix timestamp range
        facilities = await client.list_facilities(
            from_timestamp=1700000000,
            to_timestamp=1710000000,
            page=1,
        )


asyncio.run(main())
```

## Create a Facility

```python
import asyncio
import os
from healthsites import HealthsitesClient, Tag

async def main():
    async with HealthsitesClient(api_key=os.environ.get("HEALTHSITES_API_KEY")) as client:
        tag = Tag(
            amenity="clinic",
            healthcare=["doctor"],
            name="Example Clinic",
            operator="Ministry of Health",
            operator_type="public",
            operational_status="operational",
            opening_hours="Mo-Fr 08:00-17:00",
            contact_number="+1-555-0100",
            beds=50,
            staff_doctors=5,
            staff_nurses=20,
            wheelchair=True,
            emergency=False,
            water_source="water_works",
            electricity="grid",
            addr_street="Main Street",
            addr_city="Example City",
        )

        response = await client.create_facility(
            lat=47.287,
            lon=8.765,
            tag=tag,
            comment="Adding example clinic",
            source="survey",
            hashtags="#healthsites;#example",
        )
        print(response)

asyncio.run(main())
```

## Get a Facility

```python
import asyncio
import os
from healthsites import HealthsitesClient

async def main():
    async with HealthsitesClient(api_key=os.environ.get("HEALTHSITES_API_KEY")) as client:
        facility = await client.get_facility(osm_type="node", osm_id=123456789)
        print(facility)

asyncio.run(main())
```

## Update a Facility

```python
import asyncio
import os
from healthsites import HealthsitesClient, Tag

async def main():
    async with HealthsitesClient(api_key=os.environ.get("HEALTHSITES_API_KEY")) as client:
        tag = Tag(
            amenity="clinic",
            healthcare=["doctor"],
            name="Updated Clinic Name",
            beds=60,
            staff_doctors=7,
            staff_nurses=25,
            emergency=True,
        )

        response = await client.update_facility(
            osm_type="node",
            osm_id=123456789,
            lat=47.287,
            lon=8.765,
            tag=tag,
            comment="Updating clinic details",
            source="survey",
        )
        print(response)

asyncio.run(main())
```

## Get Facility Statistics

```python
import asyncio
import os
from healthsites import HealthsitesClient

async def main():
    async with HealthsitesClient(api_key=os.environ.get("HEALTHSITES_API_KEY")) as client:
        stats = await client.get_statistics(country="South Africa")
        print(stats)

asyncio.run(main())
```

## Download Shapefile

```python
import asyncio
import os
from healthsites import HealthsitesClient

async def main():
    async with HealthsitesClient(api_key=os.environ.get("HEALTHSITES_API_KEY")) as client:
        path = await client.download_shapefile(
            country="South Africa",
            output_path="south_africa_health.zip",
        )
        print(f"Saved to: {path}")

asyncio.run(main())
```

## Error Handling

```python
import asyncio
import os
from healthsites import HealthsitesClient
from healthsites.exceptions import AuthenticationError, NotFoundError, RateLimitError

async def main():
    async with HealthsitesClient(api_key=os.environ.get("HEALTHSITES_API_KEY")) as client:
        try:
            facility = await client.get_facility(osm_type="node", osm_id=123456)
        except AuthenticationError as e:
            print(f"Authentication failed: {e.message}")
        except NotFoundError as e:
            print(f"Facility not found: {e.message}")
        except RateLimitError as e:
            print(f"Rate limit exceeded, try again later: {e.message}")

asyncio.run(main())
```

---

Made with love by [Kartoza](https://kartoza.com) | [Donate!](https://github.com/sponsors/kartoza) | [GitHub](https://github.com/kartoza/healthsites-api-client)