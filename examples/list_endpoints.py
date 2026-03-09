#!/usr/bin/env python3
"""
Example script demonstrating how to list all Healthsites API endpoints.

Made with love by Kartoza | https://kartoza.com
"""

import os

from healthsites import HealthsitesClient


def main():
    """List all available API endpoints."""
    api_key = os.environ.get("HEALTHSITES_API_KEY", "your-api-key-here")

    client = HealthsitesClient(api_key=api_key)

    print("Healthsites.io API v3 Endpoints")
    print("=" * 60)
    print()

    endpoints = client.list_endpoints()

    for ep in endpoints:
        print(f"{ep['method']:6} {ep['path']}")
        print(f"       Description: {ep['description']}")
        print(f"       Function:    {ep['function']}")
        print()

    print("=" * 60)
    print(f"Total endpoints: {len(endpoints)}")
    print()
    print("Made with love by Kartoza | https://kartoza.com")


if __name__ == "__main__":
    main()
