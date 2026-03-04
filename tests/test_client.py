"""Tests for the Healthsites API client."""

import httpx
import pytest
import respx

from healthsites import HealthsitesClient
from healthsites.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


@pytest.fixture
def api_key():
    """Test API key."""
    return "test-api-key"


@pytest.fixture
async def client(api_key):
    """Create a test client."""
    async with HealthsitesClient(api_key=api_key) as client:
        yield client


class TestHealthsitesClient:
    """Tests for HealthsitesClient."""

    def test_list_endpoints(self, api_key):
        """Test listing endpoints."""
        client = HealthsitesClient(api_key=api_key)
        endpoints = client.list_endpoints()

        assert len(endpoints) == 7
        assert all("method" in ep for ep in endpoints)
        assert all("path" in ep for ep in endpoints)
        assert all("description" in ep for ep in endpoints)
        assert all("function" in ep for ep in endpoints)

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_facilities(self, client):
        """Test listing facilities."""
        mock_response = {
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature", "properties": {"name": "Test Facility"}}
            ],
        }

        respx.get("https://healthsites.io/api/v3/facilities/").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        result = await client.list_facilities(page=1, country="ZA")

        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 1

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_facility(self, client):
        """Test getting a specific facility."""
        mock_response = {
            "type": "Feature",
            "properties": {"name": "Test Facility"},
            "geometry": {"type": "Point", "coordinates": [28.0, -26.0]},
        }

        respx.get("https://healthsites.io/api/v3/facilities/node/123456").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        result = await client.get_facility(osm_type="node", osm_id=123456)

        assert result["type"] == "Feature"
        assert result["properties"]["name"] == "Test Facility"

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_statistics(self, client):
        """Test getting statistics."""
        mock_response = {
            "total": 1000,
            "by_type": {"hospital": 500, "clinic": 500},
        }

        respx.get("https://healthsites.io/api/v3/facilities/statistic/").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        result = await client.get_statistics(country="ZA")

        assert result["total"] == 1000

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_user(self, client):
        """Test getting user details."""
        mock_response = {
            "username": "testuser",
            "email": "test@example.com",
        }

        respx.get("https://healthsites.io/api/v3/user/").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        result = await client.get_user()

        assert result["username"] == "testuser"

    @respx.mock
    @pytest.mark.asyncio
    async def test_authentication_error(self, client):
        """Test handling authentication errors."""
        respx.get("https://healthsites.io/api/v3/facilities/").mock(
            return_value=httpx.Response(401, json={"detail": "Invalid API key"})
        )

        with pytest.raises(AuthenticationError):
            await client.list_facilities(page=1)

    @respx.mock
    @pytest.mark.asyncio
    async def test_not_found_error(self, client):
        """Test handling not found errors."""
        respx.get("https://healthsites.io/api/v3/facilities/node/999999").mock(
            return_value=httpx.Response(404, json={"detail": "Not found"})
        )

        with pytest.raises(NotFoundError):
            await client.get_facility(osm_type="node", osm_id=999999)

    @respx.mock
    @pytest.mark.asyncio
    async def test_rate_limit_error(self, client):
        """Test handling rate limit errors."""
        respx.get("https://healthsites.io/api/v3/facilities/").mock(
            return_value=httpx.Response(429, json={"detail": "Rate limit exceeded"})
        )

        with pytest.raises(RateLimitError):
            await client.list_facilities(page=1)

    @respx.mock
    @pytest.mark.asyncio
    async def test_validation_error(self, client):
        """Test handling validation errors."""
        respx.get("https://healthsites.io/api/v3/facilities/").mock(
            return_value=httpx.Response(400, json={"detail": "Invalid parameter"})
        )

        with pytest.raises(ValidationError):
            await client.list_facilities(page=1)

    @respx.mock
    @pytest.mark.asyncio
    async def test_create_facility(self, client):
        """Test creating a facility."""
        mock_response = {
            "type": "Feature",
            "properties": {"name": "New Facility"},
        }

        respx.post("https://healthsites.io/api/v3/facilities/").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        data = {
            "type": "Feature",
            "properties": {"name": "New Facility"},
            "geometry": {"type": "Point", "coordinates": [28.0, -26.0]},
        }

        result = await client.create_facility(data)

        assert result["properties"]["name"] == "New Facility"

    @respx.mock
    @pytest.mark.asyncio
    async def test_update_facility(self, client):
        """Test updating a facility."""
        mock_response = {
            "type": "Feature",
            "properties": {"name": "Updated Facility"},
        }

        respx.post("https://healthsites.io/api/v3/facilities/node/123456").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        data = {"properties": {"name": "Updated Facility"}}
        result = await client.update_facility(
            osm_type="node",
            osm_id=123456,
            data=data,
        )

        assert result["properties"]["name"] == "Updated Facility"
