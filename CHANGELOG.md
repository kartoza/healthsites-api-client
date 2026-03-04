# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-03

### Added

- Initial release
- Async client `HealthsitesClient` with full API v3 support
- Synchronous wrapper `HealthsitesClientSync`
- All API endpoints:
  - `list_facilities()` - List facilities with filters
  - `create_facility()` - Create new facility
  - `get_facility()` - Get specific facility
  - `update_facility()` - Update facility
  - `get_statistics()` - Get facility statistics
  - `download_shapefile()` - Download country shapefile
  - `get_user()` - Get authenticated user details
  - `list_endpoints()` - List all available endpoints
- Custom exceptions for error handling
- Comprehensive test suite
- MkDocs documentation
- Nix flake for reproducible development

---

Made with love by [Kartoza](https://kartoza.com) | [Donate!](https://github.com/sponsors/kartoza) | [GitHub](https://github.com/kartoza/healthsites-api-client)
