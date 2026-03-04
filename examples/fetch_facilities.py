#!/usr/bin/env python3
"""
Example script demonstrating how to fetch health facilities.

Made with love by Kartoza | https://kartoza.com
"""

import asyncio
import os

from healthsites import HealthsitesClient


async def main():
    """Fetch health facilities from South Africa."""
    api_key = os.environ.get("HEALTHSITES_API_KEY", "your-api-key-here")

    async with HealthsitesClient(api_key=api_key) as client:
        print("Fetching health facilities from South Africa...")
        print()

        try:
            # Fetch first page of facilities
            result = await client.list_facilities(
                country="ZA",
                page=1,
                output="geojson",
            )

            features = result.get("features", [])
            print(f"Found {len(features)} facilities on page 1")
            print()

            # Print first 5 facilities
            for i, feature in enumerate(features[:5], 1):
                props = feature.get("properties", {})
                name = props.get("name", "Unknown")
                amenity = props.get("amenity", "Unknown")
                print(f"{i}. {name} ({amenity})")

            if len(features) > 5:
                print(f"   ... and {len(features) - 5} more")

        except Exception as e:
            print(f"Error: {e}")

        print()
        print("Made with love by Kartoza | https://kartoza.com")


if __name__ == "__main__":
    asyncio.run(main())
