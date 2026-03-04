# Quick Start

## Get an API Key

1. Visit [healthsites.io](https://healthsites.io)
2. Create an account or log in
3. Navigate to your profile to get your API key

## Async Usage (Recommended)

```python
import asyncio
from healthsites import HealthsitesClient

async def main():
    async with HealthsitesClient(api_key="your-api-key") as client:
        # List facilities
        facilities = await client.list_facilities(country="ZA", page=1)
        print(facilities)

asyncio.run(main())
```

## Synchronous Usage

```python
from healthsites.client import HealthsitesClientSync

client = HealthsitesClientSync(api_key="your-api-key")
facilities = client.list_facilities(country="ZA", page=1)
print(facilities)
client.close()
```

## List Available Endpoints

```python
from healthsites import HealthsitesClient

client = HealthsitesClient(api_key="your-api-key")
for endpoint in client.list_endpoints():
    print(f"{endpoint['method']} {endpoint['path']}")
    print(f"  {endpoint['description']}")
    print(f"  Function: {endpoint['function']}")
```

---

Made with love by [Kartoza](https://kartoza.com) | [Donate!](https://github.com/sponsors/kartoza) | [GitHub](https://github.com/kartoza/healthsites-api-client)
