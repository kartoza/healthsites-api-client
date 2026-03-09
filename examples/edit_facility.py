#!/usr/bin/env python3
"""
Example script demonstrating how to edit a health facility.

Made with love by Kartoza | https://kartoza.com
"""

import asyncio
import os

from healthsites import HealthsitesClient, Tag


async def main():
    """Update an existing health facility."""
    api_key = os.environ.get("HEALTHSITES_API_KEY", "your-api-key-here")

    # OSM type and ID of the facility to update
    osm_type = "node"
    osm_id = 123456789

    async with HealthsitesClient(api_key=api_key) as client:
        print(f"Updating facility {osm_type}/{osm_id}...")
        print()

        tag = Tag(
            amenity="clinic",
            healthcare=["doctor"],
            name="Updated Clinic Name",
            operator="Ministry of Health",
            operator_type="public",
            operational_status="operational",
            opening_hours="Mo-Fr 08:00-17:00",
            contact_number="+1-555-0100",
            beds=60,
            staff_doctors=7,
            staff_nurses=25,
            wheelchair=True,
            emergency=True,
            water_source="water_works",
            electricity="grid",
            addr_street="Main Street",
            addr_city="Example City",
        )

        print("Tag payload:")
        for key, value in tag.to_dict().items():
            print(f"  {key}: {value}")
        print()

        try:
            response = await client.update_facility(
                osm_type=osm_type,
                osm_id=osm_id,
                lat=47.287,
                lon=8.765,
                tag=tag,
                comment="Updating clinic details",
                source="survey",
                hashtags="#healthsites;#example",
            )
            print(f"Updated facility: {response}")
        except Exception as e:
            print(f"Error: {e}")

        print()
        print("Made with love by Kartoza | https://kartoza.com")


if __name__ == "__main__":
    asyncio.run(main())