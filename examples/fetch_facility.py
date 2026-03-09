#!/usr/bin/env python3
"""
Example script demonstrating how to fetch a single health facility.

Made with love by Kartoza | https://kartoza.com
"""

import argparse
import asyncio
import os

from healthsites import HealthsitesClient


async def main():
    """Fetch a single health facility by OSM type and ID."""
    parser = argparse.ArgumentParser(description="Fetch a health facility by OSM type and ID.")
    parser.add_argument("--osm_type", choices=["node", "way"], required=True, help="OSM element type")
    parser.add_argument("--osm_id", type=int, required=True, help="OSM element ID")
    args = parser.parse_args()

    api_key = os.environ.get("HEALTHSITES_API_KEY", "your-api-key-here")
    osm_type = args.osm_type
    osm_id = args.osm_id

    async with HealthsitesClient(api_key=api_key) as client:
        print(f"Fetching facility {osm_type}/{osm_id}...")
        print()

        try:
            response = await client.get_facility(
                osm_type=osm_type,
                osm_id=osm_id,
            )
            print(f"Facility: {response}")
        except Exception as e:
            print(f"Error: {e}")

        print()
        print("Made with love by Kartoza | https://kartoza.com")


if __name__ == "__main__":
    asyncio.run(main())