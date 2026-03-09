#!/usr/bin/env python3
"""
Example script demonstrating how to create a health facility.

Made with love by Kartoza | https://kartoza.com
"""

import asyncio
import os

from healthsites import HealthsitesClient, Tag


async def main():
    """Create a health facility."""
    api_key = os.environ.get("HEALTHSITES_API_KEY", "your-api-key-here")

    async with HealthsitesClient(api_key=api_key) as client:
        print("Creating a new health facility...")
        print()

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

        print("Tag payload:")
        for key, value in tag.to_dict().items():
            print(f"  {key}: {value}")
        print()

        try:
            response = await client.create_facility(
                lat=47.287,
                lon=8.765,
                tag=tag,
                comment="Adding example clinic",
                source="survey",
                hashtags="#healthsites;#example",
            )
            print(f"Created facility: {response}")
        except Exception as e:
            print(f"Error: {e}")

        print()
        print("Made with love by Kartoza | https://kartoza.com")


if __name__ == "__main__":
    asyncio.run(main())