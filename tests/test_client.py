"""Tests for the Healthsites API client."""

import os

import httpx
import pytest
import respx

from healthsites import HealthsitesClient, Tag
from healthsites.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

_env_url = os.environ.get("HEALTHSITES_URL")
BASE_URL = f"{_env_url}/api/v3" if _env_url else "https://healthsites.io/api/v3"


@pytest.fixture
def api_key():
    """Test API key."""
    return os.environ.get("HEALTHSITES_API_KEY", "test-api-key")


@pytest.fixture
async def client(api_key):
    """Create a test client."""
    async with HealthsitesClient(api_key=api_key) as client:
        yield client


@pytest.fixture
def tag():
    """Sample Tag for create/update tests."""
    return Tag(
        amenity="clinic",
        healthcare=["doctor"],
        name="Test Facility",
        operator_type="public",
        beds=10,
    )


class TestHealthsitesClient:
    """Tests for HealthsitesClient."""

    def test_base_url_default(self, api_key):
        """Test default base URL falls back to env or hardcoded default."""
        client = HealthsitesClient(api_key=api_key)
        assert client.base_url == BASE_URL

    def test_base_url_custom(self, api_key):
        """Test custom base URL overrides default."""
        client = HealthsitesClient(api_key=api_key, base_url=BASE_URL)
        assert client.base_url == BASE_URL

    def test_auth_header(self, api_key):
        """Test Authorization header is set correctly."""
        client = HealthsitesClient(api_key=api_key)
        assert client._auth_headers() == {"Authorization": f"Bearer {api_key}"}

    def test_list_endpoints(self, api_key):
        """Test listing endpoints."""
        client = HealthsitesClient(api_key=api_key)
        endpoints = client.list_endpoints()

        assert len(endpoints) == 7
        assert all("method" in ep for ep in endpoints)
        assert all("path" in ep for ep in endpoints)
        assert all("description" in ep for ep in endpoints)
        assert all("function" in ep for ep in endpoints)

    def test_tag_to_dict(self, tag):
        """Test Tag.to_dict omits None and empty lists."""
        d = tag.to_dict()
        assert d["amenity"] == "clinic"
        assert d["healthcare"] == ["doctor"]
        assert d["name"] == "Test Facility"
        assert d["beds"] == 10
        assert "operator" not in d
        assert "speciality" not in d

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

        respx.get(f"{BASE_URL}/facilities/").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        result = await client.list_facilities(page=1, country="South Africa")

        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 1

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_facilities_with_timestamps(self, client):
        """Test listing facilities with Unix timestamp filters."""
        mock_response = {"type": "FeatureCollection", "features": []}

        respx.get(f"{BASE_URL}/facilities/").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        result = await client.list_facilities(
            from_timestamp=1700000000,
            to_timestamp=1710000000,
        )

        assert result["type"] == "FeatureCollection"

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_facility(self, client):
        """Test getting a specific facility."""
        mock_response = {
            "type": "Feature",
            "properties": {"name": "Test Facility"},
            "geometry": {"type": "Point", "coordinates": [28.0, -26.0]},
        }

        respx.get(f"{BASE_URL}/facilities/node/123456").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        result = await client.get_facility(osm_type="node", osm_id=123456)

        assert result["type"] == "Feature"
        assert result["properties"]["name"] == "Test Facility"

    @respx.mock
    @pytest.mark.asyncio
    async def test_create_facility_with_tag(self, client, tag):
        """Test creating a facility using a Tag instance."""
        mock_response = {"type": "Feature", "properties": {"name": "Test Facility"}}

        respx.post(f"{BASE_URL}/facilities/").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        result = await client.create_facility(
            lat=47.287,
            lon=8.765,
            tag=tag,
            comment="Test comment",
            source="survey",
        )

        assert result["properties"]["name"] == "Test Facility"

    @respx.mock
    @pytest.mark.asyncio
    async def test_create_facility_with_dict(self, client):
        """Test creating a facility using a raw dict tag."""
        mock_response = {"type": "Feature", "properties": {"name": "Test Facility"}}

        respx.post(f"{BASE_URL}/facilities/").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        result = await client.create_facility(
            lat=47.287,
            lon=8.765,
            tag={"amenity": "clinic", "healthcare": ["doctor"], "name": "Test Facility"},
        )

        assert result["properties"]["name"] == "Test Facility"

    @respx.mock
    @pytest.mark.asyncio
    async def test_update_facility(self, client, tag):
        """Test updating a facility."""
        mock_response = {"type": "Feature", "properties": {"name": "Test Facility"}}

        respx.post(f"{BASE_URL}/facilities/node/123456").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        result = await client.update_facility(
            osm_type="node",
            osm_id=123456,
            lat=47.287,
            lon=8.765,
            tag=tag,
            comment="Updated details",
        )

        assert result["properties"]["name"] == "Test Facility"

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_statistics(self, client):
        """Test getting statistics."""
        mock_response = {
            "total": 1000,
            "by_type": {"hospital": 500, "clinic": 500},
        }

        respx.get(f"{BASE_URL}/facilities/statistic/").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        result = await client.get_statistics(country="South Africa")

        assert result["total"] == 1000

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_user(self, client):
        """Test getting user details."""
        mock_response = {
            "username": "testuser",
            "email": "test@example.com",
        }

        respx.get(f"{BASE_URL}/user/").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        result = await client.get_user()

        assert result["username"] == "testuser"

    @respx.mock
    @pytest.mark.asyncio
    async def test_authentication_error(self, client):
        """Test handling authentication errors."""
        respx.get(f"{BASE_URL}/facilities/").mock(
            return_value=httpx.Response(401, json={"detail": "Invalid API key"})
        )

        with pytest.raises(AuthenticationError):
            await client.list_facilities(page=1)

    @respx.mock
    @pytest.mark.asyncio
    async def test_not_found_error(self, client):
        """Test handling not found errors."""
        respx.get(f"{BASE_URL}/facilities/node/999999").mock(
            return_value=httpx.Response(404, json={"detail": "Not found"})
        )

        with pytest.raises(NotFoundError):
            await client.get_facility(osm_type="node", osm_id=999999)

    @respx.mock
    @pytest.mark.asyncio
    async def test_rate_limit_error(self, client):
        """Test handling rate limit errors."""
        respx.get(f"{BASE_URL}/facilities/").mock(
            return_value=httpx.Response(429, json={"detail": "Rate limit exceeded"})
        )

        with pytest.raises(RateLimitError):
            await client.list_facilities(page=1)

    @respx.mock
    @pytest.mark.asyncio
    async def test_validation_error(self, client):
        """Test handling validation errors."""
        respx.get(f"{BASE_URL}/facilities/").mock(
            return_value=httpx.Response(400, json={"detail": "Invalid parameter"})
        )

        with pytest.raises(ValidationError):
            await client.list_facilities(page=1)