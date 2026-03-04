"""
Healthsites API Client.

Provides async access to the Healthsites.io API v3.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Literal

import httpx

from healthsites.exceptions import (
    AuthenticationError,
    HealthsitesError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


OSMType = Literal["node", "way", "relation"]
OutputFormat = Literal["json", "geojson", "xml"]
TagFormat = Literal["osm", "hxl"]


class HealthsitesClient:
    """
    Async client for the Healthsites.io API v3.

    Example:
        async with HealthsitesClient(api_key="your-api-key") as client:
            facilities = await client.list_facilities(country="ZA", page=1)
            print(facilities)
    """

    BASE_URL = "https://healthsites.io/api/v3"

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        timeout: float = 30.0,
    ):
        """
        Initialize the Healthsites API client.

        Args:
            api_key: Your Healthsites API key.
            base_url: Optional custom base URL for the API.
            timeout: Request timeout in seconds (default: 30.0).
        """
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> HealthsitesClient:
        """Enter async context manager."""
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context manager."""
        if self._client:
            await self._client.aclose()
            self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        """Get the HTTP client, creating one if necessary."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    def _handle_response(self, response: httpx.Response) -> Any:
        """Handle API response and raise appropriate exceptions."""
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise AuthenticationError()
        elif response.status_code == 404:
            raise NotFoundError()
        elif response.status_code == 429:
            raise RateLimitError()
        elif response.status_code == 400:
            try:
                detail = response.json().get("detail", "Validation error")
            except Exception:
                detail = response.text
            raise ValidationError(str(detail))
        else:
            raise HealthsitesError(
                f"API error: {response.text}",
                status_code=response.status_code,
            )

    async def _get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Make a GET request to the API."""
        params = params or {}
        params["api-key"] = self.api_key
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        url = f"{self.base_url}{endpoint}"
        response = await self.client.get(url, params=params)
        return self._handle_response(response)

    async def _post(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Make a POST request to the API."""
        params = params or {}
        params["api-key"] = self.api_key
        params = {k: v for k, v in params.items() if v is not None}

        url = f"{self.base_url}{endpoint}"
        response = await self.client.post(url, json=data, params=params)
        return self._handle_response(response)

    # -------------------------------------------------------------------------
    # Facilities Endpoints
    # -------------------------------------------------------------------------

    async def list_facilities(
        self,
        page: int = 1,
        country: str | None = None,
        extent: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        flat_properties: bool | None = None,
        tag_format: TagFormat | None = None,
        output: OutputFormat | None = None,
    ) -> dict[str, Any]:
        """
        List facilities with optional filtering.

        Args:
            page: Page number for pagination (required).
            country: Filter by country code (e.g., "ZA" for South Africa).
            extent: Bounding box as "min_lon,min_lat,max_lon,max_lat".
            from_date: Filter facilities updated from this date (ISO format).
            to_date: Filter facilities updated to this date (ISO format).
            flat_properties: Return flattened properties structure.
            tag_format: Tag format ("osm" or "hxl").
            output: Output format ("json", "geojson", or "xml").

        Returns:
            Dictionary containing facility data and pagination info.
        """
        params = {
            "page": page,
            "country": country,
            "extent": extent,
            "from": from_date,
            "to": to_date,
            "flat-properties": flat_properties,
            "tag-format": tag_format,
            "output": output,
        }
        return await self._get("/facilities/", params)

    async def create_facility(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Create a new facility.

        Args:
            data: Facility data including geometry and properties.

        Returns:
            Created facility data.
        """
        return await self._post("/facilities/", data=data)

    async def get_facility(
        self,
        osm_type: OSMType,
        osm_id: int,
    ) -> dict[str, Any]:
        """
        Get a specific facility by OSM type and ID.

        Args:
            osm_type: OSM element type ("node", "way", or "relation").
            osm_id: OSM element ID.

        Returns:
            Facility detail data.
        """
        return await self._get(f"/facilities/{osm_type}/{osm_id}")

    async def update_facility(
        self,
        osm_type: OSMType,
        osm_id: int,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Update an existing facility.

        Args:
            osm_type: OSM element type ("node", "way", or "relation").
            osm_id: OSM element ID.
            data: Updated facility data.

        Returns:
            Updated facility data.
        """
        return await self._post(f"/facilities/{osm_type}/{osm_id}", data=data)

    async def get_statistics(
        self,
        country: str | None = None,
        extent: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        flat_properties: bool | None = None,
        tag_format: TagFormat | None = None,
        output: OutputFormat | None = None,
    ) -> dict[str, Any]:
        """
        Get facility statistics.

        Args:
            country: Filter by country code (e.g., "ZA" for South Africa).
            extent: Bounding box as "min_lon,min_lat,max_lon,max_lat".
            from_date: Filter facilities updated from this date (ISO format).
            to_date: Filter facilities updated to this date (ISO format).
            flat_properties: Return flattened properties structure.
            tag_format: Tag format ("osm" or "hxl").
            output: Output format ("json", "geojson", or "xml").

        Returns:
            Statistics data for facilities.
        """
        params = {
            "country": country,
            "extent": extent,
            "from": from_date,
            "to": to_date,
            "flat-properties": flat_properties,
            "tag-format": tag_format,
            "output": output,
        }
        return await self._get("/facilities/statistic/", params)

    # -------------------------------------------------------------------------
    # Shapefile Endpoint
    # -------------------------------------------------------------------------

    async def download_shapefile(
        self,
        country: str,
        output_path: str | Path | None = None,
    ) -> bytes | Path:
        """
        Download shapefile data for a country.

        Args:
            country: Country code (e.g., "ZA" for South Africa).
            output_path: Optional path to save the shapefile. If not provided,
                        returns the raw bytes.

        Returns:
            Path to the saved file if output_path is provided, otherwise bytes.
        """
        url = f"{self.base_url}/shapefile/{country}"
        params = {"api-key": self.api_key}

        response = await self.client.get(url, params=params)

        if response.status_code != 200:
            self._handle_response(response)

        if output_path:
            output_path = Path(output_path)
            output_path.write_bytes(response.content)
            return output_path

        return response.content

    # -------------------------------------------------------------------------
    # User Endpoint
    # -------------------------------------------------------------------------

    async def get_user(self) -> dict[str, Any]:
        """
        Get the currently authenticated user's details.

        Returns:
            User detail data.
        """
        return await self._get("/user/")

    # -------------------------------------------------------------------------
    # Convenience Methods
    # -------------------------------------------------------------------------

    async def list_all_facilities(
        self,
        country: str | None = None,
        **kwargs,
    ) -> list[dict[str, Any]]:
        """
        Fetch all facilities across all pages.

        Args:
            country: Filter by country code.
            **kwargs: Additional filter parameters.

        Yields:
            All facilities matching the criteria.
        """
        all_facilities = []
        page = 1

        while True:
            result = await self.list_facilities(
                page=page,
                country=country,
                **kwargs,
            )
            facilities = result.get("features", result.get("results", []))
            if not facilities:
                break

            all_facilities.extend(facilities)
            page += 1

            # Check if we've reached the last page
            if "next" not in result or result.get("next") is None:
                break

        return all_facilities

    def list_endpoints(self) -> list[dict[str, str]]:
        """
        List all available API endpoints.

        Returns:
            List of endpoint information dictionaries.
        """
        return [
            {
                "method": "GET",
                "path": "/api/v3/facilities/",
                "description": "List facilities with filtering parameters",
                "function": "list_facilities()",
            },
            {
                "method": "POST",
                "path": "/api/v3/facilities/",
                "description": "Create a new facility",
                "function": "create_facility()",
            },
            {
                "method": "GET",
                "path": "/api/v3/facilities/statistic/",
                "description": "Get facility statistics",
                "function": "get_statistics()",
            },
            {
                "method": "GET",
                "path": "/api/v3/facilities/{osm_type}/{osm_id}",
                "description": "Get a specific facility by OSM type and ID",
                "function": "get_facility()",
            },
            {
                "method": "POST",
                "path": "/api/v3/facilities/{osm_type}/{osm_id}",
                "description": "Update an existing facility",
                "function": "update_facility()",
            },
            {
                "method": "GET",
                "path": "/api/v3/shapefile/{country}",
                "description": "Download shapefile data for a country",
                "function": "download_shapefile()",
            },
            {
                "method": "GET",
                "path": "/api/v3/user/",
                "description": "Get current user details",
                "function": "get_user()",
            },
        ]

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None


# Synchronous wrapper for convenience
class HealthsitesClientSync:
    """
    Synchronous wrapper for HealthsitesClient.

    Example:
        client = HealthsitesClientSync(api_key="your-api-key")
        facilities = client.list_facilities(country="ZA", page=1)
        print(facilities)
        client.close()
    """

    def __init__(self, api_key: str, **kwargs):
        """Initialize synchronous client."""
        self._async_client = HealthsitesClient(api_key, **kwargs)

    def _run(self, coro):
        """Run async coroutine synchronously."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)

    def list_facilities(self, **kwargs):
        """List facilities (sync wrapper)."""
        return self._run(self._async_client.list_facilities(**kwargs))

    def create_facility(self, data):
        """Create facility (sync wrapper)."""
        return self._run(self._async_client.create_facility(data))

    def get_facility(self, osm_type, osm_id):
        """Get facility (sync wrapper)."""
        return self._run(self._async_client.get_facility(osm_type, osm_id))

    def update_facility(self, osm_type, osm_id, data):
        """Update facility (sync wrapper)."""
        return self._run(self._async_client.update_facility(osm_type, osm_id, data))

    def get_statistics(self, **kwargs):
        """Get statistics (sync wrapper)."""
        return self._run(self._async_client.get_statistics(**kwargs))

    def download_shapefile(self, country, output_path=None):
        """Download shapefile (sync wrapper)."""
        return self._run(self._async_client.download_shapefile(country, output_path))

    def get_user(self):
        """Get user (sync wrapper)."""
        return self._run(self._async_client.get_user())

    def list_all_facilities(self, **kwargs):
        """List all facilities (sync wrapper)."""
        return self._run(self._async_client.list_all_facilities(**kwargs))

    def list_endpoints(self):
        """List all endpoints."""
        return self._async_client.list_endpoints()

    def close(self):
        """Close the client."""
        self._run(self._async_client.close())
