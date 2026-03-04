"""
Healthsites API Client Library.

A Python client for the Healthsites.io API v3.

Made with love by Kartoza | https://kartoza.com
"""

from healthsites.client import HealthsitesClient
from healthsites.exceptions import (
    HealthsitesError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

__version__ = "0.1.0"
__author__ = "Kartoza"
__email__ = "info@kartoza.com"
__url__ = "https://github.com/kartoza/healthsites-api-client"

__all__ = [
    "HealthsitesClient",
    "HealthsitesError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
]
